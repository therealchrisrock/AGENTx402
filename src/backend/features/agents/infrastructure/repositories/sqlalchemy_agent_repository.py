"""SQLAlchemy implementation of agent repository."""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.features.agents.domain.entities import Agent, AgentStatus
from src.backend.features.agents.domain.repositories import IAgentRepository
from src.backend.features.agents.infrastructure.models import AgentMapper, AgentORM
from src.backend.shared.infrastructure.persistence import SQLAlchemyRepository


class SQLAlchemyAgentRepository(
    SQLAlchemyRepository[Agent, AgentORM], IAgentRepository
):
    """SQLAlchemy implementation of agent repository.

    Inherits common CRUD operations from SQLAlchemyRepository.
    Adds domain-specific query methods for agents.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialize repository.

        Args:
            session: SQLAlchemy async session
        """
        super().__init__(
            session=session, model_class=AgentORM, mapper=AgentMapper()
        )

    # Domain-specific queries below

    async def get_by_user_id(self, user_id: UUID) -> List[Agent]:
        """Get all agents for a user.

        Args:
            user_id: User ID

        Returns:
            List of user's agents
        """
        result = await self.session.execute(
            select(self.model_class).where(self.model_class.user_id == user_id)
        )
        orm_models = result.scalars().all()
        return self.mapper.to_domain_list(list(orm_models))

    async def get_by_mandate_id(self, mandate_id: UUID) -> Optional[Agent]:
        """Get agent by mandate ID.

        Args:
            mandate_id: Mandate ID

        Returns:
            Agent if found, None otherwise
        """
        result = await self.session.execute(
            select(self.model_class).where(self.model_class.mandate_id == mandate_id)
        )
        orm_model = result.scalar_one_or_none()
        return self.mapper.to_domain(orm_model) if orm_model else None

    async def get_by_status(self, status: AgentStatus) -> List[Agent]:
        """Get all agents with a specific status.

        Args:
            status: Agent status

        Returns:
            List of agents with the status
        """
        result = await self.session.execute(
            select(self.model_class).where(self.model_class.status == status.value)
        )
        orm_models = result.scalars().all()
        return self.mapper.to_domain_list(list(orm_models))

    async def get_active_agents(self, user_id: UUID) -> List[Agent]:
        """Get all active agents for a user.

        Args:
            user_id: User ID

        Returns:
            List of active agents
        """
        result = await self.session.execute(
            select(self.model_class).where(
                self.model_class.user_id == user_id,
                self.model_class.status == AgentStatus.ACTIVE.value,
            )
        )
        orm_models = result.scalars().all()
        return self.mapper.to_domain_list(list(orm_models))
