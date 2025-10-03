"""Wallet address value object."""

import re
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class WalletAddress(BaseModel):
    """Ethereum wallet address value object.

    Ensures wallet addresses are valid and properly formatted.
    """

    address: str = Field(..., description="Ethereum wallet address")

    @field_validator("address")
    @classmethod
    def validate_address(cls, v: str) -> str:
        """Validate Ethereum address format.

        Args:
            v: Address to validate

        Returns:
            Normalized address

        Raises:
            ValueError: If address is invalid
        """
        if not v:
            raise ValueError("Address cannot be empty")

        # Remove whitespace
        v = v.strip()

        # Check format (0x followed by 40 hex characters)
        if not re.match(r"^0x[a-fA-F0-9]{40}$", v):
            raise ValueError(f"Invalid Ethereum address format: {v}")

        # Convert to checksum address (lowercase for now)
        # In production, use web3.py's to_checksum_address
        return v.lower()

    @property
    def short_address(self) -> str:
        """Get shortened version of address for display.

        Returns:
            Shortened address (e.g., "0x742d...3bf8")
        """
        return f"{self.address[:6]}...{self.address[-4:]}"

    def __str__(self) -> str:
        """String representation.

        Returns:
            Full address
        """
        return self.address

    def __eq__(self, other) -> bool:
        """Check equality with another address.

        Args:
            other: Other address to compare

        Returns:
            True if addresses are equal
        """
        if isinstance(other, WalletAddress):
            return self.address.lower() == other.address.lower()
        if isinstance(other, str):
            return self.address.lower() == other.lower()
        return False

    @classmethod
    def create(cls, address: str) -> Optional["WalletAddress"]:
        """Safe creation of wallet address.

        Args:
            address: Address string

        Returns:
            WalletAddress or None if invalid
        """
        try:
            return cls(address=address)
        except ValueError:
            return None