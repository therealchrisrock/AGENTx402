"""gRPC server for Telegram bot backend communication."""

import asyncio
import logging
from concurrent import futures
from datetime import datetime
from typing import Optional
from uuid import uuid4

import grpc
from google.protobuf import timestamp_pb2

# Import generated proto files
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from gen.python.api.v1 import telegram_pb2, telegram_pb2_grpc

logger = logging.getLogger(__name__)


class TelegramBackendServicer(telegram_pb2_grpc.TelegramBackendServicer):
    """Implementation of the TelegramBackend gRPC service."""

    def __init__(self):
        """Initialize the service with in-memory user storage (for testing)."""
        # In-memory storage for testing
        self.users = {}
        logger.info("TelegramBackendServicer initialized")

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

        user = self.users.get(request.telegram_id)

        if not user:
            return telegram_pb2.GetUserStateResponse(
                user_exists=False,
                state=telegram_pb2.USER_STATE_UNSPECIFIED
            )

        return telegram_pb2.GetUserStateResponse(
            user_exists=True,
            state=user['state'],
            user_id=user['user_id'],
            wallet_address=user.get('wallet_address', ''),
            balance=user.get('balance', 0.0)
        )

    async def RegisterUser(self, request, context):
        """Register a new user."""
        logger.info(f"RegisterUser: {request.telegram_id}, username: {request.telegram_username}")

        # Check if user already exists
        if request.telegram_id in self.users:
            user = self.users[request.telegram_id]
            return telegram_pb2.RegisterUserResponse(
                user_id=user['user_id'],
                state=user['state'],
                success=False,
                message="User already exists"
            )

        # Create new user
        user_id = str(uuid4())
        self.users[request.telegram_id] = {
            'user_id': user_id,
            'telegram_username': request.telegram_username,
            'state': telegram_pb2.USER_STATE_NEW,
            'created_at': datetime.utcnow()
        }

        return telegram_pb2.RegisterUserResponse(
            user_id=user_id,
            state=telegram_pb2.USER_STATE_NEW,
            success=True,
            message="User registered successfully"
        )

    async def ConnectWallet(self, request, context):
        """Connect wallet to user account."""
        logger.info(f"ConnectWallet: user_id={request.user_id}, wallet={request.wallet_address}")

        # Find user by user_id
        user = None
        telegram_id = None
        for tid, u in self.users.items():
            if u['user_id'] == request.user_id:
                user = u
                telegram_id = tid
                break

        if not user:
            return telegram_pb2.ConnectWalletResponse(
                success=False,
                message="User not found",
                new_state=telegram_pb2.USER_STATE_UNSPECIFIED
            )

        # Update user with wallet
        user['wallet_address'] = request.wallet_address
        user['wallet_type'] = request.wallet_type
        user['state'] = telegram_pb2.USER_STATE_WALLET_CONNECTED

        # Simulate balance check (would call web3 in production)
        balance = 1000.0 if request.wallet_address.startswith('0x') else 0.0
        user['balance'] = balance

        if balance >= 50:
            user['state'] = telegram_pb2.USER_STATE_FUNDED

        return telegram_pb2.ConnectWalletResponse(
            success=True,
            message=f"Wallet connected successfully. Balance: ${balance:.2f}",
            new_state=user['state'],
            balance=balance
        )

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