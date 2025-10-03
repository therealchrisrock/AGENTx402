"""Mandate repository interface."""

from abc import abstractmethod
from typing import List, Optional
from uuid import UUID

from src.backend.shared.application.interfaces import IRepository
from ..entities import Mandate


class IMandateRepository(IRepository[Mandate]):
    """Repository interface for Mandate aggregate."""

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> List[Mandate]:
        """Get all mandates for a user.

        Args:
            user_id: User ID

        Returns:
            List of user's mandates
        """
        pass

    @abstractmethod
    async def get_active_mandates(self, user_id: UUID) -> List[Mandate]:
        """Get all active (non-revoked, valid) mandates for a user.

        Args:
            user_id: User ID

        Returns:
            List of active mandates
        """
        pass

    @abstractmethod
    async def get_by_nonce(self, user_id: UUID, nonce: int) -> Optional[Mandate]:
        """Get mandate by user ID and nonce.

        Args:
            user_id: User ID
            nonce: Mandate nonce

        Returns:
            Mandate if found, None otherwise
        """
        pass
