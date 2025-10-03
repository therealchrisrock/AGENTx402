"""Unit tests for domain entities."""

from datetime import datetime, timedelta
from uuid import uuid4

import pytest

from src.backend.features.agents.domain.entities import Agent, Mandate
from src.backend.features.agents.domain.value_objects import (
    MandateConstraints,
    MandateIntent,
    RiskTolerance,
)


class TestMandate:
    """Tests for Mandate aggregate."""

    def test_create_mandate(self) -> None:
        """Test creating a new mandate."""
        user_id = uuid4()
        intent = MandateIntent(
            max_spend=1000000,
            valid_until=datetime.utcnow() + timedelta(days=30),
            risk_tolerance=RiskTolerance.MODERATE,
            strategy_type="copy_trading",
        )
        constraints = MandateConstraints(
            per_transaction_max=50000, daily_limit=200000, allowed_protocols=["uniswap", "sushiswap"]
        )

        mandate = Mandate.create(
            user_id=user_id,
            user_address="0x1234567890123456789012345678901234567890",
            intent=intent,
            constraints=constraints,
            nonce=1,
        )

        assert mandate.user_id == user_id
        assert mandate.nonce == 1
        assert not mandate.revoked
        assert mandate.signature is None
        assert len(mandate.get_domain_events()) == 1

    def test_sign_mandate(self) -> None:
        """Test signing a mandate."""
        user_id = uuid4()
        intent = MandateIntent(
            max_spend=1000000,
            valid_until=datetime.utcnow() + timedelta(days=30),
            risk_tolerance=RiskTolerance.MODERATE,
            strategy_type="copy_trading",
        )
        constraints = MandateConstraints(per_transaction_max=50000)

        mandate = Mandate.create(
            user_id=user_id,
            user_address="0x1234567890123456789012345678901234567890",
            intent=intent,
            constraints=constraints,
            nonce=1,
        )

        signature = "0xabcdef123456"
        mandate.sign(signature)

        assert mandate.signature == signature
        assert len(mandate.get_domain_events()) == 2

    def test_cannot_sign_twice(self) -> None:
        """Test that a mandate cannot be signed twice."""
        user_id = uuid4()
        intent = MandateIntent(
            max_spend=1000000,
            valid_until=datetime.utcnow() + timedelta(days=30),
            risk_tolerance=RiskTolerance.MODERATE,
            strategy_type="copy_trading",
        )
        constraints = MandateConstraints(per_transaction_max=50000)

        mandate = Mandate.create(
            user_id=user_id,
            user_address="0x1234567890123456789012345678901234567890",
            intent=intent,
            constraints=constraints,
            nonce=1,
        )

        mandate.sign("0xabcdef123456")

        with pytest.raises(ValueError, match="already signed"):
            mandate.sign("0x999999999999")

    def test_revoke_mandate(self) -> None:
        """Test revoking a mandate."""
        user_id = uuid4()
        intent = MandateIntent(
            max_spend=1000000,
            valid_until=datetime.utcnow() + timedelta(days=30),
            risk_tolerance=RiskTolerance.MODERATE,
            strategy_type="copy_trading",
        )
        constraints = MandateConstraints(per_transaction_max=50000)

        mandate = Mandate.create(
            user_id=user_id,
            user_address="0x1234567890123456789012345678901234567890",
            intent=intent,
            constraints=constraints,
            nonce=1,
        )

        mandate.revoke()

        assert mandate.revoked
        assert not mandate.is_valid()


class TestAgent:
    """Tests for Agent aggregate."""

    def test_create_agent(self) -> None:
        """Test creating a new agent."""
        mandate_id = uuid4()
        user_id = uuid4()

        agent = Agent.create(
            mandate_id=mandate_id,
            user_id=user_id,
            strategy_type="copy_trading",
            configuration={"min_trade": 100},
        )

        assert agent.mandate_id == mandate_id
        assert agent.user_id == user_id
        assert agent.total_trades == 0
        assert agent.total_volume == 0
        assert len(agent.get_domain_events()) == 1

    def test_activate_agent(self) -> None:
        """Test activating an agent."""
        agent = Agent.create(
            mandate_id=uuid4(), user_id=uuid4(), strategy_type="copy_trading"
        )

        agent.activate()

        assert agent.is_active()
        assert len(agent.get_domain_events()) == 2

    def test_record_trade(self) -> None:
        """Test recording a trade."""
        agent = Agent.create(
            mandate_id=uuid4(), user_id=uuid4(), strategy_type="copy_trading"
        )

        agent.activate()
        agent.record_trade(trade_amount=50000, protocol="uniswap", transaction_hash="0xabc")

        assert agent.total_trades == 1
        assert agent.total_volume == 50000
        assert len(agent.get_domain_events()) == 3
