"""Mapper for Mandate domain entity to ORM model."""

from src.backend.features.agents.domain.entities import Mandate
from src.backend.features.agents.domain.value_objects import (
    MandateConstraints,
    MandateIntent,
    RiskTolerance,
)
from src.backend.shared.infrastructure.persistence import BaseMapper

from .mandate_orm import MandateORM


class MandateMapper(BaseMapper[Mandate, MandateORM]):
    """Mapper between Mandate domain entity and MandateORM model."""

    def to_domain(self, model: MandateORM) -> Mandate:
        """Convert ORM model to domain entity.

        Args:
            model: MandateORM instance

        Returns:
            Mandate domain entity
        """
        # Reconstruct value objects from JSON
        intent = MandateIntent(
            max_spend=model.intent_data["max_spend"],
            valid_until=model.intent_data["valid_until"],
            risk_tolerance=RiskTolerance(model.intent_data["risk_tolerance"]),
            strategy_type=model.intent_data["strategy_type"],
        )

        constraints = MandateConstraints(
            per_transaction_max=model.constraints_data["per_transaction_max"],
            daily_limit=model.constraints_data.get("daily_limit"),
            allowed_protocols=model.constraints_data.get("allowed_protocols", []),
        )

        # Create domain entity
        mandate = Mandate(
            id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            user_id=model.user_id,
            user_address=model.user_address,
            intent=intent,
            constraints=constraints,
            signature=model.signature,
            nonce=model.nonce,
            revoked=model.revoked,
        )

        return mandate

    def to_orm(self, entity: Mandate, model: MandateORM | None = None) -> MandateORM:
        """Convert domain entity to ORM model.

        Args:
            entity: Mandate domain entity
            model: Existing MandateORM to update (optional)

        Returns:
            MandateORM instance
        """
        # Serialize value objects to JSON
        intent_data = {
            "max_spend": entity.intent.max_spend,
            "valid_until": entity.intent.valid_until.isoformat(),
            "risk_tolerance": entity.intent.risk_tolerance.value,
            "strategy_type": entity.intent.strategy_type,
        }

        constraints_data = {
            "per_transaction_max": entity.constraints.per_transaction_max,
            "daily_limit": entity.constraints.daily_limit,
            "allowed_protocols": entity.constraints.allowed_protocols,
        }

        if model is None:
            # Create new ORM model
            model = MandateORM(
                id=entity.id,
                created_at=entity.created_at,
                updated_at=entity.updated_at,
                user_id=entity.user_id,
                user_address=entity.user_address,
                intent_data=intent_data,
                constraints_data=constraints_data,
                signature=entity.signature,
                nonce=entity.nonce,
                revoked=entity.revoked,
            )
        else:
            # Update existing model
            model.user_address = entity.user_address
            model.intent_data = intent_data
            model.constraints_data = constraints_data
            model.signature = entity.signature
            model.nonce = entity.nonce
            model.revoked = entity.revoked
            model.updated_at = entity.updated_at

        return model
