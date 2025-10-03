"""API routes for mandates."""

import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.features.agents.application.commands import (
    CreateMandateCommand,
    CreateMandateCommandHandler,
    SignMandateCommand,
    SignMandateCommandHandler,
)
from src.backend.features.agents.application.queries import (
    GetMandateQuery,
    GetMandateQueryHandler,
)
from src.backend.features.agents.domain.value_objects import RiskTolerance
from src.backend.features.agents.infrastructure.repositories import (
    SQLAlchemyMandateRepository,
)
from src.backend.features.agents.presentation.schemas import (
    CreateMandateRequest,
    MandateResponse,
    SignMandateRequest,
)
from src.backend.shared.infrastructure.database import DatabaseSessionManager

logger = logging.getLogger(__name__)

router = APIRouter()


# Dependency to get database session
async def get_db_session() -> AsyncSession:
    """Get database session dependency."""
    # TODO: Inject from app context
    raise NotImplementedError("Database session dependency not yet configured")


@router.post("/", response_model=MandateResponse, status_code=status.HTTP_201_CREATED)
async def create_mandate(
    request: CreateMandateRequest,
    db: AsyncSession = Depends(get_db_session),
) -> MandateResponse:
    """Create a new mandate.

    Args:
        request: Create mandate request
        db: Database session

    Returns:
        Created mandate

    Raises:
        HTTPException: If creation fails
    """
    try:
        # Create repository and handler
        repository = SQLAlchemyMandateRepository(db)
        handler = CreateMandateCommandHandler(repository)

        # Create command
        command = CreateMandateCommand(
            user_id=request.user_id,
            user_address=request.user_address,
            max_spend=request.intent.max_spend,
            valid_until=request.intent.valid_until,
            risk_tolerance=RiskTolerance(request.intent.risk_tolerance),
            strategy_type=request.intent.strategy_type,
            per_transaction_max=request.constraints.per_transaction_max,
            daily_limit=request.constraints.daily_limit,
            allowed_protocols=request.constraints.allowed_protocols,
            nonce=request.nonce,
        )

        # Execute command
        mandate = await handler.handle(command)

        # Map to response
        return MandateResponse(
            id=mandate.id,
            user_id=mandate.user_id,
            user_address=mandate.user_address,
            intent=request.intent,
            constraints=request.constraints,
            signature=mandate.signature,
            nonce=mandate.nonce,
            revoked=mandate.revoked,
            created_at=mandate.created_at,
            updated_at=mandate.updated_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating mandate: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
        )


@router.get("/{mandate_id}", response_model=MandateResponse)
async def get_mandate(
    mandate_id: UUID,
    db: AsyncSession = Depends(get_db_session),
) -> MandateResponse:
    """Get mandate by ID.

    Args:
        mandate_id: Mandate ID
        db: Database session

    Returns:
        Mandate

    Raises:
        HTTPException: If not found
    """
    try:
        repository = SQLAlchemyMandateRepository(db)
        handler = GetMandateQueryHandler(repository)

        query = GetMandateQuery(mandate_id=mandate_id)
        mandate = await handler.handle(query)

        # Map to response - simplified for scaffolding
        return MandateResponse(
            id=mandate.id,
            user_id=mandate.user_id,
            user_address=mandate.user_address,
            intent={
                "max_spend": mandate.intent.max_spend,
                "valid_until": mandate.intent.valid_until,
                "risk_tolerance": mandate.intent.risk_tolerance.value,
                "strategy_type": mandate.intent.strategy_type,
            },
            constraints={
                "per_transaction_max": mandate.constraints.per_transaction_max,
                "daily_limit": mandate.constraints.daily_limit,
                "allowed_protocols": mandate.constraints.allowed_protocols,
            },
            signature=mandate.signature,
            nonce=mandate.nonce,
            revoked=mandate.revoked,
            created_at=mandate.created_at,
            updated_at=mandate.updated_at,
        )
    except Exception as e:
        logger.error(f"Error getting mandate: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mandate not found")


@router.put("/{mandate_id}/signature", response_model=MandateResponse)
async def sign_mandate(
    mandate_id: UUID,
    request: SignMandateRequest,
    db: AsyncSession = Depends(get_db_session),
) -> MandateResponse:
    """Sign a mandate.

    Args:
        mandate_id: Mandate ID
        request: Sign request
        db: Database session

    Returns:
        Signed mandate

    Raises:
        HTTPException: If signing fails
    """
    try:
        repository = SQLAlchemyMandateRepository(db)
        handler = SignMandateCommandHandler(repository)

        command = SignMandateCommand(mandate_id=mandate_id, signature=request.signature)
        mandate = await handler.handle(command)

        # Map to response - simplified for scaffolding
        return MandateResponse(
            id=mandate.id,
            user_id=mandate.user_id,
            user_address=mandate.user_address,
            intent={
                "max_spend": mandate.intent.max_spend,
                "valid_until": mandate.intent.valid_until,
                "risk_tolerance": mandate.intent.risk_tolerance.value,
                "strategy_type": mandate.intent.strategy_type,
            },
            constraints={
                "per_transaction_max": mandate.constraints.per_transaction_max,
                "daily_limit": mandate.constraints.daily_limit,
                "allowed_protocols": mandate.constraints.allowed_protocols,
            },
            signature=mandate.signature,
            nonce=mandate.nonce,
            revoked=mandate.revoked,
            created_at=mandate.created_at,
            updated_at=mandate.updated_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error signing mandate: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
        )
