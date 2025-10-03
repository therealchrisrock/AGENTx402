"""Telegram bot command handlers."""

import logging

from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command.

    Args:
        update: Telegram update
        context: Handler context
    """
    user = update.effective_user
    welcome_message = f"""
👋 Welcome to TradingBotAgent, {user.first_name}!

I'm your AI-powered trading assistant. I can help you:
• Create autonomous trading bots
• Invest in top-performing strategies
• Monitor your portfolio 24/7
• Manage risk automatically

To get started, just tell me what you want to achieve. For example:
"I want to invest $500 in copy trading with moderate risk"

Or type /help to learn more.
    """
    await update.message.reply_text(welcome_message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command.

    Args:
        update: Telegram update
        context: Handler context
    """
    help_text = """
🤖 TradingBotAgent Commands:

/start - Start the bot and see welcome message
/help - Show this help message
/status - View your active mandates and agents
/cancel - Cancel current operation

💡 You can also just talk to me naturally! Tell me what you want to do and I'll guide you through the process.
    """
    await update.message.reply_text(help_text)


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /status command.

    Args:
        update: Telegram update
        context: Handler context
    """
    # TODO: Fetch user's mandates and agents from backend
    status_message = """
📊 Your Status:

Active Mandates: 0
Running Agents: 0
Total Invested: $0.00

You don't have any active trading bots yet. Send me a message to get started!
    """
    await update.message.reply_text(status_message)
