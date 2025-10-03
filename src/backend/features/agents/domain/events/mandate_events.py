"""Mandate domain events."""

from uuid import UUID

from src.backend.shared.domain.base import DomainEvent


class MandateCreated(DomainEvent):
    """Event raised when a mandate is created."""

    mandate_id: UUID
    user_id: UUID
    user_address: str


class MandateSigned(DomainEvent):
    """Event raised when a mandate is signed."""

    mandate_id: UUID
    user_id: UUID
    signature: str


class MandateRevoked(DomainEvent):
    """Event raised when a mandate is revoked."""

    mandate_id: UUID
    user_id: UUID
