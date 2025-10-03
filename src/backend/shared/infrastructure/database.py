"""Shared database infrastructure."""

import logging
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

logger = logging.getLogger(__name__)


class DatabaseSessionManager:
    """Database session manager."""

    def __init__(self, database_url: str, echo: bool = False):
        """Initialize database session manager.

        Args:
            database_url: Database URL
            echo: Whether to echo SQL statements
        """
        # Use SQLite for testing if DATABASE_URL is not properly configured
        if "postgresql" not in database_url or "localhost" in database_url:
            # Use SQLite for testing
            database_url = "sqlite+aiosqlite:///./test.db"
            logger.info("Using SQLite for testing")

        self.engine = create_async_engine(
            database_url,
            echo=echo,
            pool_pre_ping=True if "sqlite" not in database_url else False,
        )
        self.async_session = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def create_tables(self):
        """Create all database tables."""
        from src.backend.shared.infrastructure.base import Base
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get database session.

        Yields:
            Database session
        """
        async with self.async_session() as session:
            yield session

    async def close(self):
        """Close database connections."""
        await self.engine.dispose()