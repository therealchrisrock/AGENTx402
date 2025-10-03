# TradingBotAgent

An AI-powered trading bot platform that enables users to invest in autonomous trading agents through natural language conversations on Telegram, secured by HTTP 402 payment mandates.

## 🏗️ Architecture

This project follows **Domain-Driven Design (DDD)** principles with a clean hexagonal architecture:

```text
telegram-402/
├── src/
│   ├── backend/                 # FastAPI HTTP API
│   │   ├── features/
│   │   │   └── agents/          # Agent orchestration domain
│   │   │       ├── domain/      # Pure business logic
│   │   │       ├── application/ # Use cases & commands
│   │   │       ├── infrastructure/ # Technical implementations
│   │   │       └── presentation/   # API routes & schemas
│   │   └── shared/              # Cross-cutting concerns
│   │       ├── domain/          # Base entities, value objects
│   │       ├── infrastructure/  # Database, cache, blockchain
│   │       └── application/     # Shared interfaces
│   ├── telegram_bot/            # Telegram bot interface
│   │   ├── handlers/            # Command & message handlers
│   │   ├── services/            # Claude AI, backend client
│   │   └── core/                # Configuration
│   └── shared_kernel/           # Shared types
├── tests/                       # Unit & integration tests
├── migrations/                  # Alembic database migrations
└── docker/                      # Docker configurations
```

## 🚀 Features

- **🤖 Conversational Interface** - Natural language interaction via Telegram
- **🔐 Cryptographic Mandates** - Secure, signed authorizations with spending limits (HTTP 402)
- **🎯 Agent Orchestration** - Autonomous trading bot management
- **⛓️ Blockchain Integration** - Ethereum/Web3 for transparent execution
- **📊 Domain Events** - Event-driven architecture for scalability
- **🧪 Comprehensive Testing** - Unit and integration tests

## ⚡ Quick Start

```bash
# 1. Install dependencies
pip install uv
uv sync --dev

# 2. Setup environment
cp .env.example .env
# Edit .env with your API keys

# 3. Run with Docker
docker-compose up --build

# Or run manually
uv run uvicorn src.backend.main:app --reload  # Terminal 1
uv run python -m src.telegram_bot.main         # Terminal 2
```

See [COMMANDS.md](COMMANDS.md) for all available commands.

## 📋 Prerequisites

