"""Get user query and handler."""

import logging
from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.features.users.domain.entities import User
from src.backend.features.users.infrastructure.repositories import SQLAlchemyUserRepository

logger = logging.getLogger(__name__)


class GetUserByTelegramIdQuery(BaseModel):
    """Query to get user by Telegram ID."""

    telegram_id: int = Field(..., description="Telegram user ID")


class GetUserByTelegramIdQueryHandler:
    """Handler for GetUserByTelegramIdQuery."""

    def __init__(self, session: AsyncSession):
        """Initialize handler with database session.

        Args:
            session: Database session
        """
        self.session = session
        self.repository = SQLAlchemyUserRepository(session)

    async def handle(self, query: GetUserByTelegramIdQuery) -> Optional[User]:
        """Handle get user query.

        Args:
            query: Get user query

        Returns:
            User or None if not found
        """
        try:
            user = await self.repository.get_by_telegram_id(query.telegram_id)
            if user:
                logger.debug(f"Found user {user.id} for telegram_id: {query.telegram_id}")
            else:
                logger.debug(f"No user found for telegram_id: {query.telegram_id}")
            return user
        except Exception as e:
            logger.error(f"Failed to get user: {e}")
            return None