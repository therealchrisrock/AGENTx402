"""Simple gRPC server for testing onboarding flow."""

import asyncio
import logging
from concurrent import futures
from datetime import datetime
from uuid import uuid4
from typing import Dict, Any

import grpc
from google.protobuf import timestamp_pb2

# Import generated proto files
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'gen', 'python'))

from api.v1 import telegram_pb2, telegram_pb2_grpc

logger = logging.getLogger(__name__)

# In-memory storage for testing
users_db: Dict[int, Dict[str, Any]] = {}


class TelegramBackendServicer(telegram_pb2_grpc.TelegramBackendServicer):
    """Simple implementation of the TelegramBackend gRPC service."""

    async def Ping(self, request, context):
        """Health check endpoint."""
        logger.info(f"Ping received: {request.message}")

        now = timestamp_pb2.Timestamp()
        now.GetCurrentTime()

        return telegram_pb2.PingResponse(
            message=f"Pong! Received: {request.message}",
            server_time=now
        )

    async def GetUserState(self, request, context):
        """Get user state by telegram ID."""
        logger.info(f"GetUserState for telegram_id: {request.telegram_id}")

        user = users_db.get(request.telegram_id)

        if not user:
            return telegram_pb2.GetUserStateResponse(
                user_exists=False,
                state=telegram_pb2.USER_STATE_UNSPECIFIED
            )

        return telegram_pb2.GetUserStateResponse(
            user_exists=True,
            state=user['state'],
            user_id=user['id'],
            wallet_address=user.get('wallet_address', ''),
            balance=user.get('balance', 0)
        )

    async def RegisterUser(self, request, context):
        """Register a new user."""
        logger.info(f"RegisterUser: {request.telegram_id}, username: {request.telegram_username}")

        if request.telegram_id in users_db:
            user = users_db[request.telegram_id]
            return telegram_pb2.RegisterUserResponse(
                user_id=user['id'],
                state=user['state'],
                success=False,
                message="User already exists"
            )

        # Create new user
        user_id = str(uuid4())
        users_db[request.telegram_id] = {
            'id': user_id,
            'telegram_username': request.telegram_username,
            'state': telegram_pb2.USER_STATE_NEW,
            'balance': 0,
            'wallet_address': None
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

        # Find user by ID
        user = None
        for tid, u in users_db.items():
            if u['id'] == request.user_id:
                user = u
                break

        if not user:
            return telegram_pb2.ConnectWalletResponse(
                success=False,
                message="User not found",
                new_state=telegram_pb2.USER_STATE_UNSPECIFIED
            )

        # Update user wallet
        user['wallet_address'] = request.wallet_address
        user['wallet_type'] = request.wallet_type or "manual"

        # Simulate balance check (mock)
        balance = 100.0  # Mock balance
        user['balance'] = balance

        if balance >= 50:
            user['state'] = telegram_pb2.USER_STATE_FUNDED
        else:
            user['state'] = telegram_pb2.USER_STATE_WALLET_CONNECTED

        return telegram_pb2.ConnectWalletResponse(
            success=True,
            message="Wallet connected successfully",
            new_state=user['state'],
            balance=balance
        )

    async def ClassifyIntent(self, request, context):
        """Classify user message intent."""
        logger.info(f"ClassifyIntent: {request.message}")

        message_lower = request.message.lower()

        if any(word in message_lower for word in ['start', 'help', 'hello', 'hi']):
            domain = telegram_pb2.ClassifyIntentResponse.INTENT_DOMAIN_HELP
            action = 'greeting'
        elif any(word in message_lower for word in ['wallet', 'connect', 'metamask']):
            domain = telegram_pb2.ClassifyIntentResponse.INTENT_DOMAIN_ONBOARDING
            action = 'connect_wallet'
        else:
            domain = telegram_pb2.ClassifyIntentResponse.INTENT_DOMAIN_UNSPECIFIED
            action = 'unknown'

        return telegram_pb2.ClassifyIntentResponse(
            domain=domain,
            action=action,
            entities={},
            confidence=0.8
        )


async def serve(port: int = 50051):
    """Start the gRPC server."""
    server = grpc.aio.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=[
            ('grpc.max_receive_message_length', 1024 * 1024 * 10),
            ('grpc.max_send_message_length', 1024 * 1024 * 10),
        ]
    )

    telegram_pb2_grpc.add_TelegramBackendServicer_to_server(
        TelegramBackendServicer(), server
    )

    server.add_insecure_port(f'[::]:{port}')

    logger.info(f"Test gRPC server starting on port {port}...")
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