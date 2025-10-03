"""Get mandate query and handler."""

from dataclasses import dataclass
from uuid import UUID

from src.backend.features.agents.domain.entities import Mandate
from src.backend.features.agents.domain.repositories import IMandateRepository
from src.backend.shared.domain.exceptions import EntityNotFoundError


@dataclass(frozen=True)
class GetMandateQuery:
    """Query to get a mandate by ID."""

    mandate_id: UUID


class GetMandateQueryHandler:
    """Handler for GetMandateQuery."""

    def __init__(self, mandate_repository: IMandateRepository) -> None:
        """Initialize handler.

        Args:
            mandate_repository: Mandate repository
        """
        self.mandate_repository = mandate_repository

    async def handle(self, query: GetMandateQuery) -> Mandate:
        """Handle the query.

        Args:
            query: Get mandate query

        Returns:
            Mandate

        Raises:
            EntityNotFoundError: If mandate not found
        """
        mandate = await self.mandate_repository.get_by_id(query.mandate_id)
        if not mandate:
            raise EntityNotFoundError("Mandate", query.mandate_id)

        return mandate
