"""Telegram bot command handlers."""

import logging

from telegram import Update
from telegram.ext import ContextTypes

from src.telegram_bot.services.grpc_client import get_grpc_client

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command with user registration.

    Args:
        update: Telegram update
        context: Handler context
    """
    user = update.effective_user
    telegram_id = user.id
    username = user.username or ""

    # Check if user exists via gRPC
    client = get_grpc_client()
    user_state = await client.get_user_state(telegram_id)

    if not user_state:
        # Register new user
        result = await client.register_user(telegram_id, username)
        if result and result['success']:
            logger.info(f"New user registered: {telegram_id}")
            welcome_message = f"""
👋 Welcome to Agent x402, {user.first_name}!

I'm your AI-powered trading assistant for autonomous crypto strategies.

Let's get you started:
1️⃣ Connect your wallet
2️⃣ Choose a trading strategy
3️⃣ Set your risk preferences

To begin, I'll need you to connect your wallet. You can:
• Type your wallet address (0x...)
• Use /wallet to see connection options

Ready when you are! 🚀
            """
        else:
            welcome_message = "Error registering user. Please try again."
    else:
        # Returning user
        state = user_state.get('state', 'NEW')
        balance = user_state.get('balance', 0)

        if state == 'NEW':
            welcome_message = f"""
Welcome back, {user.first_name}!

I see you haven't connected a wallet yet.
Use /wallet to connect your wallet and start trading.
            """
        elif state == 'WALLET_CONNECTED':
            welcome_message = f"""
Welcome back, {user.first_name}!

Wallet connected but no funds detected.
Balance: ${balance:.2f}

You need at least $50 to create a trading mandate.
            """
        elif state == 'FUNDED':
            welcome_message = f"""
Welcome back, {user.first_name}!

✅ Wallet connected
💰 Balance: ${balance:.2f}

Ready to trade! Use /create to set up your first trading mandate.
            """
        else:
            welcome_message = f"Welcome back, {user.first_name}!"

    await update.message.reply_text(welcome_message)


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /ping command to test gRPC connection.

    Args:
        update: Telegram update
        context: Handler context
    """
    await update.message.reply_text("🏓 Testing connection...")

    try:
        client = get_grpc_client()
        response = await client.ping("Hello from Telegram!")

        if response:
            await update.message.reply_text(f"✅ Connection successful!\n\nServer says: {response}")
        else:
            await update.message.reply_text("❌ Connection failed. Backend might be down.")
    except Exception as e:
        logger.error(f"Ping error: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")


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
