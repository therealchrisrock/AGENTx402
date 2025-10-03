"""Unit of Work implementation for SQLAlchemy."""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.shared.application.interfaces import IUnitOfWork
from src.backend.shared.domain.base import DomainEvent


class SQLAlchemyUnitOfWork(IUnitOfWork):
    """SQLAlchemy implementation of Unit of Work pattern.

    Manages transaction boundaries and coordinates:
    - Database session lifecycle
    - Commit/rollback operations
    - Domain event collection for post-commit dispatch
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialize Unit of Work.

        Args:
            session: SQLAlchemy async session
        """
        self.session = session
        self._domain_events: list[DomainEvent] = []

    async def commit(self) -> None:
        """Commit the transaction and collect domain events."""
        # Collect domain events from all tracked entities before commit
        self._collect_domain_events()

        # Commit the transaction
        await self.session.commit()

    async def rollback(self) -> None:
        """Rollback the transaction and clear domain events."""
        await self.session.rollback()
        self._domain_events.clear()

    def collect_events(self) -> list[DomainEvent]:
        """Get collected domain events for dispatching.

        Returns:
            List of domain events
        """
        return self._domain_events.copy()

    def clear_events(self) -> None:
        """Clear collected domain events."""
        self._domain_events.clear()

    async def __aenter__(self) -> "SQLAlchemyUnitOfWork":
        """Enter the context manager.

        Returns:
            Self
        """
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit the context manager.

        Args:
            exc_type: Exception type
            exc_val: Exception value
            exc_tb: Exception traceback
        """
        if exc_type is not None:
            await self.rollback()
        else:
            # Events are collected in commit(), will be dispatched by caller
            pass

    def _collect_domain_events(self) -> None:
        """Collect domain events from tracked aggregate roots.

        Iterates through all objects in the session and extracts
        domain events from aggregate roots.
        """
        for obj in self.session.identity_map.values():
            # Check if object has domain events (aggregate root)
            if hasattr(obj, "get_domain_events"):
                events = obj.get_domain_events()
                self._domain_events.extend(events)
                # Clear events from aggregate after collection
                if hasattr(obj, "clear_domain_events"):
                    obj.clear_domain_events()
