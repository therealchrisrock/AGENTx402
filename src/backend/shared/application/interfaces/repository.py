"""Base repository interface."""

from abc import ABC, abstractmethod
from typing import Generic, List, Optional
from uuid import UUID

from src.backend.shared.domain.base import TEntity


class IRepository(ABC, Generic[TEntity]):
    """Base repository interface for data access.

    Repositories abstract the data access layer and provide
    a collection-like interface for accessing domain objects.
    """

    @abstractmethod
    async def add(self, entity: TEntity) -> TEntity:
        """Add a new entity.

        Args:
            entity: Entity to add

        Returns:
            The added entity
        """
        pass

    @abstractmethod
    async def get_by_id(self, entity_id: UUID) -> Optional[TEntity]:
        """Get entity by ID.

        Args:
            entity_id: Entity ID

        Returns:
            Entity if found, None otherwise
        """
        pass

    @abstractmethod
    async def get_all(self) -> List[TEntity]:
        """Get all entities.

        Returns:
            List of all entities
        """
        pass

    @abstractmethod
    async def update(self, entity: TEntity) -> TEntity:
        """Update an existing entity.

        Args:
            entity: Entity to update

        Returns:
            The updated entity
        """
        pass

    @abstractmethod
    async def delete(self, entity_id: UUID) -> bool:
        """Delete an entity.

        Args:
            entity_id: Entity ID

        Returns:
            True if deleted, False otherwise
        """
        pass

    @abstractmethod
    async def exists(self, entity_id: UUID) -> bool:
        """Check if entity exists.

        Args:
            entity_id: Entity ID

        Returns:
            True if exists, False otherwise
        """
        pass
