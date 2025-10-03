"""Base value object class for DDD."""

from abc import ABC
from typing import Any

from pydantic import BaseModel


class ValueObject(BaseModel, ABC):
    """Base class for all value objects.

    Value objects are immutable and have no identity.
    They are equal when their attributes are equal.
    """

    class Config:
        """Pydantic configuration."""

        frozen = True  # Immutable
        validate_assignment = True
        arbitrary_types_allowed = True

    def __eq__(self, other: Any) -> bool:
        """Value objects are equal if all attributes are equal."""
        if not isinstance(other, self.__class__):
            return False
        return self.model_dump() == other.model_dump()

    def __hash__(self) -> int:
        """Hash based on all attribute values."""
        return hash(tuple(sorted(self.model_dump().items())))
