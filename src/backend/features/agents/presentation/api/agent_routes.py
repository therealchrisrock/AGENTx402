"""API routes for agents."""

import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.backend.features.agents.application.commands import (
    CreateAgentCommand,
    CreateAgentCommandHandler,
)
from src.backend.features.agents.application.queries import (
    GetUserAgentsQuery,
    GetUserAgentsQueryHandler,
)
from src.backend.features.agents.infrastructure.repositories import (
    SQLAlchemyAgentRepository,
    SQLAlchemyMandateRepository,
)
from src.backend.features.agents.presentation.schemas import (
    AgentListResponse,
    AgentResponse,
    CreateAgentRequest,
)

logger = logging.getLogger(__name__)

router = APIRouter()


# Dependency to get database session
from src.backend.core.dependencies import get_db as get_db_session


@router.post("/", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    request: CreateAgentRequest,
    db: AsyncSession = Depends(get_db_session),
) -> AgentResponse:
    """Create a new agent.

    Args:
        request: Create agent request
        db: Database session

    Returns:
        Created agent

    Raises:
        HTTPException: If creation fails
    """
    try:
        # Create repositories and handler
        agent_repo = SQLAlchemyAgentRepository(db)
        mandate_repo = SQLAlchemyMandateRepository(db)
        handler = CreateAgentCommandHandler(agent_repo, mandate_repo)

        # Create command
        command = CreateAgentCommand(
            mandate_id=request.mandate_id,
            user_id=request.user_id,
            strategy_type=request.strategy_type,
            configuration=request.configuration,
        )

        # Execute command
        agent = await handler.handle(command)

        # Map to response
        return AgentResponse(
            id=agent.id,
            mandate_id=agent.mandate_id,
            user_id=agent.user_id,
            strategy_type=agent.strategy_type,
            status=agent.status.value,
            total_trades=agent.total_trades,
            total_volume=agent.total_volume,
            configuration=agent.configuration,
            created_at=agent.created_at,
            updated_at=agent.updated_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating agent: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
        )


@router.get("/user/{user_id}", response_model=AgentListResponse)
async def get_user_agents(
    user_id: UUID,
    active_only: bool = False,
    db: AsyncSession = Depends(get_db_session),
) -> AgentListResponse:
    """Get all agents for a user.

    Args:
        user_id: User ID
        active_only: Filter active agents only
        db: Database session

    Returns:
        List of agents

    Raises:
        HTTPException: If query fails
    """
    try:
        repository = SQLAlchemyAgentRepository(db)
        handler = GetUserAgentsQueryHandler(repository)

        query = GetUserAgentsQuery(user_id=user_id, active_only=active_only)
        agents = await handler.handle(query)

        # Map to response
        agent_responses = [
            AgentResponse(
                id=agent.id,
                mandate_id=agent.mandate_id,
                user_id=agent.user_id,
                strategy_type=agent.strategy_type,
                status=agent.status.value,
                total_trades=agent.total_trades,
                total_volume=agent.total_volume,
                configuration=agent.configuration,
                created_at=agent.created_at,
                updated_at=agent.updated_at,
            )
            for agent in agents
        ]

        return AgentListResponse(agents=agent_responses, total=len(agent_responses))
    except Exception as e:
        logger.error(f"Error getting user agents: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
        )
