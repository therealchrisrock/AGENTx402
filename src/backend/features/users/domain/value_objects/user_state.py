"""User state value object."""

from enum import Enum


class UserState(str, Enum):
    """User account states in the onboarding flow."""

    NEW = "NEW"
    WALLET_CONNECTED = "WALLET_CONNECTED"
    WALLET_CONNECTED_NO_FUNDS = "WALLET_CONNECTED_NO_FUNDS"
    FUNDED = "FUNDED"
    ACTIVE_TRADER = "ACTIVE_TRADER"

    def can_create_mandate(self) -> bool:
        """Check if user can create trading mandates.

        Returns:
            True if user can create mandates
        """
        return self in (UserState.FUNDED, UserState.ACTIVE_TRADER)

    def can_trade(self) -> bool:
        """Check if user can actively trade.

        Returns:
            True if user can trade
        """
        return self == UserState.ACTIVE_TRADER

    def next_state(self, wallet_connected: bool = False, balance: float = 0, has_mandate: bool = False) -> "UserState":
        """Determine next state based on conditions.

        Args:
            wallet_connected: Whether wallet is connected
            balance: Current wallet balance
            has_mandate: Whether user has active mandate

        Returns:
            Next user state
        """
        if self == UserState.NEW and wallet_connected:
            if balance >= 50:
                return UserState.FUNDED
            return UserState.WALLET_CONNECTED_NO_FUNDS

        if self == UserState.WALLET_CONNECTED_NO_FUNDS and balance >= 50:
            return UserState.FUNDED

        if self == UserState.FUNDED and has_mandate:
            return UserState.ACTIVE_TRADER

        return self