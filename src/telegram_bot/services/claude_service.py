"""Claude AI service for Telegram bot."""

import logging
from typing import Any, Dict, List

from anthropic import Anthropic

logger = logging.getLogger(__name__)


class ClaudeService:
    """Service for interacting with Claude API."""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514") -> None:
        """Initialize Claude service.

        Args:
            api_key: Anthropic API key
            model: Model to use
        """
        self.client = Anthropic(api_key=api_key)
        self.model = model

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str = "",
        max_tokens: int = 1024,
    ) -> str:
        """Generate a conversational response.

        Args:
            messages: List of message dictionaries
            system_prompt: System prompt
            max_tokens: Maximum tokens

        Returns:
            Generated response

        Raises:
            Exception: If API call fails
        """
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system=system_prompt,
                messages=messages,
            )

            return response.content[0].text
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            raise

    async def generate_mandate(self, conversation_history: List[Dict[str, str]]) -> Dict[str, Any]:
        """Generate structured mandate from conversation.

        Args:
            conversation_history: Conversation history

        Returns:
            Structured mandate data

        Raises:
            NotImplementedError: Not yet implemented
        """
        # TODO: Implement with structured output
        raise NotImplementedError("Mandate generation not yet implemented")
