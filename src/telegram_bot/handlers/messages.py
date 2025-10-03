"""Telegram bot message handlers."""

import logging

from telegram import Update
from telegram.ext import ContextTypes

from src.telegram_bot.core.config import get_settings
from src.telegram_bot.services.claude_service import ClaudeService

logger = logging.getLogger(__name__)
settings = get_settings()

# Initialize Claude service
claude_service = ClaudeService(settings.anthropic_api_key)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle natural language messages.

    Args:
        update: Telegram update
        context: Handler context
    """
    user_message = update.message.text
    user_id = update.effective_user.id

    logger.info(f"User {user_id} sent: {user_message}")

    try:
        # Generate response using Claude
        response = await claude_service.generate_response(
            messages=[{"role": "user", "content": user_message}],
            system_prompt=(
                "You are a helpful AI assistant for a crypto trading bot platform. "
                "Help users create trading bot mandates and explain how the system works."
            ),
        )

        await update.message.reply_text(response)
    except Exception as e:
        logger.error(f"Error generating Claude response: {e}")
        await update.message.reply_text(
            "Sorry, I encountered an error. Please try again later."
        )
