"""User repository interface."""

from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from ..entities import User


class UserRepository(ABC):
    """Abstract repository for User aggregate.

    Defines the interface for user persistence operations.
    """

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID.

        Args:
            user_id: User UUID

        Returns:
            User or None if not found
        """
        pass

    @abstractmethod
    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Get user by Telegram ID.

        Args:
            telegram_id: Telegram user ID

        Returns:
            User or None if not found
        """
        pass

    @abstractmethod
    async def get_by_wallet_address(self, wallet_address: str) -> Optional[User]:
        """Get user by wallet address.

        Args:
            wallet_address: Ethereum wallet address

        Returns:
            User or None if not found
        """
        pass

    @abstractmethod
    async def save(self, user: User) -> None:
        """Save user aggregate.

        Args:
            user: User to save
        """
        pass

    @abstractmethod
    async def exists_by_telegram_id(self, telegram_id: int) -> bool:
        """Check if user exists by Telegram ID.

        Args:
            telegram_id: Telegram user ID

        Returns:
            True if user exists
        """
        pass

    @abstractmethod
    async def exists_by_wallet_address(self, wallet_address: str) -> bool:
        """Check if wallet address is already registered.

        Args:
            wallet_address: Ethereum wallet address

        Returns:
            True if wallet is already registered
        """
        pass