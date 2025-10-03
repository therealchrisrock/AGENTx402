"""Tests for domain event dispatcher."""

from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from src.backend.shared.domain.base import DomainEvent
from src.backend.shared.infrastructure.messaging import (
    DomainEventDispatcher,
    get_event_dispatcher,
)


class TestEventA(DomainEvent):
    """Test event A."""

    data_a: str


class TestEventB(DomainEvent):
    """Test event B."""

    data_b: int


@pytest.fixture
def dispatcher() -> DomainEventDispatcher:
    """Create fresh dispatcher."""
    disp = DomainEventDispatcher()
    return disp


def test_register_handler(dispatcher: DomainEventDispatcher) -> None:
    """Test registering event handler."""
    handler = MagicMock()
    handler.__name__ = "test_handler"

    dispatcher.register(TestEventA, handler)

    assert TestEventA in dispatcher._handlers
    assert handler in dispatcher._handlers[TestEventA]


def test_dispatch_event(dispatcher: DomainEventDispatcher) -> None:
    """Test dispatching event to handler."""
    handler = MagicMock()
    handler.__name__ = "test_handler"
    dispatcher.register(TestEventA, handler)

    event = TestEventA(aggregate_id=uuid4(), event_type="TestEventA", data_a="test")
    dispatcher.dispatch(event)

    handler.assert_called_once_with(event)


def test_dispatch_to_multiple_handlers(dispatcher: DomainEventDispatcher) -> None:
    """Test dispatching event to multiple handlers."""
    handler1 = MagicMock()
    handler1.__name__ = "test_handler1"
    handler2 = MagicMock()
    handler2.__name__ = "test_handler2"

    dispatcher.register(TestEventA, handler1)
    dispatcher.register(TestEventA, handler2)

    event = TestEventA(aggregate_id=uuid4(), event_type="TestEventA", data_a="test")
    dispatcher.dispatch(event)

    handler1.assert_called_once_with(event)
    handler2.assert_called_once_with(event)


def test_dispatch_only_to_matching_handlers(dispatcher: DomainEventDispatcher) -> None:
    """Test event only dispatched to handlers for that event type."""
    handler_a = MagicMock()
    handler_a.__name__ = "handler_a"
    handler_b = MagicMock()
    handler_b.__name__ = "handler_b"

    dispatcher.register(TestEventA, handler_a)
    dispatcher.register(TestEventB, handler_b)

    event_a = TestEventA(aggregate_id=uuid4(), event_type="TestEventA", data_a="test")
    dispatcher.dispatch(event_a)

    handler_a.assert_called_once_with(event_a)
    handler_b.assert_not_called()


def test_dispatch_no_handlers(dispatcher: DomainEventDispatcher) -> None:
    """Test dispatching event with no registered handlers."""
    event = TestEventA(aggregate_id=uuid4(), event_type="TestEventA", data_a="test")

    # Should not raise exception
    dispatcher.dispatch(event)


def test_dispatch_handler_exception(dispatcher: DomainEventDispatcher) -> None:
    """Test handler exception doesn't stop other handlers."""
    handler1 = MagicMock(side_effect=Exception("Handler error"))
    handler1.__name__ = "handler1"
    handler2 = MagicMock()
    handler2.__name__ = "handler2"

    dispatcher.register(TestEventA, handler1)
    dispatcher.register(TestEventA, handler2)

    event = TestEventA(aggregate_id=uuid4(), event_type="TestEventA", data_a="test")
    dispatcher.dispatch(event)

    # Both handlers should be called despite first one failing
    handler1.assert_called_once()
    handler2.assert_called_once()


def test_dispatch_all(dispatcher: DomainEventDispatcher) -> None:
    """Test dispatching multiple events."""
    handler_a = MagicMock()
    handler_a.__name__ = "handler_a"
    handler_b = MagicMock()
    handler_b.__name__ = "handler_b"

    dispatcher.register(TestEventA, handler_a)
    dispatcher.register(TestEventB, handler_b)

    events = [
        TestEventA(aggregate_id=uuid4(), event_type="TestEventA", data_a="test"),
        TestEventB(aggregate_id=uuid4(), event_type="TestEventB", data_b=42),
    ]

    dispatcher.dispatch_all(events)

    handler_a.assert_called_once()
    handler_b.assert_called_once()


def test_clear_handlers(dispatcher: DomainEventDispatcher) -> None:
    """Test clearing all handlers."""
    handler = MagicMock()
    handler.__name__ = "test_handler"
    dispatcher.register(TestEventA, handler)

    dispatcher.clear_handlers()

    assert len(dispatcher._handlers) == 0


def test_get_event_dispatcher() -> None:
    """Test getting global dispatcher instance."""
    dispatcher1 = get_event_dispatcher()
    dispatcher2 = get_event_dispatcher()

    # Should return same instance
    assert dispatcher1 is dispatcher2
