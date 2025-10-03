"""Base mapper for entity-model conversion."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel as PydanticModel
from sqlalchemy.orm import DeclarativeBase

TEntity = TypeVar("TEntity", bound=PydanticModel)
TModel = TypeVar("TModel", bound=DeclarativeBase)


class BaseMapper(ABC, Generic[TEntity, TModel]):
    """Base mapper for converting between domain entities and ORM models.

    This mapper handles the transformation between:
    - Domain entities (Pydantic models with business logic)
    - ORM models (SQLAlchemy models for persistence)

    Subclasses must implement:
    - to_domain(): Convert ORM model to domain entity
    - to_orm(): Convert domain entity to ORM model
    """

    @abstractmethod
    def to_domain(self, model: TModel) -> TEntity:
        """Convert ORM model to domain entity.

        Args:
            model: SQLAlchemy ORM model

        Returns:
            Domain entity
        """
        pass

    @abstractmethod
    def to_orm(self, entity: TEntity, model: TModel | None = None) -> TModel:
        """Convert domain entity to ORM model.

        Args:
            entity: Domain entity
            model: Existing ORM model to update (optional)

        Returns:
            SQLAlchemy ORM model
        """
        pass

    def to_domain_list(self, models: list[TModel]) -> list[TEntity]:
        """Convert list of ORM models to domain entities.

        Args:
            models: List of SQLAlchemy ORM models

        Returns:
            List of domain entities
        """
        return [self.to_domain(model) for model in models]

    def to_orm_list(self, entities: list[TEntity]) -> list[TModel]:
        """Convert list of domain entities to ORM models.

        Args:
            entities: List of domain entities

        Returns:
            List of SQLAlchemy ORM models
        """
        return [self.to_orm(entity) for entity in entities]
