"""Register user command and handler."""

import logging
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.features.users.domain.entities import User
from src.backend.features.users.infrastructure.repositories import SQLAlchemyUserRepository

logger = logging.getLogger(__name__)


class RegisterUserCommand(BaseModel):
    """Command to register a new user."""

    telegram_id: int = Field(..., description="Telegram user ID")
    telegram_username: Optional[str] = Field(None, description="Telegram username")


class RegisterUserResult(BaseModel):
    """Result of user registration."""

    success: bool
    user_id: Optional[UUID] = None
    message: str
    already_exists: bool = False


class RegisterUserCommandHandler:
    """Handler for RegisterUserCommand."""

    def __init__(self, session: AsyncSession):
        """Initialize handler with database session.

        Args:
            session: Database session
        """
        self.session = session
        self.repository = SQLAlchemyUserRepository(session)

    async def handle(self, command: RegisterUserCommand) -> RegisterUserResult:
        """Handle user registration command.

        Args:
            command: Registration command

        Returns:
            Registration result
        """
        try:
            # Check if user already exists
            existing_user = await self.repository.get_by_telegram_id(command.telegram_id)
            if existing_user:
                logger.info(f"User already exists for telegram_id: {command.telegram_id}")
                return RegisterUserResult(
                    success=False,
                    user_id=existing_user.id,
                    message="User already registered",
                    already_exists=True
                )

            # Create new user
            user = User.create(
                telegram_id=command.telegram_id,
                telegram_username=command.telegram_username
            )

            # Save to repository
            await self.repository.save(user)
            await self.session.commit()

            logger.info(f"Successfully registered user {user.id} for telegram_id: {command.telegram_id}")

            return RegisterUserResult(
                success=True,
                user_id=user.id,
                message="User registered successfully",
                already_exists=False
            )

        except Exception as e:
            logger.error(f"Failed to register user: {e}")
            await self.session.rollback()
            return RegisterUserResult(
                success=False,
                message=f"Registration failed: {str(e)}",
                already_exists=False
            )