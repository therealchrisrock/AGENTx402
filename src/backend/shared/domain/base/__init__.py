"""Base domain building blocks."""

from .aggregate_root import AggregateRoot
from .domain_event import DomainEvent
from .entity import Entity, TEntity
from .value_object import ValueObject

__all__ = [
    "Entity",
    "TEntity",
    "ValueObject",
    "AggregateRoot",
    "DomainEvent",
]
