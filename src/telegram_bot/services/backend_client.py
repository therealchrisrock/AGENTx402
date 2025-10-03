"""Backend API client for Telegram bot."""

import logging
from typing import Any, Dict, List

import httpx

from src.telegram_bot.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class BackendClient:
    """HTTP client for FastAPI backend."""

    def __init__(self) -> None:
        """Initialize backend client."""
        self.base_url = settings.backend_url
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=30.0)

    async def create_mandate(self, mandate_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new mandate.

        Args:
            mandate_data: Mandate data

        Returns:
            Created mandate response

        Raises:
            httpx.HTTPError: If request fails
        """
        try:
            response = await self.client.post("/api/v1/mandates", json=mandate_data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Error creating mandate: {e}")
            raise

    async def get_user_mandates(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all mandates for a user.

        Args:
            user_id: User ID

        Returns:
            List of mandates

        Raises:
            httpx.HTTPError: If request fails
        """
        try:
            # TODO: Implement actual endpoint
            response = await self.client.get(f"/api/v1/mandates/user/{user_id}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Error fetching mandates: {e}")
            raise

    async def update_signature(self, mandate_id: str, signature: str) -> Dict[str, Any]:
        """Update mandate signature.

        Args:
            mandate_id: Mandate ID
            signature: Signature

        Returns:
            Updated mandate

        Raises:
            httpx.HTTPError: If request fails
        """
        try:
            response = await self.client.put(
                f"/api/v1/mandates/{mandate_id}/signature", json={"signature": signature}
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Error updating signature: {e}")
            raise

    async def close(self) -> None:
        """Close the HTTP client."""
        await self.client.aclose()