- **Python 3.12+**
- **[uv](https://docs.astral.sh/uv/)** - Fast Python package manager
- **PostgreSQL 15+**
- **Redis 7+**
- **Docker & Docker Compose** (recommended)

## 🛠️ Local Development Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/telegram-402.git
cd telegram-402
```

### 2. Install dependencies

This project uses [uv](https://docs.astral.sh/uv/) for fast dependency management:

```bash
# Install uv if you haven't already
pip install uv

# Install all dependencies (including dev)
uv sync --dev
```

### 3. Configure environment variables

```bash
cp .env.example .env
# Edit .env with your actual values
```

**Required environment variables:**
- `TELEGRAM_BOT_TOKEN` - Get from [@BotFather](https://t.me/BotFather)
- `ANTHROPIC_API_KEY` - Get from [console.anthropic.com](https://console.anthropic.com)
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `ETHEREUM_RPC_URL` - Ethereum RPC endpoint

### 4. Run with Docker Compose (Recommended)

```bash
docker-compose up --build
```

This will start:
- PostgreSQL database (port 5432)
- Redis cache (port 6379)
- FastAPI backend (port 8000)
- Telegram bot

### 5. Run manually (without Docker)

**Terminal 1 - Database & Redis:**
```bash
docker-compose up postgres redis
```

**Terminal 2 - Run migrations:**
```bash
uv run alembic upgrade head
```

**Terminal 3 - Backend API:**
```bash
uv run uvicorn src.backend.main:app --reload
# API available at http://localhost:8000
# Docs at http://localhost:8000/docs
```

**Terminal 4 - Telegram Bot:**
```bash
uv run python -m src.telegram_bot.main
```

## 🧪 Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=term-missing

# Run specific test file
uv run pytest tests/unit/backend/test_domain_entities.py

# Run only unit tests
uv run pytest tests/unit/

# Run only integration tests
uv run pytest tests/integration/
```

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Key Endpoints

- `POST /api/v1/mandates` - Create a new mandate
- `GET /api/v1/mandates/{id}` - Get mandate by ID
- `PUT /api/v1/mandates/{id}/signature` - Sign a mandate
- `POST /api/v1/agents` - Create a new agent
- `GET /api/v1/agents/user/{user_id}` - Get user's agents

## 🏛️ Domain Model

### Core Entities

**Mandate** (Aggregate Root)
- Represents a signed user authorization for trading
- Contains spending limits and constraints
- Emits domain events (MandateCreated, MandateSigned, MandateRevoked)

**Agent** (Aggregate Root)
- Autonomous trading bot instance
- Executes trades within mandate constraints
- Tracks performance metrics
- Emits domain events (AgentCreated, AgentActivated, TradeExecuted)

### Value Objects

- **MandateIntent** - User's investment goals (risk tolerance, strategy, budget)
- **MandateConstraints** - Spending and operational limits
- **RiskTolerance** - Conservative, Moderate, Aggressive

## 🔄 Development Workflow

### Adding a New Feature

1. **Create domain models** in `src/backend/features/{feature}/domain/`
2. **Define use cases** in `src/backend/features/{feature}/application/`
3. **Implement infrastructure** in `src/backend/features/{feature}/infrastructure/`
4. **Create API routes** in `src/backend/features/{feature}/presentation/`
5. **Write tests** in `tests/unit/` and `tests/integration/`

### Database Migrations

```bash
# Create a new migration
uv run alembic revision --autogenerate -m "Add user table"

# Apply migrations
uv run migrate

# Rollback one migration
uv run alembic downgrade -1
```

### Code Quality

```bash
# Format code
uv run black src/ tests/

# Lint code
uv run ruff check src/ tests/

# Type checking
uv run mypy src/
```

> **💡 Tip:** See [COMMANDS.md](COMMANDS.md) for a complete list of all available commands.

## 🐳 Docker Deployment

### Build images

```bash
docker-compose build
```

### Run in detached mode

```bash
docker-compose up -d
```

### View logs

```bash
docker-compose logs -f backend
docker-compose logs -f telegram_bot
```

### Stop services

```bash
docker-compose down
```

## 📖 Project Structure Details

### Backend Features (DDD Layers)

Each feature follows this structure:

- **`domain/`** - Pure business logic, no dependencies
  - `entities/` - Aggregate roots and entities
  - `value_objects/` - Immutable value types
  - `events/` - Domain events
  - `repositories/` - Repository interfaces
  - `services/` - Domain services

- **`application/`** - Use cases and orchestration
  - `commands/` - Write operations
  - `queries/` - Read operations
  - `use_cases/` - Business workflows

- **`infrastructure/`** - Technical implementations
  - `repositories/` - Database implementations
  - `adapters/` - External service adapters
  - `services/` - Infrastructure services

- **`presentation/`** - API layer
  - `api/` - FastAPI routes
  - `schemas/` - Pydantic request/response models

## 🤝 Contributing

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make changes and write tests
3. Run quality checks: `uv run black . && uv run ruff check . && uv run pytest`
4. Commit with conventional commits: `git commit -m "feat(agents): add trade execution"`
5. Push and create PR: `git push origin feature/my-feature`

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: See `/docs` directory
- **Issues**: [GitHub Issues](https://github.com/yourusername/telegram-402/issues)

## 🗺️ Roadmap

- [ ] Implement SQLAlchemy ORM models
- [ ] Add user authentication & JWT
- [ ] Implement blockchain signature verification
- [ ] Add trading strategy templates
- [ ] Build Telegram Mini App for signing
- [ ] Add real-time portfolio monitoring
- [ ] Implement event bus for domain events
- [ ] Add monitoring & observability
- [ ] Deploy to production

---

Built with ❤️ using FastAPI, Telegram Bot API, and Claude AI
