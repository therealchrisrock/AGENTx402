#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Telegram Onboarding Flow Test Runner${NC}"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating from template...${NC}"
    cp .env.example .env
    echo -e "${RED}❌ Please edit .env and add your Telegram bot token${NC}"
    echo "   Get a token from @BotFather on Telegram"
    echo ""
    echo "   Then run this script again."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d .venv ]; then
    echo -e "${YELLOW}📦 Creating virtual environment...${NC}"
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Check if dependencies are installed
if ! python -c "import grpc" 2>/dev/null; then
    echo -e "${YELLOW}📦 Installing dependencies...${NC}"
    pip install -r requirements.txt 2>/dev/null || {
        # If requirements.txt doesn't exist, install manually
        pip install grpcio grpcio-tools python-telegram-bot pydantic pydantic-settings \
                   sqlalchemy aiosqlite asyncpg python-dotenv anthropic
    }
fi

# Function to run server in background
run_grpc_server() {
    echo -e "${GREEN}🔧 Starting gRPC test server...${NC}"
    python test_grpc_server.py &
    GRPC_PID=$!
    sleep 2
    echo -e "${GREEN}✅ gRPC server running (PID: $GRPC_PID)${NC}"
    echo ""
}

# Function to run bot
run_telegram_bot() {
    echo -e "${GREEN}🤖 Starting Telegram bot...${NC}"
    echo -e "${YELLOW}   Open Telegram and message your bot to test${NC}"
    echo -e "${YELLOW}   Commands: /start, /wallet, /ping, /status${NC}"
    echo ""
    echo -e "${RED}Press Ctrl+C to stop${NC}"
    echo ""
    python -m src.telegram_bot.main
}

# Trap to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Shutting down...${NC}"
    if [ ! -z "$GRPC_PID" ]; then
        kill $GRPC_PID 2>/dev/null
    fi
    exit 0
}
trap cleanup INT

# Check if we're running automated test or interactive
if [ "$1" == "auto" ]; then
    echo -e "${GREEN}🤖 Running automated tests...${NC}"
    run_grpc_server
    python test_onboarding.py
    cleanup
else
    echo -e "${GREEN}📱 Starting interactive test mode...${NC}"
    echo ""
    run_grpc_server
    run_telegram_bot
fi