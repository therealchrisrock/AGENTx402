"""gRPC server for Telegram bot backend communication."""

import asyncio
import logging
from concurrent import futures
from datetime import datetime
from typing import Optional
from uuid import uuid4

import grpc
from google.protobuf import timestamp_pb2
from sqlalchemy.ext.asyncio import AsyncSession

# Import generated proto files
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from gen.python.api.v1 import telegram_pb2, telegram_pb2_grpc

# Import user domain and application
from src.backend.core.dependencies import get_db
from src.backend.features.users.application.commands import (
    RegisterUserCommand,
    RegisterUserCommandHandler,
    ConnectWalletCommand,
    ConnectWalletCommandHandler,
)
from src.backend.features.users.application.queries import (
    GetUserByTelegramIdQuery,
    GetUserByTelegramIdQueryHandler,
)
from src.backend.features.users.domain.value_objects import UserState

logger = logging.getLogger(__name__)


class TelegramBackendServicer(telegram_pb2_grpc.TelegramBackendServicer):
    """Implementation of the TelegramBackend gRPC service."""

    def __init__(self):
        """Initialize the service."""
        logger.info("TelegramBackendServicer initialized")

    def _map_user_state(self, state: UserState) -> int:
        """Map domain UserState to proto UserState.

        Args:
            state: Domain user state

        Returns:
            Proto user state enum value
        """
        state_map = {
            UserState.NEW: telegram_pb2.USER_STATE_NEW,
            UserState.WALLET_CONNECTED: telegram_pb2.USER_STATE_WALLET_CONNECTED,
            UserState.WALLET_CONNECTED_NO_FUNDS: telegram_pb2.USER_STATE_WALLET_CONNECTED,
            UserState.FUNDED: telegram_pb2.USER_STATE_FUNDED,
            UserState.ACTIVE_TRADER: telegram_pb2.USER_STATE_ACTIVE_TRADER,
        }
        return state_map.get(state, telegram_pb2.USER_STATE_UNSPECIFIED)

    async def Ping(self, request, context):
        """Health check endpoint."""
        logger.info(f"Ping received: {request.message}")

        # Create timestamp
        now = timestamp_pb2.Timestamp()
        now.GetCurrentTime()

        return telegram_pb2.PingResponse(
            message=f"Pong! Received: {request.message}",
            server_time=now
        )

    async def GetUserState(self, request, context):
        """Get user state by telegram ID."""
        logger.info(f"GetUserState for telegram_id: {request.telegram_id}")

        # Get database session
        async for session in get_db():
            try:
                query_handler = GetUserByTelegramIdQueryHandler(session)
                query = GetUserByTelegramIdQuery(telegram_id=request.telegram_id)
                user = await query_handler.handle(query)

                if not user:
                    return telegram_pb2.GetUserStateResponse(
                        user_exists=False,
                        state=telegram_pb2.USER_STATE_UNSPECIFIED
                    )

                return telegram_pb2.GetUserStateResponse(
                    user_exists=True,
                    state=self._map_user_state(user.state),
                    user_id=str(user.id),
                    wallet_address=user.wallet_address or '',
                    balance=user.balance
                )
            finally:
                await session.close()

    async def RegisterUser(self, request, context):
        """Register a new user."""
        logger.info(f"RegisterUser: {request.telegram_id}, username: {request.telegram_username}")

        # Get database session
        async for session in get_db():
            try:
                command_handler = RegisterUserCommandHandler(session)
                command = RegisterUserCommand(
                    telegram_id=request.telegram_id,
                    telegram_username=request.telegram_username or None
                )
                result = await command_handler.handle(command)

                if result.already_exists:
                    # Get existing user to return state
                    query_handler = GetUserByTelegramIdQueryHandler(session)
                    query = GetUserByTelegramIdQuery(telegram_id=request.telegram_id)
                    user = await query_handler.handle(query)

                    return telegram_pb2.RegisterUserResponse(
                        user_id=str(user.id) if user else '',
                        state=self._map_user_state(user.state) if user else telegram_pb2.USER_STATE_UNSPECIFIED,
                        success=False,
                        message=result.message
                    )

                return telegram_pb2.RegisterUserResponse(
                    user_id=str(result.user_id) if result.user_id else '',
                    state=telegram_pb2.USER_STATE_NEW,
                    success=result.success,
                    message=result.message
                )
            finally:
                await session.close()

    async def ConnectWallet(self, request, context):
        """Connect wallet to user account."""
        logger.info(f"ConnectWallet: user_id={request.user_id}, wallet={request.wallet_address}")

        # Get database session
        async for session in get_db():
            try:
                # Parse UUID from string
                from uuid import UUID
                try:
                    user_id = UUID(request.user_id)
                except ValueError:
                    return telegram_pb2.ConnectWalletResponse(
                        success=False,
                        message="Invalid user ID format",
                        new_state=telegram_pb2.USER_STATE_UNSPECIFIED
                    )

                command_handler = ConnectWalletCommandHandler(session)
                command = ConnectWalletCommand(
                    user_id=user_id,
                    wallet_address=request.wallet_address,
                    wallet_type=request.wallet_type or "manual"
                )
                result = await command_handler.handle(command)

                return telegram_pb2.ConnectWalletResponse(
                    success=result.success,
                    message=result.message,
                    new_state=self._map_user_state(result.new_state) if result.new_state else telegram_pb2.USER_STATE_UNSPECIFIED,
                    balance=result.balance
                )
            finally:
                await session.close()

    async def ClassifyIntent(self, request, context):
        """Classify user message intent."""
        logger.info(f"ClassifyIntent: {request.message}")

        message_lower = request.message.lower()

        # Simple rule-based classification for testing
        if any(word in message_lower for word in ['start', 'help', 'hello', 'hi']):
            domain = telegram_pb2.ClassifyIntentResponse.INTENT_DOMAIN_HELP
            action = 'greeting'
        elif any(word in message_lower for word in ['wallet', 'connect', 'metamask']):
            domain = telegram_pb2.ClassifyIntentResponse.INTENT_DOMAIN_ONBOARDING
            action = 'connect_wallet'
        elif any(word in message_lower for word in ['invest', 'trade', 'buy', 'sell']):
            domain = telegram_pb2.ClassifyIntentResponse.INTENT_DOMAIN_TRADING
            action = 'create_mandate'
        elif any(word in message_lower for word in ['portfolio', 'balance', 'position']):
            domain = telegram_pb2.ClassifyIntentResponse.INTENT_DOMAIN_PORTFOLIO
            action = 'view_portfolio'
        else:
            domain = telegram_pb2.ClassifyIntentResponse.INTENT_DOMAIN_UNSPECIFIED
            action = 'unknown'

        # Extract entities (simple example)
        entities = {}
        if '$' in message_lower:
            # Try to extract amount
            import re
            amount_match = re.search(r'\$(\d+(?:\.\d+)?)', message_lower)
            if amount_match:
                entities['amount'] = amount_match.group(1)

        return telegram_pb2.ClassifyIntentResponse(
            domain=domain,
            action=action,
            entities=entities,
            confidence=0.8 if domain != telegram_pb2.ClassifyIntentResponse.INTENT_DOMAIN_UNSPECIFIED else 0.3
        )


async def serve(port: int = 50051):
    """Start the gRPC server."""
    server = grpc.aio.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=[
            ('grpc.max_receive_message_length', 1024 * 1024 * 10),  # 10MB
            ('grpc.max_send_message_length', 1024 * 1024 * 10),
        ]
    )

    telegram_pb2_grpc.add_TelegramBackendServicer_to_server(
        TelegramBackendServicer(), server
    )

    # Listen on port
    server.add_insecure_port(f'[::]:{port}')

    logger.info(f"gRPC server starting on port {port}...")
    await server.start()

    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Shutting down gRPC server...")
        await server.stop(0)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    asyncio.run(serve())