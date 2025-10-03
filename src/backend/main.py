"""FastAPI backend application entry point."""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.core.config import get_settings
from src.backend.core.dependencies import sessionmanager
from src.backend.features.agents.presentation.api import agent_router, mandate_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Get settings
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager.

    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting TradingBotAgent API...")
    logger.info(f"Database URL: {settings.database_url}")

    yield

    # Shutdown
    logger.info("Shutting down TradingBotAgent API...")
    if sessionmanager:
        await sessionmanager.close()
    logger.info("Database connections closed")


app = FastAPI(
    title="TradingBotAgent API",
    version="0.1.0",
    description="AI-powered trading bot platform with HTTP 402 mandate system",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(mandate_router, prefix="/api/v1/mandates", tags=["mandates"])
app.include_router(agent_router, prefix="/api/v1/agents", tags=["agents"])


@app.get("/health")
async def health_check():
    """Health check endpoint.

    Returns:
        Health status
    """
    return {"status": "healthy", "service": "tradingbotagent-api", "version": "0.1.0"}


@app.get("/")
async def hello_world():
    """Hello world endpoint.

    Returns:
        Hello world message
    """
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.backend.main:app", host="0.0.0.0", port=8000, reload=True)
