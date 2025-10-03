"""SQLAlchemy implementation of UserRepository."""

import logging
from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.features.users.domain.entities import User
from src.backend.features.users.domain.repositories import UserRepository
from src.backend.features.users.infrastructure.models import UserORM, UserMapper

logger = logging.getLogger(__name__)


class SQLAlchemyUserRepository(UserRepository):
    """SQLAlchemy implementation of UserRepository."""

    def __init__(self, session: AsyncSession):
        """Initialize repository with database session.

        Args:
            session: AsyncSession for database operations
        """
        self.session = session
        self.mapper = UserMapper()

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID.

        Args:
            user_id: User UUID

        Returns:
            User or None if not found
        """
        result = await self.session.get(UserORM, user_id)
        if result:
            return self.mapper.to_entity(result)
        return None

    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Get user by Telegram ID.

        Args:
            telegram_id: Telegram user ID

        Returns:
            User or None if not found
        """
        stmt = select(UserORM).where(UserORM.telegram_id == telegram_id)
        result = await self.session.execute(stmt)
        orm = result.scalar_one_or_none()

        if orm:
            return self.mapper.to_entity(orm)
        return None

    async def get_by_wallet_address(self, wallet_address: str) -> Optional[User]:
        """Get user by wallet address.

        Args:
            wallet_address: Ethereum wallet address

        Returns:
            User or None if not found
        """
        # Normalize address for comparison
        normalized_address = wallet_address.lower()

        stmt = select(UserORM).where(
            UserORM.wallet_address == normalized_address
        )
        result = await self.session.execute(stmt)
        orm = result.scalar_one_or_none()

        if orm:
            return self.mapper.to_entity(orm)
        return None

    async def save(self, user: User) -> None:
        """Save user aggregate.

        Args:
            user: User to save
        """
        # Check if user exists
        existing = await self.session.get(UserORM, user.id)

        if existing:
            # Update existing
            self.mapper.update_orm(existing, user)
            logger.info(f"Updated user {user.id}")
        else:
            # Create new
            orm = self.mapper.to_orm(user)
            self.session.add(orm)
            logger.info(f"Created new user {user.id}")

        # Commit will be handled by unit of work or transaction manager
        await self.session.flush()

        # Process domain events
        for event in user.get_domain_events():
            logger.info(f"Domain event: {event.event_type} for user {user.id}")
            # Here you would publish events to event bus/queue
            # For now, just log them

        # Clear events after processing
        user.clear_domain_events()

    async def exists_by_telegram_id(self, telegram_id: int) -> bool:
        """Check if user exists by Telegram ID.

        Args:
            telegram_id: Telegram user ID

        Returns:
            True if user exists
        """
        stmt = select(UserORM.id).where(UserORM.telegram_id == telegram_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def exists_by_wallet_address(self, wallet_address: str) -> bool:
        """Check if wallet address is already registered.

        Args:
            wallet_address: Ethereum wallet address

        Returns:
            True if wallet is already registered
        """
        # Normalize address for comparison
        normalized_address = wallet_address.lower()

        stmt = select(UserORM.id).where(
            UserORM.wallet_address == normalized_address
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None