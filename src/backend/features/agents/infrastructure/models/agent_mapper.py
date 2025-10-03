"""Mapper for Agent domain entity to ORM model."""

from src.backend.features.agents.domain.entities import Agent, AgentStatus
from src.backend.shared.infrastructure.persistence import BaseMapper

from .agent_orm import AgentORM


class AgentMapper(BaseMapper[Agent, AgentORM]):
    """Mapper between Agent domain entity and AgentORM model."""

    def to_domain(self, model: AgentORM) -> Agent:
        """Convert ORM model to domain entity.

        Args:
            model: AgentORM instance

        Returns:
            Agent domain entity
        """
        agent = Agent(
            id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            mandate_id=model.mandate_id,
            user_id=model.user_id,
            strategy_type=model.strategy_type,
            status=AgentStatus(model.status),
            total_trades=model.total_trades,
            total_volume=model.total_volume,
            configuration=model.configuration,
        )

        return agent

    def to_orm(self, entity: Agent, model: AgentORM | None = None) -> AgentORM:
        """Convert domain entity to ORM model.

        Args:
            entity: Agent domain entity
            model: Existing AgentORM to update (optional)

        Returns:
            AgentORM instance
        """
        if model is None:
            # Create new ORM model
            model = AgentORM(
                id=entity.id,
                created_at=entity.created_at,
                updated_at=entity.updated_at,
                mandate_id=entity.mandate_id,
                user_id=entity.user_id,
                strategy_type=entity.strategy_type,
                status=entity.status.value,
                total_trades=entity.total_trades,
                total_volume=entity.total_volume,
                configuration=entity.configuration,
            )
        else:
            # Update existing model
            model.strategy_type = entity.strategy_type
            model.status = entity.status.value
            model.total_trades = entity.total_trades
            model.total_volume = entity.total_volume
            model.configuration = entity.configuration
            model.updated_at = entity.updated_at

        return model
