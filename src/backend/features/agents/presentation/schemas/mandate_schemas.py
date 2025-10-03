"""Pydantic schemas for mandate API."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class MandateIntentSchema(BaseModel):
    """Schema for mandate intent."""

    max_spend: int = Field(..., gt=0, description="Maximum spend in smallest unit")
    valid_until: datetime = Field(..., description="Expiration timestamp")
    risk_tolerance: str = Field(..., description="Risk tolerance level")
    strategy_type: str = Field(..., description="Trading strategy type")


class MandateConstraintsSchema(BaseModel):
    """Schema for mandate constraints."""

    per_transaction_max: int = Field(..., gt=0, description="Max per transaction")
    daily_limit: Optional[int] = Field(None, description="Daily spending limit")
    allowed_protocols: List[str] = Field(default_factory=list, description="Allowed protocols")


class CreateMandateRequest(BaseModel):
    """Request schema for creating a mandate."""

    user_id: UUID
    user_address: str = Field(..., min_length=42, max_length=42)
    intent: MandateIntentSchema
    constraints: MandateConstraintsSchema
    nonce: int = Field(..., ge=0)


class SignMandateRequest(BaseModel):
    """Request schema for signing a mandate."""

    signature: str = Field(..., description="Cryptographic signature")


class MandateResponse(BaseModel):
    """Response schema for mandate."""

    id: UUID
    user_id: UUID
    user_address: str
    intent: MandateIntentSchema
    constraints: MandateConstraintsSchema
    signature: Optional[str] = None
    nonce: int
    revoked: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True
