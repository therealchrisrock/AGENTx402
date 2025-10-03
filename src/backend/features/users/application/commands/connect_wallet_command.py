"""Connect wallet command and handler."""

import logging
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.features.users.domain.value_objects import UserState
from src.backend.features.users.infrastructure.repositories import SQLAlchemyUserRepository

logger = logging.getLogger(__name__)


class ConnectWalletCommand(BaseModel):
    """Command to connect wallet to user account."""

    user_id: UUID = Field(..., description="User ID")
    wallet_address: str = Field(..., description="Ethereum wallet address")
    wallet_type: str = Field(default="manual", description="Wallet connection type")


class ConnectWalletResult(BaseModel):
    """Result of wallet connection."""

    success: bool
    message: str
    new_state: Optional[UserState] = None
    balance: float = 0.0


class ConnectWalletCommandHandler:
    """Handler for ConnectWalletCommand."""

    def __init__(self, session: AsyncSession):
        """Initialize handler with database session.

        Args:
            session: Database session
        """
        self.session = session
        self.repository = SQLAlchemyUserRepository(session)

    async def handle(self, command: ConnectWalletCommand) -> ConnectWalletResult:
        """Handle wallet connection command.

        Args:
            command: Wallet connection command

        Returns:
            Connection result
        """
        try:
            # Get user
            user = await self.repository.get_by_id(command.user_id)
            if not user:
                return ConnectWalletResult(
                    success=False,
                    message="User not found"
                )

            # Check if wallet is already registered to another user
            existing_wallet_user = await self.repository.get_by_wallet_address(command.wallet_address)
            if existing_wallet_user and existing_wallet_user.id != command.user_id:
                return ConnectWalletResult(
                    success=False,
                    message="Wallet already registered to another user"
                )

            # TODO: Check actual wallet balance using Web3
            # For now, simulate balance check
            balance = 1000.0 if command.wallet_address.startswith("0x") else 0.0

            # Connect wallet
            user.connect_wallet(
                wallet_address=command.wallet_address,
                wallet_type=command.wallet_type,
                balance=balance
            )

            # Save changes
            await self.repository.save(user)
            await self.session.commit()

            logger.info(f"Connected wallet {command.wallet_address[:10]}... to user {user.id}")

            return ConnectWalletResult(
                success=True,
                message=f"Wallet connected successfully. Balance: ${balance:.2f}",
                new_state=user.state,
                balance=balance
            )

        except ValueError as e:
            # Domain validation error
            logger.warning(f"Wallet connection validation failed: {e}")
            return ConnectWalletResult(
                success=False,
                message=str(e)
            )
        except Exception as e:
            logger.error(f"Failed to connect wallet: {e}")
            await self.session.rollback()
            return ConnectWalletResult(
                success=False,
                message=f"Connection failed: {str(e)}"
            )