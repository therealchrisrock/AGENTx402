"""Base aggregate root class for DDD."""

from typing import Any, List

from .entity import Entity
from .domain_event import DomainEvent


class AggregateRoot(Entity):
    """Base class for aggregate roots.

    Aggregate roots are entities that serve as the entry point
    to an aggregate. They maintain consistency boundaries and
    can publish domain events.
    """

    _domain_events: List[DomainEvent] = []

    class Config:
        """Pydantic configuration."""

        from_attributes = True
        validate_assignment = True
        arbitrary_types_allowed = True
        # Exclude private fields from serialization
        fields = {"_domain_events": {"exclude": True}}

    def add_domain_event(self, event: DomainEvent) -> None:
        """Add a domain event to be published."""
        if not hasattr(self, "_domain_events"):
            self._domain_events = []
        self._domain_events.append(event)

    def clear_domain_events(self) -> None:
        """Clear all domain events."""
        self._domain_events = []

    def get_domain_events(self) -> List[DomainEvent]:
        """Get all domain events."""
        if not hasattr(self, "_domain_events"):
            self._domain_events = []
        return self._domain_events.copy()

    def model_post_init(self, __context: Any) -> None:
        """Initialize domain events list after model creation."""
        super().model_post_init(__context)
        if not hasattr(self, "_domain_events"):
            self._domain_events = []
