"""Sign mandate command and handler."""

from dataclasses import dataclass
from uuid import UUID

from src.backend.features.agents.domain.entities import Mandate
from src.backend.features.agents.domain.repositories import IMandateRepository
from src.backend.shared.domain.exceptions import EntityNotFoundError


@dataclass(frozen=True)
class SignMandateCommand:
    """Command to sign a mandate."""

    mandate_id: UUID
    signature: str


class SignMandateCommandHandler:
    """Handler for SignMandateCommand."""

    def __init__(self, mandate_repository: IMandateRepository) -> None:
        """Initialize handler.

        Args:
            mandate_repository: Mandate repository
        """
        self.mandate_repository = mandate_repository

    async def handle(self, command: SignMandateCommand) -> Mandate:
        """Handle the command.

        Args:
            command: Sign mandate command

        Returns:
            Signed mandate

        Raises:
            EntityNotFoundError: If mandate not found
            ValueError: If mandate is already signed or revoked
        """
        # Get mandate
        mandate = await self.mandate_repository.get_by_id(command.mandate_id)
        if not mandate:
            raise EntityNotFoundError("Mandate", command.mandate_id)

        # Sign mandate
        mandate.sign(command.signature)

        # Update mandate
        return await self.mandate_repository.update(mandate)
