"""Telegram bot main entry point."""

import asyncio
import logging

from telegram import Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, MessageHandler, filters

from src.telegram_bot.core.config import get_settings
from src.telegram_bot.handlers import callbacks, commands, messages

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

settings = get_settings()


async def error_handler(update: Update, context) -> None:
    """Log errors caused by updates.

    Args:
        update: Telegram update
        context: Handler context
    """
    logger.error(f"Update {update} caused error {context.error}")


def main() -> None:
    """Start the Telegram bot."""
    # Create application
    application = Application.builder().token(settings.telegram_bot_token).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", commands.start))
    application.add_handler(CommandHandler("help", commands.help_command))
    application.add_handler(CommandHandler("status", commands.status))

    # Register message handler (natural language)
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, messages.handle_message)
    )

    # Register callback query handler (inline buttons)
    application.add_handler(CallbackQueryHandler(callbacks.handle_callback))

    # Register error handler
    application.add_error_handler(error_handler)

    # Start the bot
    logger.info("Starting TradingBotAgent Telegram Bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
