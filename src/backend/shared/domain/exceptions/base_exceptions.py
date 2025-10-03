"""Base domain exceptions."""

from typing import Any, Dict, Optional


class DomainException(Exception):
    """Base exception for all domain exceptions."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        """Initialize domain exception.

        Args:
            message: Error message
            details: Additional error details
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}


class EntityNotFoundError(DomainException):
    """Exception raised when an entity is not found."""

    def __init__(
        self, entity_type: str, entity_id: Any, details: Optional[Dict[str, Any]] = None
    ) -> None:
        """Initialize entity not found error.

        Args:
            entity_type: Type of entity
            entity_id: ID of the entity
            details: Additional error details
        """
        message = f"{entity_type} with id {entity_id} not found"
        super().__init__(message, details)
        self.entity_type = entity_type
        self.entity_id = entity_id


class ValidationError(DomainException):
    """Exception raised when validation fails."""

    pass


class InvalidOperationError(DomainException):
    """Exception raised when an invalid operation is attempted."""

    pass
