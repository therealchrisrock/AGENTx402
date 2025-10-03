"""Create mandate command and handler."""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.backend.features.agents.domain.entities import Mandate
from src.backend.features.agents.domain.repositories import IMandateRepository
from src.backend.features.agents.domain.value_objects import (
    MandateConstraints,
    MandateIntent,
    RiskTolerance,
)


@dataclass(frozen=True)
class CreateMandateCommand:
    """Command to create a new mandate."""

    user_id: UUID
    user_address: str
    max_spend: int
    valid_until: datetime
    risk_tolerance: RiskTolerance
    strategy_type: str
    per_transaction_max: int
    daily_limit: int | None
    allowed_protocols: list[str]
    nonce: int


class CreateMandateCommandHandler:
    """Handler for CreateMandateCommand."""

    def __init__(self, mandate_repository: IMandateRepository) -> None:
        """Initialize handler.

        Args:
            mandate_repository: Mandate repository
        """
        self.mandate_repository = mandate_repository

    async def handle(self, command: CreateMandateCommand) -> Mandate:
        """Handle the command.

        Args:
            command: Create mandate command

        Returns:
            Created mandate

        Raises:
            ValueError: If mandate with same nonce already exists
        """
        # Check if mandate with same nonce exists
        existing = await self.mandate_repository.get_by_nonce(
            command.user_id, command.nonce
        )
        if existing:
            raise ValueError(f"Mandate with nonce {command.nonce} already exists")

        # Create value objects
        intent = MandateIntent(
            max_spend=command.max_spend,
            valid_until=command.valid_until,
            risk_tolerance=command.risk_tolerance,
            strategy_type=command.strategy_type,
        )

        constraints = MandateConstraints(
            per_transaction_max=command.per_transaction_max,
            daily_limit=command.daily_limit,
            allowed_protocols=command.allowed_protocols,
        )

        # Create mandate
        mandate = Mandate.create(
            user_id=command.user_id,
            user_address=command.user_address,
            intent=intent,
            constraints=constraints,
            nonce=command.nonce,
        )

        # Persist mandate
        return await self.mandate_repository.add(mandate)
