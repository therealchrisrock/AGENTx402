"""Mandate constraints value object."""

from typing import List, Optional

from src.backend.shared.domain.base import ValueObject


class MandateConstraints(ValueObject):
    """Value object representing mandate spending constraints."""

    per_transaction_max: int
    daily_limit: Optional[int] = None
    allowed_protocols: List[str] = []

    def is_transaction_allowed(self, amount: int) -> bool:
        """Check if transaction amount is within constraints.

        Args:
            amount: Transaction amount

        Returns:
            True if allowed, False otherwise
        """
        return amount <= self.per_transaction_max

    def is_protocol_allowed(self, protocol: str) -> bool:
        """Check if protocol is allowed.

        Args:
            protocol: Protocol name

        Returns:
            True if allowed, False otherwise
        """
        if not self.allowed_protocols:
            return True  # Empty list means all protocols allowed
        return protocol in self.allowed_protocols
