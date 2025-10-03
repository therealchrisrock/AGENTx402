"""Telegram bot callback handlers."""

import logging

from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle inline button callbacks.

    Args:
        update: Telegram update
        context: Handler context
    """
    query = update.callback_query
    await query.answer()

    callback_data = query.data
    logger.info(f"Callback data: {callback_data}")

    # TODO: Handle different callback actions
    if callback_data == "approve_mandate":
        await query.edit_message_text("Great! Please sign the mandate in the Mini App.")
    elif callback_data == "reject_mandate":
        await query.edit_message_text("Okay, let's start over. What would you like to do?")
    else:
        await query.edit_message_text(f"Callback: {callback_data}")
