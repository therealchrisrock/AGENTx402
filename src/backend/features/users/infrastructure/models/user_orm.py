"""User ORM model."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Enum,
    Float,
    String,
    UniqueConstraint,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID

from src.backend.shared.infrastructure.persistence import BaseModel
from src.backend.features.users.domain.value_objects import UserState


class UserORM(BaseModel):
    """User ORM model for database persistence."""

    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("telegram_id", name="uq_users_telegram_id"),
        UniqueConstraint("wallet_address", name="uq_users_wallet_address"),
        Index("ix_users_telegram_id", "telegram_id"),
        Index("ix_users_wallet_address", "wallet_address"),
        Index("ix_users_state", "state"),
    )

    # Telegram identity
    telegram_id = Column(BigInteger, nullable=False, unique=True)
    telegram_username = Column(String(255), nullable=True)

    # Wallet information
    wallet_address = Column(String(42), nullable=True, unique=True)
    wallet_type = Column(String(50), nullable=True)  # metamask, walletconnect, phantom, manual
    balance = Column(Float, default=0.0, nullable=False)

    # User state
    state = Column(
        Enum(UserState, name="user_state_enum"),
        default=UserState.NEW,
        nullable=False
    )

    # Tracking fields
    onboarding_completed_at = Column(DateTime(timezone=True), nullable=True)
    first_mandate_id = Column(PostgresUUID(as_uuid=True), nullable=True)

    def __repr__(self) -> str:
        """String representation.

        Returns:
            String representation of user
        """
        return (
            f"<UserORM(id={self.id}, "
            f"telegram_id={self.telegram_id}, "
            f"state={self.state}, "
            f"wallet={self.wallet_address[:10] if self.wallet_address else 'None'})>"
        )