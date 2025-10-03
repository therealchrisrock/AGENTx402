"""Mandate entity."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import Field

from src.backend.shared.domain.base import AggregateRoot
from ..events.mandate_events import MandateCreated, MandateRevoked, MandateSigned
from ..value_objects import MandateConstraints, MandateIntent


class Mandate(AggregateRoot):
    """Mandate aggregate root.

    A mandate is a signed authorization from a user that allows
    an agent to execute trades on their behalf within specified constraints.
    """

    user_id: UUID
    intent: MandateIntent
    constraints: MandateConstraints
    signature: Optional[str] = None
    nonce: int
    revoked: bool = Field(default=False)
    user_address: str

    def sign(self, signature: str) -> None:
        """Sign the mandate.

        Args:
            signature: Cryptographic signature

        Raises:
            ValueError: If mandate is already signed or revoked
        """
        if self.signature:
            raise ValueError("Mandate is already signed")
        if self.revoked:
            raise ValueError("Cannot sign a revoked mandate")

        self.signature = signature
        self.updated_at = datetime.utcnow()
        self.add_domain_event(
            MandateSigned(
                aggregate_id=self.id,
                event_type="MandateSigned",
                mandate_id=self.id,
                user_id=self.user_id,
                signature=signature,
            )
        )

    def revoke(self) -> None:
        """Revoke the mandate.

        Raises:
            ValueError: If mandate is already revoked
        """
        if self.revoked:
            raise ValueError("Mandate is already revoked")

        self.revoked = True
        self.updated_at = datetime.utcnow()
        self.add_domain_event(
            MandateRevoked(
                aggregate_id=self.id,
                event_type="MandateRevoked",
                mandate_id=self.id,
                user_id=self.user_id,
            )
        )

    def is_valid(self) -> bool:
        """Check if mandate is valid.

        Returns:
            True if valid, False otherwise
        """
        return (
            not self.revoked
            and self.signature is not None
            and self.intent.is_valid()
        )

    def can_execute_trade(self, amount: int, protocol: str) -> bool:
        """Check if trade can be executed within mandate constraints.

        Args:
            amount: Trade amount
            protocol: Protocol name

        Returns:
            True if allowed, False otherwise
        """
        if not self.is_valid():
            return False

        return (
            self.constraints.is_transaction_allowed(amount)
            and self.constraints.is_protocol_allowed(protocol)
        )

    @classmethod
    def create(
        cls,
        user_id: UUID,
        user_address: str,
        intent: MandateIntent,
        constraints: MandateConstraints,
        nonce: int,
    ) -> "Mandate":
        """Create a new mandate.

        Args:
            user_id: User ID
            user_address: User wallet address
            intent: Mandate intent
            constraints: Mandate constraints
            nonce: Nonce for replay protection

        Returns:
            New mandate instance
        """
        mandate = cls(
            user_id=user_id,
            user_address=user_address,
            intent=intent,
            constraints=constraints,
            nonce=nonce,
        )

        mandate.add_domain_event(
            MandateCreated(
                aggregate_id=mandate.id,
                event_type="MandateCreated",
                mandate_id=mandate.id,
                user_id=user_id,
                user_address=user_address,
            )
        )

        return mandate
