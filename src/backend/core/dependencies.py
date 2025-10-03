"""FastAPI dependencies."""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.core.config import get_settings
from src.backend.shared.infrastructure.database import DatabaseSessionManager

# Get settings
settings = get_settings()

# Initialize database session manager
sessionmanager = DatabaseSessionManager(settings.database_url, echo=settings.debug)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session.

    Yields:
        Database session
    """
    async for session in sessionmanager.get_session():
        yield session
