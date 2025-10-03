"""FastAPI backend application entry point."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.backend.features.agents.presentation.api import agent_router, mandate_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager.

    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting TradingBotAgent API...")
    # TODO: Initialize database, Redis, etc.

    yield

    # Shutdown
    logger.info("Shutting down TradingBotAgent API...")
    # TODO: Close connections


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
