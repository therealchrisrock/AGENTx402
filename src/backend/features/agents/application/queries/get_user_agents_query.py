"""Get user agents query and handler."""

from dataclasses import dataclass
from typing import List
from uuid import UUID

from src.backend.features.agents.domain.entities import Agent
from src.backend.features.agents.domain.repositories import IAgentRepository


@dataclass(frozen=True)
class GetUserAgentsQuery:
    """Query to get all agents for a user."""

    user_id: UUID
    active_only: bool = False


class GetUserAgentsQueryHandler:
    """Handler for GetUserAgentsQuery."""

    def __init__(self, agent_repository: IAgentRepository) -> None:
        """Initialize handler.

        Args:
            agent_repository: Agent repository
        """
        self.agent_repository = agent_repository

    async def handle(self, query: GetUserAgentsQuery) -> List[Agent]:
        """Handle the query.

        Args:
            query: Get user agents query

        Returns:
            List of user's agents
        """
        if query.active_only:
            return await self.agent_repository.get_active_agents(query.user_id)
        return await self.agent_repository.get_by_user_id(query.user_id)
