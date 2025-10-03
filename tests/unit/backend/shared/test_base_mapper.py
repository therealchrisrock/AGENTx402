"""Tests for base mapper."""

from datetime import datetime
from uuid import UUID, uuid4

import pytest
from pydantic import BaseModel as PydanticModel
from sqlalchemy.orm import Mapped, mapped_column

from src.backend.shared.infrastructure.persistence import BaseMapper, BaseModel


# Test fixtures
class TestEntity(PydanticModel):
    """Test domain entity."""

    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TestOrmModel(BaseModel):
    """Test ORM model."""

    __tablename__ = "test_entities"

    name: Mapped[str] = mapped_column(nullable=False)


class TestMapper(BaseMapper[TestEntity, TestOrmModel]):
    """Test mapper implementation."""

    def to_domain(self, model: TestOrmModel) -> TestEntity:
        """Convert ORM to domain."""
        return TestEntity.model_validate(model)

    def to_orm(self, entity: TestEntity, model: TestOrmModel | None = None) -> TestOrmModel:
        """Convert domain to ORM."""
        if model is None:
            model = TestOrmModel(
                id=entity.id,
                name=entity.name,
                created_at=entity.created_at,
                updated_at=entity.updated_at,
            )
        else:
            model.name = entity.name
            model.updated_at = entity.updated_at

        return model


@pytest.fixture
def mapper() -> TestMapper:
    """Create test mapper."""
    return TestMapper()


@pytest.fixture
def test_entity() -> TestEntity:
    """Create test entity."""
    entity_id = uuid4()
    now = datetime.utcnow()
    return TestEntity(
        id=entity_id,
        name="Test Entity",
        created_at=now,
        updated_at=now,
    )


@pytest.fixture
def test_orm_model() -> TestOrmModel:
    """Create test ORM model."""
    entity_id = uuid4()
    now = datetime.utcnow()
    model = TestOrmModel(
        id=entity_id,
        name="Test Model",
        created_at=now,
        updated_at=now,
    )
    return model


def test_to_domain(mapper: TestMapper, test_orm_model: TestOrmModel) -> None:
    """Test converting ORM model to domain entity."""
    entity = mapper.to_domain(test_orm_model)

    assert entity.id == test_orm_model.id
    assert entity.name == test_orm_model.name
    assert entity.created_at == test_orm_model.created_at
    assert entity.updated_at == test_orm_model.updated_at


def test_to_orm_new_model(mapper: TestMapper, test_entity: TestEntity) -> None:
    """Test converting domain entity to new ORM model."""
    model = mapper.to_orm(test_entity)

    assert model.id == test_entity.id
    assert model.name == test_entity.name
    assert model.created_at == test_entity.created_at
    assert model.updated_at == test_entity.updated_at


def test_to_orm_update_existing(
    mapper: TestMapper, test_entity: TestEntity, test_orm_model: TestOrmModel
) -> None:
    """Test updating existing ORM model from domain entity."""
    test_entity.name = "Updated Name"
    model = mapper.to_orm(test_entity, test_orm_model)

    assert model is test_orm_model
    assert model.name == "Updated Name"


def test_to_domain_list(mapper: TestMapper) -> None:
    """Test converting list of ORM models to domain entities."""
    now = datetime.utcnow()
    models = [
        TestOrmModel(id=uuid4(), name="Model 1", created_at=now, updated_at=now),
        TestOrmModel(id=uuid4(), name="Model 2", created_at=now, updated_at=now),
        TestOrmModel(id=uuid4(), name="Model 3", created_at=now, updated_at=now),
    ]

    entities = mapper.to_domain_list(models)

    assert len(entities) == 3
    assert all(isinstance(e, TestEntity) for e in entities)
    assert entities[0].name == "Model 1"
    assert entities[1].name == "Model 2"
    assert entities[2].name == "Model 3"


def test_to_orm_list(mapper: TestMapper) -> None:
    """Test converting list of domain entities to ORM models."""
    entities = [
        TestEntity(
            id=uuid4(),
            name="Entity 1",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        ),
        TestEntity(
            id=uuid4(),
            name="Entity 2",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        ),
    ]

    models = mapper.to_orm_list(entities)

    assert len(models) == 2
    assert all(isinstance(m, TestOrmModel) for m in models)
    assert models[0].name == "Entity 1"
    assert models[1].name == "Entity 2"
