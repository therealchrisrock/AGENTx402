"""Mandate ORM model."""

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.backend.shared.infrastructure.persistence import BaseModel


class MandateORM(BaseModel):
    """SQLAlchemy ORM model for Mandate aggregate.

    Stores mandate data with JSON columns for value objects.
    """

    __tablename__ = "mandates"

    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    user_address: Mapped[str] = mapped_column(String(42), nullable=False)

    # Value objects stored as JSON
    intent_data: Mapped[dict] = mapped_column(JSON, nullable=False)
    constraints_data: Mapped[dict] = mapped_column(JSON, nullable=False)

    signature: Mapped[str | None] = mapped_column(String, nullable=True)
    nonce: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    def __repr__(self) -> str:
        """String representation."""
        return f"<MandateORM(id={self.id}, user_id={self.user_id}, revoked={self.revoked})>"
