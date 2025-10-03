"""Tests for Unit of Work."""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.shared.domain.base import AggregateRoot, DomainEvent
from src.backend.shared.infrastructure.persistence import SQLAlchemyUnitOfWork


class TestEvent(DomainEvent):
    """Test domain event."""

    test_data: str


class TestAggregate(AggregateRoot):
    """Test aggregate root."""

    name: str


@pytest.fixture
def mock_session() -> AsyncSession:
    """Create mock async session."""
    session = MagicMock(spec=AsyncSession)
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.identity_map = {}
    return session


@pytest.fixture
def uow(mock_session: AsyncSession) -> SQLAlchemyUnitOfWork:
    """Create unit of work."""
    return SQLAlchemyUnitOfWork(mock_session)


@pytest.mark.anyio
async def test_commit(uow: SQLAlchemyUnitOfWork) -> None:
    """Test commit transaction."""
    await uow.commit()

    uow.session.commit.assert_called_once()


@pytest.mark.anyio
async def test_rollback(uow: SQLAlchemyUnitOfWork) -> None:
    """Test rollback transaction."""
    await uow.rollback()

    uow.session.rollback.assert_called_once()


@pytest.mark.anyio
async def test_rollback_clears_events(uow: SQLAlchemyUnitOfWork) -> None:
    """Test rollback clears domain events."""
    # Add some events
    uow._domain_events = [
        TestEvent(aggregate_id=uuid4(), event_type="TestEvent", test_data="data")
    ]

    await uow.rollback()

    assert len(uow._domain_events) == 0


@pytest.mark.anyio
async def test_collect_events_from_aggregates(mock_session: AsyncSession) -> None:
    """Test collecting domain events from aggregate roots."""
    # Create aggregate with events
    aggregate = TestAggregate(name="Test")
    event = TestEvent(
        aggregate_id=aggregate.id,
        event_type="TestEvent",
        test_data="test data",
    )
    aggregate.add_domain_event(event)

    # Add to session identity map
    mock_session.identity_map = {aggregate.id: aggregate}

    uow = SQLAlchemyUnitOfWork(mock_session)
    await uow.commit()

    # Check events were collected
    events = uow.collect_events()
    assert len(events) == 1
    assert events[0] == event

    # Check aggregate events were cleared
    assert len(aggregate.get_domain_events()) == 0


@pytest.mark.anyio
async def test_context_manager_success(mock_session: AsyncSession) -> None:
    """Test context manager on success."""
    async with SQLAlchemyUnitOfWork(mock_session) as uow:
        assert uow.session == mock_session

    # Session should not be rolled back on success
    mock_session.rollback.assert_not_called()


@pytest.mark.anyio
async def test_context_manager_exception(mock_session: AsyncSession) -> None:
    """Test context manager on exception."""
    try:
        async with SQLAlchemyUnitOfWork(mock_session):
            raise ValueError("Test error")
    except ValueError:
        pass

    # Session should be rolled back on exception
    mock_session.rollback.assert_called_once()


def test_collect_events_returns_copy(uow: SQLAlchemyUnitOfWork) -> None:
    """Test collect_events returns a copy."""
    event = TestEvent(aggregate_id=uuid4(), event_type="TestEvent", test_data="data")
    uow._domain_events = [event]

    events = uow.collect_events()
    events.append(
        TestEvent(aggregate_id=uuid4(), event_type="TestEvent", test_data="more data")
    )

    # Original list should not be modified
    assert len(uow._domain_events) == 1


def test_clear_events(uow: SQLAlchemyUnitOfWork) -> None:
    """Test clearing events."""
    uow._domain_events = [
        TestEvent(aggregate_id=uuid4(), event_type="TestEvent", test_data="data")
    ]

    uow.clear_events()

    assert len(uow._domain_events) == 0
