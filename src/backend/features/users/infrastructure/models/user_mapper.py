"""User mapper for domain-ORM conversion."""

from typing import Optional

from src.backend.shared.infrastructure.persistence import BaseMapper
from src.backend.features.users.domain.entities import User
from src.backend.features.users.domain.value_objects import UserState
from .user_orm import UserORM


class UserMapper(BaseMapper[User, UserORM]):
    """Mapper for User domain entity and ORM model."""

    @staticmethod
    def to_orm(entity: User) -> UserORM:
        """Convert domain entity to ORM model.

        Args:
            entity: User domain entity

        Returns:
            UserORM model
        """
        return UserORM(
            id=entity.id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            telegram_id=entity.telegram_id,
            telegram_username=entity.telegram_username,
            state=entity.state,
            wallet_address=entity.wallet_address,
            wallet_type=entity.wallet_type,
            balance=entity.balance,
            onboarding_completed_at=entity.onboarding_completed_at,
            first_mandate_id=entity.first_mandate_id,
        )

    @staticmethod
    def to_entity(orm: UserORM) -> User:
        """Convert ORM model to domain entity.

        Args:
            orm: UserORM model

        Returns:
            User domain entity
        """
        user = User(
            id=orm.id,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
            telegram_id=orm.telegram_id,
            telegram_username=orm.telegram_username,
            state=orm.state,
            wallet_address=orm.wallet_address,
            wallet_type=orm.wallet_type,
            balance=orm.balance,
            onboarding_completed_at=orm.onboarding_completed_at,
            first_mandate_id=orm.first_mandate_id,
        )
        # Clear domain events after loading from DB
        user.clear_domain_events()
        return user

    @staticmethod
    def update_orm(orm: UserORM, entity: User) -> None:
        """Update ORM model with domain entity data.

        Args:
            orm: UserORM model to update
            entity: User domain entity with new data
        """
        orm.updated_at = entity.updated_at
        orm.telegram_username = entity.telegram_username
        orm.state = entity.state
        orm.wallet_address = entity.wallet_address
        orm.wallet_type = entity.wallet_type
        orm.balance = entity.balance
        orm.onboarding_completed_at = entity.onboarding_completed_at
        orm.first_mandate_id = entity.first_mandate_id