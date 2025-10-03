"""Unit of work interface."""

from abc import ABC, abstractmethod


class IUnitOfWork(ABC):
    """Unit of work interface for managing transactions.

    The Unit of Work pattern maintains a list of objects affected by a
    business transaction and coordinates the writing out of changes.
    """

    @abstractmethod
    async def commit(self) -> None:
        """Commit the transaction."""
        pass

    @abstractmethod
    async def rollback(self) -> None:
        """Rollback the transaction."""
        pass

    @abstractmethod
    async def __aenter__(self) -> "IUnitOfWork":
        """Enter the context manager."""
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the context manager."""
        pass
