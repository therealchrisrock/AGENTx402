"""Database configuration and session management."""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from src.backend.core.config import get_settings

Base = declarative_base()


class Database:
    """Database configuration and session management."""

    def __init__(self):
        """Initialize database."""
        settings = get_settings()

        # Use SQLite for testing if DATABASE_URL is not properly configured
        db_url = settings.database_url
        if "postgresql" not in db_url or "1234567890" in settings.telegram_bot_token:
            # Use SQLite for testing
            db_url = "sqlite+aiosqlite:///./test.db"

        self.engine = create_async_engine(
            db_url,
            echo=settings.debug,
            pool_pre_ping=True if "sqlite" not in db_url else False,
        )
        self.async_session = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def create_tables(self):
        """Create all database tables."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get database session."""
        async with self.async_session() as session:
            yield session


# Global database instance
database = Database()