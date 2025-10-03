"""Agent ORM model."""

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.backend.shared.infrastructure.persistence import BaseModel


class AgentORM(BaseModel):
    """SQLAlchemy ORM model for Agent aggregate.

    Stores agent data with relationships to mandates.
    """

    __tablename__ = "agents"

    mandate_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("mandates.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    strategy_type: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    # Metrics
    total_trades: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_volume: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Configuration stored as JSON
    configuration: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    def __repr__(self) -> str:
        """String representation."""
        return f"<AgentORM(id={self.id}, status={self.status}, total_trades={self.total_trades})>"
