"""gRPC client for communicating with backend services."""

import logging
from typing import Optional, Dict, Any
import grpc

# Import generated proto files
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from gen.python.api.v1 import telegram_pb2, telegram_pb2_grpc

logger = logging.getLogger(__name__)


class BackendGRPCClient:
    """gRPC client for backend communication."""

    def __init__(self, host: str = "localhost", port: int = 50051):
        """Initialize gRPC client.

        Args:
            host: Backend host
            port: Backend gRPC port
        """
        self.host = host
        self.port = port
        self.channel = None
        self.stub = None
        self._connect()

    def _connect(self):
        """Establish gRPC connection."""
        try:
            # Create channel with options
            options = [
                ('grpc.max_receive_message_length', 1024 * 1024 * 10),
                ('grpc.max_send_message_length', 1024 * 1024 * 10),
            ]
            self.channel = grpc.insecure_channel(
                f'{self.host}:{self.port}',
                options=options
            )
            self.stub = telegram_pb2_grpc.TelegramBackendStub(self.channel)
            logger.info(f"Connected to gRPC server at {self.host}:{self.port}")
        except Exception as e:
            logger.error(f"Failed to connect to gRPC server: {e}")
            raise

    def close(self):
        """Close gRPC connection."""
        if self.channel:
            self.channel.close()
            logger.info("gRPC connection closed")

    async def ping(self, message: str = "Hello") -> Optional[str]:
        """Test connection with ping.

        Args:
            message: Message to send

        Returns:
            Response message or None if error
        """
        try:
            request = telegram_pb2.PingRequest(message=message)
            response = self.stub.Ping(request)
            return response.message
        except grpc.RpcError as e:
            logger.error(f"gRPC ping failed: {e.code()}: {e.details()}")
            return None

    async def get_user_state(self, telegram_id: int) -> Optional[Dict[str, Any]]:
        """Get user state by telegram ID.

        Args:
            telegram_id: Telegram user ID

        Returns:
            User state dict or None if not found
        """
        try:
            request = telegram_pb2.GetUserStateRequest(telegram_id=telegram_id)
            response = self.stub.GetUserState(request)

            if not response.user_exists:
                return None

            return {
                'user_id': response.user_id,
                'state': self._state_to_string(response.state),
                'wallet_address': response.wallet_address,
                'balance': response.balance
            }
        except grpc.RpcError as e:
            logger.error(f"gRPC GetUserState failed: {e.code()}: {e.details()}")
            return None

    async def register_user(self, telegram_id: int, username: str = "") -> Optional[Dict[str, Any]]:
        """Register a new user.

        Args:
            telegram_id: Telegram user ID
            username: Telegram username

        Returns:
            Registration result or None if error
        """
        try:
            request = telegram_pb2.RegisterUserRequest(
                telegram_id=telegram_id,
                telegram_username=username
            )
            response = self.stub.RegisterUser(request)

            return {
                'user_id': response.user_id,
                'state': self._state_to_string(response.state),
                'success': response.success,
                'message': response.message
            }
        except grpc.RpcError as e:
            logger.error(f"gRPC RegisterUser failed: {e.code()}: {e.details()}")
            return None

    async def connect_wallet(
        self,
        user_id: str,
        wallet_address: str,
        wallet_type: str = "manual"
    ) -> Optional[Dict[str, Any]]:
        """Connect wallet to user account.

        Args:
            user_id: User UUID
            wallet_address: Wallet address
            wallet_type: Type of wallet connection

        Returns:
            Connection result or None if error
        """
        try:
            request = telegram_pb2.ConnectWalletRequest(
                user_id=user_id,
                wallet_address=wallet_address,
                wallet_type=wallet_type
            )
            response = self.stub.ConnectWallet(request)

            return {
                'success': response.success,
                'message': response.message,
                'new_state': self._state_to_string(response.new_state),
                'balance': response.balance
            }
        except grpc.RpcError as e:
            logger.error(f"gRPC ConnectWallet failed: {e.code()}: {e.details()}")
            return None

    async def classify_intent(
        self,
        message: str,
        telegram_id: int,
        context: Optional[Dict[str, str]] = None
    ) -> Optional[Dict[str, Any]]:
        """Classify user message intent.

        Args:
            message: User message
            telegram_id: User telegram ID
            context: Optional context dict

        Returns:
            Intent classification or None if error
        """
        try:
            request = telegram_pb2.ClassifyIntentRequest(
                message=message,
                telegram_id=telegram_id,
                context=context or {}
            )
            response = self.stub.ClassifyIntent(request)

            return {
                'domain': self._domain_to_string(response.domain),
                'action': response.action,
                'entities': dict(response.entities),
                'confidence': response.confidence
            }
        except grpc.RpcError as e:
            logger.error(f"gRPC ClassifyIntent failed: {e.code()}: {e.details()}")
            return None

    def _state_to_string(self, state) -> str:
        """Convert UserState enum to string."""
        state_map = {
            telegram_pb2.USER_STATE_UNSPECIFIED: "UNSPECIFIED",
            telegram_pb2.USER_STATE_NEW: "NEW",
            telegram_pb2.USER_STATE_WALLET_CONNECTED: "WALLET_CONNECTED",
            telegram_pb2.USER_STATE_FUNDED: "FUNDED",
            telegram_pb2.USER_STATE_ACTIVE_TRADER: "ACTIVE_TRADER",
        }
        return state_map.get(state, "UNKNOWN")

    def _domain_to_string(self, domain) -> str:
        """Convert IntentDomain enum to string."""
        domain_map = {
            telegram_pb2.ClassifyIntentResponse.INTENT_DOMAIN_UNSPECIFIED: "UNSPECIFIED",
            telegram_pb2.ClassifyIntentResponse.INTENT_DOMAIN_ONBOARDING: "ONBOARDING",
            telegram_pb2.ClassifyIntentResponse.INTENT_DOMAIN_TRADING: "TRADING",
            telegram_pb2.ClassifyIntentResponse.INTENT_DOMAIN_PORTFOLIO: "PORTFOLIO",
            telegram_pb2.ClassifyIntentResponse.INTENT_DOMAIN_HELP: "HELP",
        }
        return domain_map.get(domain, "UNKNOWN")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# Singleton instance
_client_instance: Optional[BackendGRPCClient] = None


def get_grpc_client() -> BackendGRPCClient:
    """Get or create gRPC client singleton.

    Returns:
        gRPC client instance
    """
    global _client_instance
    if _client_instance is None:
        _client_instance = BackendGRPCClient()
    return _client_instance