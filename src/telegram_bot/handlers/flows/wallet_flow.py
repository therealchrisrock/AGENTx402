"""Wallet connection flow handler."""

import logging
import re
from typing import Optional

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from src.telegram_bot.services.grpc_client import get_grpc_client

logger = logging.getLogger(__name__)

# Conversation states
WALLET_MENU, WALLET_INPUT, WALLET_CONFIRM = range(3)


class WalletConnectionFlow:
    """Handles wallet connection conversation flow."""

    @staticmethod
    async def start_wallet_flow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Start wallet connection flow.

        Args:
            update: Telegram update
            context: Handler context

        Returns:
            Next conversation state
        """
        keyboard = [
            [InlineKeyboardButton("🦊 MetaMask", callback_data="wallet_metamask")],
            [InlineKeyboardButton("🔗 WalletConnect", callback_data="wallet_connect")],
            [InlineKeyboardButton("👻 Phantom", callback_data="wallet_phantom")],
            [InlineKeyboardButton("✍️ Manual Entry", callback_data="wallet_manual")],
            [InlineKeyboardButton("❌ Cancel", callback_data="wallet_cancel")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        message = """
🔐 **Connect Your Wallet**

Choose how you'd like to connect your wallet:

• **MetaMask** - Popular Ethereum wallet
• **WalletConnect** - Universal wallet protocol
• **Phantom** - Solana & Ethereum wallet
• **Manual Entry** - Enter address directly

