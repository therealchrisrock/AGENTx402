"""Mandate intent value object."""

from datetime import datetime
from enum import Enum

from pydantic import field_validator

from src.backend.shared.domain.base import ValueObject


class RiskTolerance(str, Enum):
    """Risk tolerance levels."""

    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"


class MandateIntent(ValueObject):
    """Value object representing user's investment intent."""

    max_spend: int
    valid_until: datetime
    risk_tolerance: RiskTolerance
    strategy_type: str

    @field_validator("max_spend")
    @classmethod
    def validate_max_spend(cls, v: int) -> int:
        """Validate max spend is positive.

        Args:
            v: Max spend value

        Returns:
            Validated max spend

        Raises:
            ValueError: If max spend is not positive
        """
        if v <= 0:
            raise ValueError("max_spend must be greater than 0")
        return v

    @field_validator("valid_until")
    @classmethod
    def validate_future_date(cls, v: datetime) -> datetime:
        """Validate valid_until is in the future.

        Args:
            v: Valid until datetime

        Returns:
            Validated datetime

        Raises:
            ValueError: If datetime is not in the future
        """
        if v <= datetime.utcnow():
            raise ValueError("valid_until must be in the future")
        return v

    def is_valid(self) -> bool:
        """Check if mandate is still valid.

        Returns:
            True if valid, False otherwise
        """
        return datetime.utcnow() < self.valid_until
