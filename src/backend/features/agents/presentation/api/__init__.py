"""API routes for agents feature."""

from .agent_routes import router as agent_router
from .mandate_routes import router as mandate_router

__all__ = [
    "mandate_router",
    "agent_router",
]
