"""User domain events."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import Field

from src.backend.shared.domain.base import DomainEvent


class UserRegistered(DomainEvent):
    """Event raised when a new user is registered."""

    user_id: UUID
    telegram_id: int
    telegram_username: Optional[str] = None


class WalletConnected(DomainEvent):
    """Event raised when user connects a wallet."""

    user_id: UUID
    wallet_address: str
    wallet_type: str = Field(default="manual")  # metamask, walletconnect, phantom, manual
    connected_at: datetime = Field(default_factory=datetime.utcnow)


class UserFunded(DomainEvent):
    """Event raised when user's wallet reaches minimum funding threshold."""

    user_id: UUID
    wallet_address: str
    balance: float
    funded_at: datetime = Field(default_factory=datetime.utcnow)


class UserBecameActiveTrader(DomainEvent):
    """Event raised when user creates their first mandate and becomes active trader."""

    user_id: UUID
    first_mandate_id: UUID
    activated_at: datetime = Field(default_factory=datetime.utcnow)