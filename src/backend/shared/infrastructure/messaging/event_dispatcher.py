"""Domain event dispatcher implementation."""

import logging
from collections import defaultdict
from typing import Callable, Type

from src.backend.shared.domain.base import DomainEvent

logger = logging.getLogger(__name__)

EventHandler = Callable[[DomainEvent], None]


class DomainEventDispatcher:
    """In-memory domain event dispatcher.

    Handles registration and dispatching of domain events to handlers.
    Events are dispatched synchronously after transaction commit.
    """

    def __init__(self) -> None:
        """Initialize event dispatcher."""
        self._handlers: dict[Type[DomainEvent], list[EventHandler]] = defaultdict(list)

    def register(
        self, event_type: Type[DomainEvent], handler: EventHandler
    ) -> None:
        """Register an event handler.

        Args:
            event_type: Type of domain event
            handler: Handler function
        """
        self._handlers[event_type].append(handler)
        logger.debug(
            f"Registered handler {handler.__name__} for event {event_type.__name__}"
        )

    def dispatch(self, event: DomainEvent) -> None:
        """Dispatch a domain event to all registered handlers.

        Args:
            event: Domain event to dispatch
        """
        event_type = type(event)
        handlers = self._handlers.get(event_type, [])

        if not handlers:
            logger.debug(f"No handlers registered for event {event_type.__name__}")
            return

        logger.info(f"Dispatching event {event_type.__name__} to {len(handlers)} handlers")

        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                logger.error(
                    f"Error dispatching event {event_type.__name__} to {handler.__name__}: {e}",
                    exc_info=True,
                )

    def dispatch_all(self, events: list[DomainEvent]) -> None:
        """Dispatch multiple domain events.

        Args:
            events: List of domain events
        """
        for event in events:
            self.dispatch(event)

    def clear_handlers(self) -> None:
        """Clear all registered handlers (useful for testing)."""
        self._handlers.clear()
        logger.debug("Cleared all event handlers")


# Global dispatcher instance
_dispatcher = DomainEventDispatcher()


def get_event_dispatcher() -> DomainEventDispatcher:
    """Get the global event dispatcher instance.

    Returns:
        Domain event dispatcher
    """
    return _dispatcher
