"""Base ORM model for SQLAlchemy."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models.

    Provides common fields:
    - id: UUID primary key
    - created_at: Timestamp of creation
    - updated_at: Timestamp of last update
    """

    __abstract__ = True

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        """String representation."""
        return f"<{self.__class__.__name__}(id={self.id})>"