_Your wallet address will be used to create trading mandates._
        """

        if update.callback_query:
            await update.callback_query.answer()
            await update.callback_query.edit_message_text(
                message, reply_markup=reply_markup, parse_mode="Markdown"
            )
        else:
            await update.message.reply_text(
                message, reply_markup=reply_markup, parse_mode="Markdown"
            )

        return WALLET_MENU

    @staticmethod
    async def handle_wallet_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle wallet connection method choice.

        Args:
            update: Telegram update
            context: Handler context

        Returns:
            Next conversation state
        """
        query = update.callback_query
        await query.answer()

        choice = query.data

        if choice == "wallet_cancel":
            await query.edit_message_text("Wallet connection cancelled.")
            return ConversationHandler.END

        if choice == "wallet_manual":
            await query.edit_message_text(
                "Please enter your Ethereum wallet address:\n\n"
                "_Format: 0x followed by 40 hexadecimal characters_\n"
                "Example: `0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb4`",
                parse_mode="Markdown"
            )
            context.user_data['wallet_type'] = 'manual'
            return WALLET_INPUT

        # For other wallet types, show coming soon message
        wallet_names = {
            "wallet_metamask": "MetaMask",
            "wallet_connect": "WalletConnect",
            "wallet_phantom": "Phantom",
        }

        await query.edit_message_text(
            f"🚧 **{wallet_names.get(choice, 'This wallet')} Integration Coming Soon**\n\n"
            "For now, please use Manual Entry to connect your wallet.\n\n"
            "Use /wallet to try again.",
            parse_mode="Markdown"
        )
        return ConversationHandler.END

    @staticmethod
    async def handle_wallet_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle manual wallet address input.

        Args:
            update: Telegram update
            context: Handler context

        Returns:
            Next conversation state
        """
        address = update.message.text.strip()

        # Validate Ethereum address format
        if not re.match(r'^0x[a-fA-F0-9]{40}$', address):
            await update.message.reply_text(
                "❌ **Invalid wallet address format**\n\n"
                "Please enter a valid Ethereum address.\n"
                "Format: 0x followed by 40 hexadecimal characters\n\n"
                "Example: `0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb4`",
                parse_mode="Markdown"
            )
            return WALLET_INPUT

        # Store address in context
        context.user_data['wallet_address'] = address

        # Show confirmation
        keyboard = [
            [
                InlineKeyboardButton("✅ Confirm", callback_data="wallet_confirm"),
                InlineKeyboardButton("❌ Cancel", callback_data="wallet_cancel_confirm"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            f"**Confirm Wallet Connection**\n\n"
            f"Address: `{address[:8]}...{address[-6:]}`\n"
            f"Type: Manual Entry\n\n"
            f"Is this correct?",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

        return WALLET_CONFIRM

    @staticmethod
    async def handle_wallet_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle wallet connection confirmation.

        Args:
            update: Telegram update
            context: Handler context

        Returns:
            Next conversation state
        """
        query = update.callback_query
        await query.answer()

        if query.data == "wallet_cancel_confirm":
            await query.edit_message_text("Wallet connection cancelled.")
            return ConversationHandler.END

        # Get stored data
        wallet_address = context.user_data.get('wallet_address')
        wallet_type = context.user_data.get('wallet_type', 'manual')

        if not wallet_address:
            await query.edit_message_text("Error: No wallet address found. Please try again.")
            return ConversationHandler.END

        # Get user state first
        user = update.effective_user
        client = get_grpc_client()

        await query.edit_message_text("🔄 Connecting wallet...")

        # Get user state to get user_id
        user_state = await client.get_user_state(user.id)

        if not user_state or not user_state.get('user_id'):
            await query.edit_message_text(
                "❌ User not found. Please use /start to register first.",
                parse_mode="Markdown"
            )
            return ConversationHandler.END

        # Connect wallet via gRPC
        result = await client.connect_wallet(
            user_id=user_state['user_id'],
            wallet_address=wallet_address,
            wallet_type=wallet_type
        )

        if result and result['success']:
            balance = result.get('balance', 0)
            state = result.get('new_state', 'UNKNOWN')

            if balance >= 50:
                message = (
                    f"✅ **Wallet Connected Successfully!**\n\n"
                    f"Address: `{wallet_address[:8]}...{wallet_address[-6:]}`\n"
                    f"Balance: ${balance:.2f} USDC\n\n"
                    f"🎉 You're ready to start trading!\n"
                    f"Use /create to set up your first trading mandate."
                )
            else:
                message = (
                    f"✅ **Wallet Connected Successfully!**\n\n"
                    f"Address: `{wallet_address[:8]}...{wallet_address[-6:]}`\n"
                    f"Balance: ${balance:.2f} USDC\n\n"
                    f"⚠️ You need at least $50 to create a trading mandate.\n"
                    f"Please add funds to your wallet and check back."
                )

            await query.edit_message_text(message, parse_mode="Markdown")
        else:
            error_msg = result.get('message', 'Unknown error') if result else 'Connection failed'
            await query.edit_message_text(
                f"❌ **Failed to connect wallet**\n\n{error_msg}\n\n"
                "Please try again with /wallet",
                parse_mode="Markdown"
            )

        # Clear user data
        context.user_data.clear()
        return ConversationHandler.END

    @staticmethod
    async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Cancel the wallet connection flow.

        Args:
            update: Telegram update
            context: Handler context

        Returns:
            End of conversation
        """
        await update.message.reply_text(
            "Wallet connection cancelled. Use /wallet to try again."
        )
        context.user_data.clear()
        return ConversationHandler.END

    @classmethod
    def get_conversation_handler(cls) -> ConversationHandler:
        """Get conversation handler for wallet connection flow.

        Returns:
            ConversationHandler for wallet flow
        """
        return ConversationHandler(
            entry_points=[CommandHandler("wallet", cls.start_wallet_flow)],
            states={
                WALLET_MENU: [
                    CallbackQueryHandler(cls.handle_wallet_choice, pattern="^wallet_")
                ],
                WALLET_INPUT: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, cls.handle_wallet_input)
                ],
                WALLET_CONFIRM: [
                    CallbackQueryHandler(cls.handle_wallet_confirm, pattern="^wallet_confirm"),
                    CallbackQueryHandler(cls.handle_wallet_confirm, pattern="^wallet_cancel_confirm"),
                ],
            },
            fallbacks=[CommandHandler("cancel", cls.cancel)],
        )