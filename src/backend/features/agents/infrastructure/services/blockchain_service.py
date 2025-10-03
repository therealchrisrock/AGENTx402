"""Blockchain service adapter."""

import logging
from typing import Optional

from web3 import Web3
from eth_account import Account
from eth_account.messages import encode_defunct

logger = logging.getLogger(__name__)


class BlockchainService:
    """Service for blockchain interactions."""

    def __init__(self, rpc_url: str) -> None:
        """Initialize blockchain service.

        Args:
            rpc_url: Ethereum RPC URL
        """
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))

    def verify_signature(
        self, message: str, signature: str, expected_address: str
    ) -> bool:
        """Verify a message signature.

        Args:
            message: Original message
            signature: Signature to verify
            expected_address: Expected signer address

        Returns:
            True if signature is valid, False otherwise
        """
        try:
            message_hash = encode_defunct(text=message)
            recovered_address = Account.recover_message(message_hash, signature=signature)
            return recovered_address.lower() == expected_address.lower()
        except Exception as e:
            logger.error(f"Signature verification error: {e}")
            return False

    async def execute_trade(
        self, protocol: str, amount: int, from_address: str, private_key: str
    ) -> Optional[str]:
        """Execute a trade on blockchain.

        Args:
            protocol: Protocol to use
            amount: Trade amount
            from_address: Sender address
            private_key: Private key for signing

        Returns:
            Transaction hash if successful, None otherwise

        Raises:
            NotImplementedError: Not yet implemented
        """
        # TODO: Implement trade execution
        raise NotImplementedError("Trade execution not yet implemented")

    def get_balance(self, address: str) -> int:
        """Get balance of an address.

        Args:
            address: Address to check

        Returns:
            Balance in wei
        """
        try:
            return self.w3.eth.get_balance(address)
        except Exception as e:
            logger.error(f"Error getting balance: {e}")
            return 0
