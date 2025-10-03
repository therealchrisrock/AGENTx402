"""Create agent command and handler."""

from dataclasses import dataclass
from uuid import UUID

from src.backend.features.agents.domain.entities import Agent
from src.backend.features.agents.domain.repositories import IAgentRepository, IMandateRepository
from src.backend.shared.domain.exceptions import EntityNotFoundError


@dataclass(frozen=True)
class CreateAgentCommand:
    """Command to create a new agent."""

    mandate_id: UUID
    user_id: UUID
    strategy_type: str
    configuration: dict | None = None


class CreateAgentCommandHandler:
    """Handler for CreateAgentCommand."""

    def __init__(
        self,
        agent_repository: IAgentRepository,
        mandate_repository: IMandateRepository,
    ) -> None:
        """Initialize handler.

        Args:
            agent_repository: Agent repository
            mandate_repository: Mandate repository
        """
        self.agent_repository = agent_repository
        self.mandate_repository = mandate_repository

    async def handle(self, command: CreateAgentCommand) -> Agent:
        """Handle the command.

        Args:
            command: Create agent command

        Returns:
            Created agent

        Raises:
            EntityNotFoundError: If mandate not found
            ValueError: If mandate is not valid or agent already exists
        """
        # Verify mandate exists and is valid
        mandate = await self.mandate_repository.get_by_id(command.mandate_id)
        if not mandate:
            raise EntityNotFoundError("Mandate", command.mandate_id)

        if not mandate.is_valid():
            raise ValueError("Mandate is not valid")

        # Check if agent already exists for this mandate
        existing = await self.agent_repository.get_by_mandate_id(command.mandate_id)
        if existing:
            raise ValueError(f"Agent already exists for mandate {command.mandate_id}")

        # Create agent
        agent = Agent.create(
            mandate_id=command.mandate_id,
            user_id=command.user_id,
            strategy_type=command.strategy_type,
            configuration=command.configuration,
        )

        # Persist agent
        return await self.agent_repository.add(agent)
