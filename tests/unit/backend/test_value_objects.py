"""Unit tests for value objects."""

from datetime import datetime, timedelta

import pytest

from src.backend.features.agents.domain.value_objects import (
    MandateConstraints,
    MandateIntent,
    RiskTolerance,
)


class TestMandateIntent:
    """Tests for MandateIntent value object."""

    def test_create_valid_intent(self) -> None:
        """Test creating a valid mandate intent."""
        intent = MandateIntent(
            max_spend=1000000,
            valid_until=datetime.utcnow() + timedelta(days=30),
            risk_tolerance=RiskTolerance.MODERATE,
            strategy_type="copy_trading",
        )

        assert intent.max_spend == 1000000
        assert intent.risk_tolerance == RiskTolerance.MODERATE
        assert intent.is_valid()

    def test_invalid_max_spend(self) -> None:
        """Test that max_spend must be positive."""
        with pytest.raises(ValueError, match="greater than 0"):
            MandateIntent(
                max_spend=0,
                valid_until=datetime.utcnow() + timedelta(days=30),
                risk_tolerance=RiskTolerance.MODERATE,
                strategy_type="copy_trading",
            )

    def test_invalid_date(self) -> None:
        """Test that valid_until must be in the future."""
        with pytest.raises(ValueError, match="must be in the future"):
            MandateIntent(
                max_spend=1000000,
                valid_until=datetime.utcnow() - timedelta(days=1),
                risk_tolerance=RiskTolerance.MODERATE,
                strategy_type="copy_trading",
            )

    def test_intent_immutability(self) -> None:
        """Test that intent is immutable."""
        intent = MandateIntent(
            max_spend=1000000,
            valid_until=datetime.utcnow() + timedelta(days=30),
            risk_tolerance=RiskTolerance.MODERATE,
            strategy_type="copy_trading",
        )

        with pytest.raises(Exception):  # Pydantic ValidationError
            intent.max_spend = 2000000


class TestMandateConstraints:
    """Tests for MandateConstraints value object."""

    def test_create_valid_constraints(self) -> None:
        """Test creating valid constraints."""
        constraints = MandateConstraints(
            per_transaction_max=50000, daily_limit=200000, allowed_protocols=["uniswap"]
        )

        assert constraints.per_transaction_max == 50000
        assert constraints.daily_limit == 200000
        assert len(constraints.allowed_protocols) == 1

    def test_is_transaction_allowed(self) -> None:
        """Test transaction amount validation."""
        constraints = MandateConstraints(per_transaction_max=50000)

        assert constraints.is_transaction_allowed(30000)
        assert not constraints.is_transaction_allowed(60000)

    def test_is_protocol_allowed(self) -> None:
        """Test protocol validation."""
        constraints = MandateConstraints(
            per_transaction_max=50000, allowed_protocols=["uniswap", "sushiswap"]
        )

        assert constraints.is_protocol_allowed("uniswap")
        assert not constraints.is_protocol_allowed("pancakeswap")

    def test_empty_protocols_allows_all(self) -> None:
        """Test that empty protocol list allows all protocols."""
        constraints = MandateConstraints(per_transaction_max=50000, allowed_protocols=[])

        assert constraints.is_protocol_allowed("anything")
