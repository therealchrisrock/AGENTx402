"""SQLAlchemy implementation of agent repository."""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import delete as sql_delete
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.features.agents.domain.entities import Agent, AgentStatus
from src.backend.features.agents.domain.repositories import IAgentRepository
from src.backend.features.agents.infrastructure.models import AgentMapper, AgentORM


class SQLAlchemyAgentRepository(IAgentRepository):
    """SQLAlchemy implementation of agent repository."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize repository.

        Args:
            session: SQLAlchemy async session
        """
        self.session = session
        self.mapper = AgentMapper()

    async def add(self, entity: Agent) -> Agent:
        """Add a new agent.

        Args:
            entity: Agent to add

        Returns:
            The added agent
        """
        orm_model = self.mapper.to_orm(entity)
        self.session.add(orm_model)
        await self.session.flush()
        return entity

    async def get_by_id(self, entity_id: UUID) -> Optional[Agent]:
        """Get agent by ID.

        Args:
            entity_id: Agent ID

        Returns:
            Agent if found, None otherwise
        """
        result = await self.session.execute(select(AgentORM).where(AgentORM.id == entity_id))
        orm_model = result.scalar_one_or_none()
        return self.mapper.to_domain(orm_model) if orm_model else None

    async def get_all(self) -> List[Agent]:
        """Get all agents.

        Returns:
            List of all agents
        """
        result = await self.session.execute(select(AgentORM))
        orm_models = result.scalars().all()
        return self.mapper.to_domain_list(list(orm_models))

    async def update(self, entity: Agent) -> Agent:
        """Update an existing agent.

        Args:
            entity: Agent to update

        Returns:
            The updated agent
        """
        result = await self.session.execute(
            select(AgentORM).where(AgentORM.id == entity.id)
        )
        orm_model = result.scalar_one_or_none()

        if orm_model:
            self.mapper.to_orm(entity, orm_model)
            await self.session.flush()

        return entity

    async def delete(self, entity_id: UUID) -> bool:
        """Delete an agent.

        Args:
            entity_id: Agent ID

        Returns:
            True if deleted, False otherwise
        """
        result = await self.session.execute(
            sql_delete(AgentORM).where(AgentORM.id == entity_id)
        )
        await self.session.flush()
        return result.rowcount > 0

    async def exists(self, entity_id: UUID) -> bool:
        """Check if agent exists.

        Args:
            entity_id: Agent ID

        Returns:
            True if exists, False otherwise
        """
        agent = await self.get_by_id(entity_id)
        return agent is not None

    async def get_by_user_id(self, user_id: UUID) -> List[Agent]:
        """Get all agents for a user.

        Args:
            user_id: User ID

        Returns:
            List of user's agents
        """
        result = await self.session.execute(
            select(AgentORM).where(AgentORM.user_id == user_id)
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
            select(AgentORM).where(AgentORM.mandate_id == mandate_id)
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
            select(AgentORM).where(AgentORM.status == status.value)
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
            select(AgentORM).where(
                AgentORM.user_id == user_id, AgentORM.status == AgentStatus.ACTIVE.value
            )
        )
        orm_models = result.scalars().all()
        return self.mapper.to_domain_list(list(orm_models))
