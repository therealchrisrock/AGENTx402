"""SQLAlchemy implementation of mandate repository."""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import delete as sql_delete
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.features.agents.domain.entities import Mandate
from src.backend.features.agents.domain.repositories import IMandateRepository
from src.backend.features.agents.infrastructure.models import MandateMapper, MandateORM


class SQLAlchemyMandateRepository(IMandateRepository):
    """SQLAlchemy implementation of mandate repository."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize repository.

        Args:
            session: SQLAlchemy async session
        """
        self.session = session
        self.mapper = MandateMapper()

    async def add(self, entity: Mandate) -> Mandate:
        """Add a new mandate.

        Args:
            entity: Mandate to add

        Returns:
            The added mandate
        """
        orm_model = self.mapper.to_orm(entity)
        self.session.add(orm_model)
        await self.session.flush()
        return entity

    async def get_by_id(self, entity_id: UUID) -> Optional[Mandate]:
        """Get mandate by ID.

        Args:
            entity_id: Mandate ID

        Returns:
            Mandate if found, None otherwise
        """
        result = await self.session.execute(
            select(MandateORM).where(MandateORM.id == entity_id)
        )
        orm_model = result.scalar_one_or_none()
        return self.mapper.to_domain(orm_model) if orm_model else None

    async def get_all(self) -> List[Mandate]:
        """Get all mandates.

        Returns:
            List of all mandates
        """
        result = await self.session.execute(select(MandateORM))
        orm_models = result.scalars().all()
        return self.mapper.to_domain_list(list(orm_models))

    async def update(self, entity: Mandate) -> Mandate:
        """Update an existing mandate.

        Args:
            entity: Mandate to update

        Returns:
            The updated mandate
        """
        result = await self.session.execute(
            select(MandateORM).where(MandateORM.id == entity.id)
        )
        orm_model = result.scalar_one_or_none()

        if orm_model:
            self.mapper.to_orm(entity, orm_model)
            await self.session.flush()

        return entity

    async def delete(self, entity_id: UUID) -> bool:
        """Delete a mandate.

        Args:
            entity_id: Mandate ID

        Returns:
            True if deleted, False otherwise
        """
        result = await self.session.execute(
            sql_delete(MandateORM).where(MandateORM.id == entity_id)
        )
        await self.session.flush()
        return result.rowcount > 0

    async def exists(self, entity_id: UUID) -> bool:
        """Check if mandate exists.

        Args:
            entity_id: Mandate ID

        Returns:
            True if exists, False otherwise
        """
        mandate = await self.get_by_id(entity_id)
        return mandate is not None

    async def get_by_user_id(self, user_id: UUID) -> List[Mandate]:
        """Get all mandates for a user.

        Args:
            user_id: User ID

        Returns:
            List of user's mandates
        """
        result = await self.session.execute(
            select(MandateORM).where(MandateORM.user_id == user_id)
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
            select(MandateORM).where(
                MandateORM.user_id == user_id,
                MandateORM.revoked == False,  # noqa: E712
                MandateORM.signature.isnot(None),
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
            select(MandateORM).where(
                MandateORM.user_id == user_id, MandateORM.nonce == nonce
            )
        )
        orm_model = result.scalar_one_or_none()
        return self.mapper.to_domain(orm_model) if orm_model else None
