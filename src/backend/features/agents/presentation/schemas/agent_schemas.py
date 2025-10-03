"""Pydantic schemas for agent API."""

from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class CreateAgentRequest(BaseModel):
    """Request schema for creating an agent."""

    mandate_id: UUID
    user_id: UUID
    strategy_type: str = Field(..., description="Trading strategy type")
    configuration: Optional[Dict] = Field(None, description="Agent configuration")


class AgentResponse(BaseModel):
    """Response schema for agent."""

    id: UUID
    mandate_id: UUID
    user_id: UUID
    strategy_type: str
    status: str
    total_trades: int
    total_volume: int
    configuration: Dict
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


class AgentListResponse(BaseModel):
    """Response schema for list of agents."""

    agents: List[AgentResponse]
    total: int
