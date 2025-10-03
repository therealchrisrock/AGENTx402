"""User aggregate root."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import Field

from src.backend.shared.domain.base import AggregateRoot
from ..events.user_events import (
    UserRegistered,
    WalletConnected,
    UserFunded,
    UserBecameActiveTrader,
)
from ..value_objects import UserState, WalletAddress


class User(AggregateRoot):
    """User aggregate root.

    Represents a user in the system with their wallet and trading state.
    """

    telegram_id: int
    telegram_username: Optional[str] = None
    state: UserState = Field(default=UserState.NEW)
    wallet_address: Optional[str] = None
    wallet_type: Optional[str] = None  # metamask, walletconnect, phantom, manual
    balance: float = Field(default=0.0)
    onboarding_completed_at: Optional[datetime] = None
    first_mandate_id: Optional[UUID] = None

    def connect_wallet(
        self,
        wallet_address: str,
        wallet_type: str = "manual",
        balance: float = 0.0
    ) -> None:
        """Connect a wallet to the user account.

        Args:
            wallet_address: Ethereum wallet address
            wallet_type: Type of wallet connection
            balance: Current wallet balance

        Raises:
            ValueError: If wallet is already connected or address is invalid
        """
        if self.wallet_address:
            raise ValueError(f"Wallet already connected: {self.wallet_address}")

        # Validate wallet address
        wallet = WalletAddress.create(wallet_address)
        if not wallet:
            raise ValueError(f"Invalid wallet address: {wallet_address}")

        self.wallet_address = wallet.address
        self.wallet_type = wallet_type
        self.balance = balance

        # Update state based on balance
        if balance >= 50:
            self.state = UserState.FUNDED
            self.add_domain_event(
                UserFunded(
                    aggregate_id=self.id,
                    event_type="UserFunded",
                    user_id=self.id,
                    wallet_address=wallet.address,
                    balance=balance,
                )
            )
        else:
            self.state = UserState.WALLET_CONNECTED_NO_FUNDS

        self.updated_at = datetime.utcnow()
        self.add_domain_event(
            WalletConnected(
                aggregate_id=self.id,
                event_type="WalletConnected",
                user_id=self.id,
                wallet_address=wallet.address,
                wallet_type=wallet_type,
            )
        )

    def update_balance(self, new_balance: float) -> None:
        """Update user's wallet balance.

        Args:
            new_balance: New balance amount

        Raises:
            ValueError: If wallet is not connected
        """
        if not self.wallet_address:
            raise ValueError("No wallet connected")

        old_balance = self.balance
        self.balance = new_balance

        # Check if user just became funded
        if old_balance < 50 <= new_balance and self.state == UserState.WALLET_CONNECTED_NO_FUNDS:
            self.state = UserState.FUNDED
            self.add_domain_event(
                UserFunded(
                    aggregate_id=self.id,
                    event_type="UserFunded",
                    user_id=self.id,
                    wallet_address=self.wallet_address,
                    balance=new_balance,
                )
            )

        self.updated_at = datetime.utcnow()

    def activate_trading(self, mandate_id: UUID) -> None:
        """Mark user as active trader when they create their first mandate.

        Args:
            mandate_id: ID of the first mandate

        Raises:
            ValueError: If user is not funded or already active
        """
        if self.state != UserState.FUNDED:
            raise ValueError(f"User must be funded to start trading. Current state: {self.state}")

        self.state = UserState.ACTIVE_TRADER
        self.first_mandate_id = mandate_id
        self.updated_at = datetime.utcnow()

        self.add_domain_event(
            UserBecameActiveTrader(
                aggregate_id=self.id,
                event_type="UserBecameActiveTrader",
                user_id=self.id,
                first_mandate_id=mandate_id,
            )
        )

    def complete_onboarding(self) -> None:
        """Mark onboarding as completed.

        Raises:
            ValueError: If wallet is not connected
        """
        if not self.wallet_address:
            raise ValueError("Cannot complete onboarding without wallet")

        self.onboarding_completed_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def can_create_mandate(self) -> bool:
        """Check if user can create trading mandates.

        Returns:
            True if user can create mandates
        """
        return self.state.can_create_mandate()

    def can_trade(self) -> bool:
        """Check if user can actively trade.

        Returns:
            True if user can trade
        """
        return self.state.can_trade()

    def is_onboarded(self) -> bool:
        """Check if user has completed onboarding.

        Returns:
            True if onboarding is complete
        """
        return self.wallet_address is not None and self.onboarding_completed_at is not None

    @property
    def short_wallet_address(self) -> Optional[str]:
        """Get shortened wallet address for display.

        Returns:
            Shortened address or None
        """
        if self.wallet_address:
            wallet = WalletAddress(address=self.wallet_address)
            return wallet.short_address
        return None

    @classmethod
    def create(
        cls,
        telegram_id: int,
        telegram_username: Optional[str] = None
    ) -> "User":
        """Create a new user.

        Args:
            telegram_id: Telegram user ID
            telegram_username: Optional Telegram username

        Returns:
            New user instance
        """
        user = cls(
            telegram_id=telegram_id,
            telegram_username=telegram_username,
            state=UserState.NEW,
        )

        user.add_domain_event(
            UserRegistered(
                aggregate_id=user.id,
                event_type="UserRegistered",
                user_id=user.id,
                telegram_id=telegram_id,
                telegram_username=telegram_username,
            )
        )

        return user