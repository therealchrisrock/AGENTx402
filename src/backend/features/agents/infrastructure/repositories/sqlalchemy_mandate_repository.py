"""SQLAlchemy implementation of mandate repository."""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.features.agents.domain.entities import Mandate
from src.backend.features.agents.domain.repositories import IMandateRepository
from src.backend.features.agents.infrastructure.models import MandateMapper, MandateORM
from src.backend.shared.infrastructure.persistence import SQLAlchemyRepository


class SQLAlchemyMandateRepository(
    SQLAlchemyRepository[Mandate, MandateORM], IMandateRepository
):
    """SQLAlchemy implementation of mandate repository.

    Inherits common CRUD operations from SQLAlchemyRepository.
    Adds domain-specific query methods for mandates.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialize repository.

        Args:
            session: SQLAlchemy async session
        """
        super().__init__(
            session=session, model_class=MandateORM, mapper=MandateMapper()
        )

    # Domain-specific queries below

    async def get_by_user_id(self, user_id: UUID) -> List[Mandate]:
        """Get all mandates for a user.

        Args:
            user_id: User ID

        Returns:
            List of user's mandates
        """
        result = await self.session.execute(
            select(self.model_class).where(self.model_class.user_id == user_id)
        )
        orm_models = result.scalars().all()
        return self.mapper.to_domain_list(list(orm_models))

    async def get_active_mandates(self, user_id: UUID) -> List[Mandate]:
        """Get all active (non-revoked, valid) mandates for a user.

        Args:
            user_id: User ID

        Returns:
            List of active mandates
        """
        result = await self.session.execute(
            select(self.model_class).where(
                self.model_class.user_id == user_id,
                self.model_class.revoked == False,  # noqa: E712
                self.model_class.signature.isnot(None),
            )
        )
        orm_models = result.scalars().all()
        return self.mapper.to_domain_list(list(orm_models))

    async def get_by_nonce(self, user_id: UUID, nonce: int) -> Optional[Mandate]:
        """Get mandate by user ID and nonce.

        Args:
            user_id: User ID
            nonce: Mandate nonce

        Returns:
            Mandate if found, None otherwise
        """
        result = await self.session.execute(
            select(self.model_class).where(
                self.model_class.user_id == user_id, self.model_class.nonce == nonce
            )
        )
        orm_model = result.scalar_one_or_none()
        return self.mapper.to_domain(orm_model) if orm_model else None
