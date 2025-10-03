"""Messaging infrastructure."""

from .event_dispatcher import DomainEventDispatcher, get_event_dispatcher

__all__ = [
    "DomainEventDispatcher",
    "get_event_dispatcher",
]
