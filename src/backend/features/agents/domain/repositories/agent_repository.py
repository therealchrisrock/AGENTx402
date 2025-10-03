"""Agent repository interface."""

from abc import abstractmethod
from typing import List, Optional
from uuid import UUID

from src.backend.shared.application.interfaces import IRepository
from ..entities import Agent, AgentStatus


class IAgentRepository(IRepository[Agent]):
    """Repository interface for Agent aggregate."""

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> List[Agent]:
        """Get all agents for a user.

        Args:
            user_id: User ID

        Returns:
            List of user's agents
        """
        pass

    @abstractmethod
    async def get_by_mandate_id(self, mandate_id: UUID) -> Optional[Agent]:
        """Get agent by mandate ID.

        Args:
            mandate_id: Mandate ID

        Returns:
            Agent if found, None otherwise
        """
        pass

    @abstractmethod
    async def get_by_status(self, status: AgentStatus) -> List[Agent]:
        """Get all agents with a specific status.

        Args:
            status: Agent status

        Returns:
            List of agents with the status
        """
        pass

    @abstractmethod
    async def get_active_agents(self, user_id: UUID) -> List[Agent]:
        """Get all active agents for a user.

        Args:
            user_id: User ID

        Returns:
            List of active agents
        """
        pass
