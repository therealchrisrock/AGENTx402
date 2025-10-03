"""Base domain event class for DDD."""

from abc import ABC
from datetime import datetime
from typing import Any, Dict
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class DomainEvent(BaseModel, ABC):
    """Base class for all domain events.

    Domain events represent something that happened in the domain
    that domain experts care about.
    """

    event_id: UUID = Field(default_factory=uuid4)
    occurred_at: datetime = Field(default_factory=datetime.utcnow)
    aggregate_id: UUID
    event_type: str

    class Config:
        """Pydantic configuration."""

        frozen = True  # Events are immutable
        validate_assignment = True
        arbitrary_types_allowed = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary."""
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DomainEvent":
        """Create event from dictionary."""
        return cls(**data)
