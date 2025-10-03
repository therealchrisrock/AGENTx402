"""Domain repositories for agents feature."""

from .agent_repository import IAgentRepository
from .mandate_repository import IMandateRepository

__all__ = [
    "IMandateRepository",
    "IAgentRepository",
]
