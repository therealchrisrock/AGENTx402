# gRPC Setup for Agent x402

This document explains the gRPC communication setup between the Telegram bot and backend services.

## Architecture

```text
Telegram Bot (Client)  ←──gRPC──→  Backend (Server)
     Port: N/A                        Port: 50051
                                      HTTP: 8000
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -e .
pip install grpcio grpcio-tools
```

### 2. Generate Proto Files

```bash
make proto-gen
```

Or manually:
```bash
python -m grpc_tools.protoc \
    -I./proto \
    --python_out=./gen/python \
    --grpc_python_out=./gen/python \
    --pyi_out=./gen/python \
    ./proto/api/v1/telegram.proto
```

### 3. Start Backend (HTTP + gRPC)

```bash
python -m src.backend.main
```

This starts:
- FastAPI HTTP server on port 8000
- gRPC server on port 50051

### 4. Start Telegram Bot

In a new terminal:
```bash
python -m src.telegram_bot.main
```

### 5. Test gRPC Connection

#### Option A: Test Script
```bash
python test_grpc.py
```

#### Option B: Telegram Bot
Send `/ping` command to your bot to test the gRPC connection.

## Available gRPC Methods

### Health Check
- `Ping(PingRequest)` - Test connection

### User Management
- `GetUserState(GetUserStateRequest)` - Get user state by telegram ID
- `RegisterUser(RegisterUserRequest)` - Register new user
- `ConnectWallet(ConnectWalletRequest)` - Connect wallet to user account

### AI/NLP
- `ClassifyIntent(ClassifyIntentRequest)` - Classify user message intent

## Proto Definitions

See `proto/api/v1/telegram.proto` for complete service definitions.

## Project Structure

```text
.
├── proto/                    # Protobuf definitions
│   ├── buf.yaml             # Buf configuration
│   ├── buf.gen.yaml         # Code generation config
│   └── api/v1/
│       └── telegram.proto   # Service definitions
├── gen/                      # Generated code (gitignored)
│   └── python/
├── src/
│   ├── backend/
│   │   ├── main.py          # Dual server runner
│   │   └── grpc_server.py   # gRPC service implementation
│   └── telegram_bot/
│       └── services/
│           └── grpc_client.py  # gRPC client
└── test_grpc.py             # Test script
```

## Development Commands

```bash
# Generate proto files
make proto-gen

# Clean generated files
make proto-clean

# Run backend
make run-backend

# Run bot
make run-bot

# Test gRPC
make test-grpc
```

## Troubleshooting

### Connection Refused
- Ensure backend is running on port 50051
- Check firewall settings

### Import Errors
- Regenerate proto files: `make proto-gen`
- Ensure gen/ directory has __init__.py files

### Module Not Found
- Install dependencies: `pip install grpcio grpcio-tools`
- Check Python path includes project root

## Next Steps

1. Implement User domain entity with proper DDD structure
2. Add database persistence (replace in-memory storage)
3. Implement Redis for conversation state caching
4. Add wallet balance checking via Web3
5. Build complete onboarding flow with wallet connection UI
