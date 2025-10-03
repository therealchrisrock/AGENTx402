# Testing the Telegram Onboarding Flow

## Prerequisites

1. **Create a Telegram Bot**
   - Open Telegram and search for @BotFather
   - Send `/newbot` command
   - Choose a name for your bot (e.g., "MyTradingTestBot")
   - Choose a username (must end with 'bot', e.g., "mytradingtest_bot")
   - Copy the bot token you receive

2. **Set up Environment**
   ```bash
   # Copy the example env file
   cp .env.example .env

   # Edit .env and add your real bot token:
   # TELEGRAM_BOT_TOKEN=YOUR_ACTUAL_BOT_TOKEN_HERE
   ```

## Running the Test

### Terminal 1: Start Backend Server
```bash
# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows

# Run the test gRPC server (uses in-memory database)
python test_grpc_server.py
```

### Terminal 2: Start Telegram Bot
```bash
# In a new terminal, activate venv
source .venv/bin/activate

# Run the Telegram bot
python -m src.telegram_bot.main
```

## Testing in Telegram

1. **Open Telegram** and search for your bot username
2. **Start conversation**: Send `/start`
3. **Connect wallet**: Send `/wallet`
4. **Choose manual entry** and enter a test address like:
   ```text
   0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb4
   ```

5. **Confirm the connection**

## Expected Flow

```text
User: /start
Bot: 👋 Welcome to Agent x402!
     Let's get you started...
     Use /wallet to connect your wallet

User: /wallet
Bot: 🔐 Connect Your Wallet
     [MetaMask] [WalletConnect] [Phantom] [Manual Entry] [Cancel]

User: [clicks Manual Entry]
Bot: Please enter your Ethereum wallet address...

User: 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb4
Bot: Confirm Wallet Connection
     Address: 0x742d35Cc...5f0bEb4
     [✅ Confirm] [❌ Cancel]

User: [clicks Confirm]
Bot: ✅ Wallet Connected Successfully!
     Balance: $100.00 USDC (mocked)
     🎉 You're ready to start trading!
```

## Test Commands

- `/start` - Initialize or check user status
- `/wallet` - Start wallet connection flow
- `/status` - Check your current status
- `/ping` - Test gRPC connection
- `/help` - Show available commands
- `/cancel` - Cancel current operation

## Debugging

If something doesn't work:

1. **Check gRPC server is running**
   - You should see: "Test gRPC server starting on port 50051..."

2. **Check bot is connected**
   - You should see: "Starting TradingBotAgent Telegram Bot..."

3. **Test gRPC connection**
   - In Telegram, send `/ping`
   - Should respond: "✅ Connection successful!"

4. **Check logs** in both terminals for any errors

## Clean Test Data

The test server stores data in memory, so just restart it to clear all data:
```bash
# Ctrl+C to stop the server
# Run again to start fresh
python test_grpc_server.py
```
