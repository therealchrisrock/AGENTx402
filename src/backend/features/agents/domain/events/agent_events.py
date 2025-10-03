"""Agent domain events."""

from uuid import UUID

from src.backend.shared.domain.base import DomainEvent


class AgentCreated(DomainEvent):
    """Event raised when an agent is created."""

    agent_id: UUID
    user_id: UUID
    mandate_id: UUID
    strategy_type: str


class AgentActivated(DomainEvent):
    """Event raised when an agent is activated."""

    agent_id: UUID
    user_id: UUID
    mandate_id: UUID


class AgentDeactivated(DomainEvent):
    """Event raised when an agent is deactivated."""

    agent_id: UUID
    user_id: UUID
    mandate_id: UUID


class TradeExecuted(DomainEvent):
    """Event raised when a trade is executed."""

    agent_id: UUID
    user_id: UUID
    mandate_id: UUID
    amount: int
    protocol: str
    transaction_hash: str
