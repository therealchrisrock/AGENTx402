"""Generic SQLAlchemy repository implementation."""

from typing import Generic, List, Optional, TypeVar
from uuid import UUID

from sqlalchemy import delete as sql_delete
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.shared.application.interfaces import IRepository
from src.backend.shared.domain.base import Entity

from .base_mapper import BaseMapper, TEntity, TModel

TEntityVar = TypeVar("TEntityVar", bound=Entity)


class SQLAlchemyRepository(Generic[TEntity, TModel], IRepository[TEntity]):
    """Generic SQLAlchemy repository implementation.

    Provides common CRUD operations for any entity-ORM model pair.
    Concrete repositories can extend this and add domain-specific queries.

    Type Parameters:
        TEntity: Domain entity type (e.g., Mandate, Agent)
        TModel: SQLAlchemy ORM model type (e.g., MandateORM, AgentORM)

    Example:
        ```python
        class SQLAlchemyMandateRepository(
            SQLAlchemyRepository[Mandate, MandateORM],
            IMandateRepository
        ):
            def __init__(self, session: AsyncSession):
                super().__init__(
                    session=session,
                    model_class=MandateORM,
                    mapper=MandateMapper()
                )

            # Add domain-specific methods
            async def get_by_nonce(self, user_id: UUID, nonce: int) -> Optional[Mandate]:
                result = await self.session.execute(
                    select(self.model_class).where(
                        self.model_class.user_id == user_id,
                        self.model_class.nonce == nonce
                    )
                )
                orm_model = result.scalar_one_or_none()
                return self.mapper.to_domain(orm_model) if orm_model else None
        ```
    """

    def __init__(
        self,
        session: AsyncSession,
        model_class: type[TModel],
        mapper: BaseMapper[TEntity, TModel],
    ) -> None:
        """Initialize repository.

        Args:
            session: SQLAlchemy async session
            model_class: ORM model class (e.g., MandateORM)
            mapper: Mapper instance for entity-model conversion
        """
        self.session = session
        self.model_class = model_class
        self.mapper = mapper

    async def add(self, entity: TEntity) -> TEntity:
        """Add a new entity.

        Args:
            entity: Entity to add

        Returns:
            The added entity
        """
        orm_model = self.mapper.to_orm(entity)
        self.session.add(orm_model)
        await self.session.flush()
        return entity

    async def get_by_id(self, entity_id: UUID) -> Optional[TEntity]:
        """Get entity by ID.

        Args:
            entity_id: Entity ID

        Returns:
            Entity if found, None otherwise
        """
        result = await self.session.execute(
            select(self.model_class).where(self.model_class.id == entity_id)
        )
        orm_model = result.scalar_one_or_none()
        return self.mapper.to_domain(orm_model) if orm_model else None

    async def get_all(self) -> List[TEntity]:
        """Get all entities.

        Returns:
            List of all entities
        """
        result = await self.session.execute(select(self.model_class))
        orm_models = result.scalars().all()
        return self.mapper.to_domain_list(list(orm_models))

    async def update(self, entity: TEntity) -> TEntity:
        """Update an existing entity.

        Args:
            entity: Entity to update

        Returns:
            The updated entity
        """
        result = await self.session.execute(
            select(self.model_class).where(self.model_class.id == entity.id)
        )
        orm_model = result.scalar_one_or_none()

        if orm_model:
            self.mapper.to_orm(entity, orm_model)
            await self.session.flush()

        return entity

    async def delete(self, entity_id: UUID) -> bool:
        """Delete an entity.

        Args:
            entity_id: Entity ID

        Returns:
            True if deleted, False otherwise
        """
        result = await self.session.execute(
            sql_delete(self.model_class).where(self.model_class.id == entity_id)
        )
        await self.session.flush()
        return result.rowcount > 0

    async def exists(self, entity_id: UUID) -> bool:
        """Check if entity exists.

        Args:
            entity_id: Entity ID

        Returns:
            True if exists, False otherwise
        """
        entity = await self.get_by_id(entity_id)
        return entity is not None
