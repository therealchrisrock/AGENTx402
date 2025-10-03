"""Initialize database tables."""

import asyncio
import logging
from sqlalchemy.ext.asyncio import create_async_engine
from src.backend.core.config import get_settings
from src.backend.core.database import Base

# Import all models to ensure they're registered
from src.backend.features.users.infrastructure.models import UserModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init_db():
    """Create database tables."""
    settings = get_settings()

    # Create engine
    engine = create_async_engine(
        settings.database_url,
        echo=True
    )

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()
    logger.info("Database tables created successfully!")


if __name__ == "__main__":
    asyncio.run(init_db())