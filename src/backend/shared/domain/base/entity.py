"""Base entity class for DDD."""

from abc import ABC
from datetime import datetime
from typing import Any, TypeVar
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Entity(BaseModel, ABC):
    """Base class for all domain entities.

    Entities have unique identity that persists over time.
    """

    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """Pydantic configuration."""

        from_attributes = True
        validate_assignment = True
        arbitrary_types_allowed = True

    def __eq__(self, other: Any) -> bool:
        """Entities are equal if they have the same ID."""
        if not isinstance(other, Entity):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """Hash based on entity ID."""
        return hash(self.id)


TEntity = TypeVar("TEntity", bound=Entity)
