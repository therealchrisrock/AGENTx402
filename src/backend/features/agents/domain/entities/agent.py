"""Agent entity."""

from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import Field

from src.backend.shared.domain.base import AggregateRoot
from ..events.agent_events import AgentActivated, AgentCreated, AgentDeactivated, TradeExecuted


class AgentStatus(str, Enum):
    """Agent status enum."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    PAUSED = "paused"


class Agent(AggregateRoot):
    """Agent aggregate root.

    An agent is an autonomous trading bot that executes trades
    on behalf of users within the constraints of their mandates.
    """

    mandate_id: UUID
    user_id: UUID
    strategy_type: str
    status: AgentStatus = Field(default=AgentStatus.INACTIVE)
    total_trades: int = Field(default=0)
    total_volume: int = Field(default=0)
    configuration: dict = Field(default_factory=dict)

    def activate(self) -> None:
        """Activate the agent.

        Raises:
            ValueError: If agent is already active
        """
        if self.status == AgentStatus.ACTIVE:
            raise ValueError("Agent is already active")

        self.status = AgentStatus.ACTIVE
        self.updated_at = datetime.utcnow()
        self.add_domain_event(
            AgentActivated(
                aggregate_id=self.id,
                event_type="AgentActivated",
                agent_id=self.id,
                user_id=self.user_id,
                mandate_id=self.mandate_id,
            )
        )

    def deactivate(self) -> None:
        """Deactivate the agent.

        Raises:
            ValueError: If agent is not active
        """
        if self.status != AgentStatus.ACTIVE:
            raise ValueError("Agent is not active")

        self.status = AgentStatus.INACTIVE
        self.updated_at = datetime.utcnow()
        self.add_domain_event(
            AgentDeactivated(
                aggregate_id=self.id,
                event_type="AgentDeactivated",
                agent_id=self.id,
                user_id=self.user_id,
                mandate_id=self.mandate_id,
            )
        )

    def record_trade(self, trade_amount: int, protocol: str, transaction_hash: str) -> None:
        """Record a trade execution.

        Args:
            trade_amount: Amount traded
            protocol: Protocol used
            transaction_hash: Blockchain transaction hash

        Raises:
            ValueError: If agent is not active
        """
        if self.status != AgentStatus.ACTIVE:
            raise ValueError("Cannot record trade for inactive agent")

        self.total_trades += 1
        self.total_volume += trade_amount
        self.updated_at = datetime.utcnow()

        self.add_domain_event(
            TradeExecuted(
                aggregate_id=self.id,
                event_type="TradeExecuted",
                agent_id=self.id,
                user_id=self.user_id,
                mandate_id=self.mandate_id,
                amount=trade_amount,
                protocol=protocol,
                transaction_hash=transaction_hash,
            )
        )

    def is_active(self) -> bool:
        """Check if agent is active.

        Returns:
            True if active, False otherwise
        """
        return self.status == AgentStatus.ACTIVE

    @classmethod
    def create(
        cls,
        mandate_id: UUID,
        user_id: UUID,
        strategy_type: str,
        configuration: Optional[dict] = None,
    ) -> "Agent":
        """Create a new agent.

        Args:
            mandate_id: Mandate ID
            user_id: User ID
            strategy_type: Trading strategy type
            configuration: Optional agent configuration

        Returns:
            New agent instance
        """
        agent = cls(
            mandate_id=mandate_id,
            user_id=user_id,
            strategy_type=strategy_type,
            configuration=configuration or {},
        )

        agent.add_domain_event(
            AgentCreated(
                aggregate_id=agent.id,
                event_type="AgentCreated",
                agent_id=agent.id,
                user_id=user_id,
                mandate_id=mandate_id,
                strategy_type=strategy_type,
            )
        )

        return agent
