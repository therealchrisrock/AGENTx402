# TradingBotAgent - Project Instructions

## Architecture Overview

This project follows **Domain-Driven Design (DDD)** principles with hexagonal architecture and CQRS patterns.

### Core Principles
- **Domain-first development**: Start with domain entities, then application layer, then infrastructure
- **Pure domain logic**: Domain layer has NO dependencies on infrastructure
- **CQRS**: Separate Commands (writes) from Queries (reads)
- **Event-driven**: Domain events for all state changes
- **Async by default**: All I/O operations use async/await

## Project Structure

```text
src/
├── backend/                    # FastAPI HTTP API
│   ├── features/
│   │   └── agents/             # Agent orchestration domain
│   │       ├── domain/         # Pure business logic (NO infrastructure deps)
│   │       │   ├── entities/   # Aggregates (Mandate, Agent)
│   │       │   ├── value_objects/  # Immutable values (MandateIntent, etc.)
│   │       │   ├── events/     # Domain events
│   │       │   ├── repositories/  # Repository interfaces ONLY
│   │       │   └── services/   # Domain services
│   │       ├── application/    # Use cases & orchestration
│   │       │   ├── commands/   # Write operations (CreateMandateCommand)
│   │       │   ├── queries/    # Read operations (GetMandateQuery)
│   │       │   └── use_cases/  # Complex workflows
│   │       ├── infrastructure/ # Technical implementations
│   │       │   ├── repositories/  # SQLAlchemy concrete implementations
│   │       │   ├── adapters/   # External service adapters
│   │       │   └── services/   # Infrastructure services
│   │       └── presentation/   # API layer
│   │           ├── api/        # FastAPI routes
│   │           └── schemas/    # Pydantic request/response models
│   └── shared/                 # Cross-cutting concerns
│       ├── domain/             # Base DDD classes
│       ├── infrastructure/     # Database, cache, blockchain
│       └── application/        # Shared interfaces
├── telegram_bot/               # Telegram interface (presentation layer)
│   ├── handlers/               # Command & message handlers
│   ├── services/               # Claude AI, backend HTTP client
│   └── core/                   # Configuration
└── shared_kernel/              # Shared base types
    ├── domain/                 # Entity, ValueObject, AggregateRoot
    └── types/                  # Common types
```

## Domain-Driven Design Layers

### 1. Domain Layer (Pure Business Logic)

**Location**: `src/backend/features/{feature}/domain/`

**Contains**:
- **Entities** - Objects with identity (e.g., `Mandate`, `Agent`)
- **Value Objects** - Immutable, validated values (e.g., `MandateIntent`, `RiskTolerance`)
- **Aggregates** - Consistency boundaries with root entities
- **Domain Events** - First-class domain changes (e.g., `MandateCreated`, `TradeExecuted`)
- **Repository Interfaces** - Abstract contracts for data access
- **Domain Services** - Business logic that doesn't fit in entities

**Rules**:
- NO infrastructure dependencies (no SQLAlchemy, no HTTP, no external services)
- Pure Python logic with type hints
- All validation in value objects or entity methods
- Emit domain events for state changes

### 2. Application Layer (Use Cases)

**Location**: `src/backend/features/{feature}/application/`

**Contains**:
- **Commands** - Write operations that change state
- **Queries** - Read operations (read-only)
- **Command/Query Handlers** - Execute use cases
- **Use Cases** - Complex business workflows

**Rules**:
- Commands and Queries are separated (CQRS)
- Each command/query has a dedicated handler
- Handlers orchestrate domain logic and repositories
- Return DTOs, not domain entities

### 3. Infrastructure Layer (Technical Implementation)

**Location**: `src/backend/features/{feature}/infrastructure/`

**Contains**:
- **Repository Implementations** - SQLAlchemy concrete classes
- **Adapters** - External service integrations
- **Services** - Technical services (blockchain, cache, etc.)

**Rules**:
- Implements domain repository interfaces
- Handles data mapping (domain ↔ ORM)
- Manages external service communication
- Database sessions, HTTP clients, etc.

### 4. Presentation Layer (API)

**Location**: `src/backend/features/{feature}/presentation/`

**Contains**:
- **API Routes** - FastAPI endpoints
- **Schemas** - Pydantic request/response models
- **Dependency injection** - Route dependencies

**Rules**:
- Routes call application command/query handlers
- Pydantic schemas for validation
- Return JSON-serializable responses
- No business logic in routes

## Development Workflow

### Adding a New Feature

**1. Start with Domain Layer**
```python
# Create domain entities first
# src/backend/features/my_feature/domain/entities/my_entity.py

from src.shared_kernel.domain import AggregateRoot
from uuid import UUID

class MyEntity(AggregateRoot):
    def __init__(self, id: UUID, name: str):
        super().__init__(id)
        self._name = name

    @classmethod
    def create(cls, name: str) -> "MyEntity":
        entity = cls(UUID(), name)
        entity.add_domain_event(MyEntityCreated(entity.id, name))
        return entity
```

**2. Define Value Objects**
```python
# src/backend/features/my_feature/domain/value_objects/my_value.py

from src.shared_kernel.domain import ValueObject

class MyValue(ValueObject):
    def __init__(self, value: str):
        if not value:
            raise ValueError("Value cannot be empty")
        self._value = value
```

**3. Create Domain Events**
```python
# src/backend/features/my_feature/domain/events/my_entity_created.py

from src.shared_kernel.domain import DomainEvent

class MyEntityCreated(DomainEvent):
    def __init__(self, entity_id: UUID, name: str):
        super().__init__()
        self.entity_id = entity_id
        self.name = name
```

**4. Define Repository Interface**
```python
# src/backend/features/my_feature/domain/repositories/my_repository.py

from abc import abstractmethod
from src.shared_kernel.domain import IRepository

class IMyRepository(IRepository[MyEntity]):
    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[MyEntity]:
        pass
```

**5. Create Application Commands/Queries**
```python
# src/backend/features/my_feature/application/commands/create_my_entity_command.py

from dataclasses import dataclass

@dataclass
class CreateMyEntityCommand:
    name: str

class CreateMyEntityCommandHandler:
    def __init__(self, repository: IMyRepository):
        self.repository = repository

    async def handle(self, command: CreateMyEntityCommand) -> UUID:
        entity = MyEntity.create(command.name)
        await self.repository.add(entity)
        return entity.id
```

**6. Implement Infrastructure**
```python
# src/backend/features/my_feature/infrastructure/repositories/sqlalchemy_my_repository.py

from sqlalchemy.ext.asyncio import AsyncSession
from src.backend.features.my_feature.domain.repositories import IMyRepository

class SQLAlchemyMyRepository(IMyRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, entity: MyEntity) -> MyEntity:
        orm_model = MyEntityMapper.to_orm(entity)
        self.session.add(orm_model)
        await self.session.flush()
        return entity
```

**7. Create API Routes**
```python
# src/backend/features/my_feature/presentation/api/my_routes.py

from fastapi import APIRouter, Depends

router = APIRouter(prefix="/api/v1/my-entities", tags=["my-entities"])

@router.post("/", status_code=201)
async def create_my_entity(
    request: CreateMyEntityRequest,
    handler: CreateMyEntityCommandHandler = Depends(get_handler)
):
    command = CreateMyEntityCommand(name=request.name)
    entity_id = await handler.handle(command)
    return {"id": str(entity_id)}
```

**8. Write Tests First (TDD)**
```python
# tests/unit/backend/features/my_feature/test_my_entity.py

async def test_create_my_entity():
    entity = MyEntity.create("Test")

    assert entity.name == "Test"
    assert len(entity.get_domain_events()) == 1
    assert isinstance(entity.get_domain_events()[0], MyEntityCreated)
```

## Package Management

**IMPORTANT**: This project uses **UV** for package management, NOT pip, poetry, or other tools.

### Common Commands

```bash
# Install dependencies
uv sync --dev

# Add a new dependency
uv add <package-name>

# Add dev dependency
uv add --dev <package-name>

# Run backend
uv run backend

# Run bot
uv run bot

# Run tests
uv run pytest

# Run migrations
uv run migrate

# Format code
uv run black src/ tests/

# Lint code
uv run ruff check src/ tests/

# Type check
uv run mypy src/
```

**Never use**:
- ❌ `pip install`
- ❌ `poetry add`
- ❌ `pipenv install`

**Always use**:
- ✅ `uv add`
- ✅ `uv sync`
- ✅ `uv run`

## Key Technical Decisions

### 1. Separate Backend & Bot
- **Backend**: FastAPI HTTP API (port 8000)
- **Bot**: Telegram bot (separate process)
- **Why**: Different runtimes, independent scaling, clear responsibility

### 2. Async Everywhere
- All I/O operations use `async`/`await`
- SQLAlchemy async sessions
- Async HTTP clients (httpx)
- python-telegram-bot async API

### 3. Type Hints Required
- Full type hints on all functions
- Mypy strict mode enabled
- Pydantic for runtime validation

### 4. Repository Pattern
- Abstract data access behind interfaces
- Domain layer depends on interfaces
- Infrastructure provides implementations
- Easy to test with mocks

### 5. CQRS Pattern
- Commands change state, return void or ID
- Queries read data, return DTOs
- Optimized separately for performance

## Database

### Technology
- **PostgreSQL 15+** with async SQLAlchemy 2.0
- **Alembic** for migrations
- **Redis** for caching

### Migrations Workflow

```bash
# Create migration (auto-detect changes)
uv run alembic revision --autogenerate -m "Add users table"

# Review migration file in migrations/versions/

# Apply migrations
uv run migrate

# Rollback one migration
uv run alembic downgrade -1

# View current revision
uv run alembic current
```

## Testing

### Test Structure
```text
tests/
├── unit/
│   └── backend/
│       └── features/
│           └── agents/
│               ├── test_domain_entities.py
│               └── test_value_objects.py
└── integration/
    └── backend/
        └── test_api_routes.py
```

### Testing Guidelines
- **Unit tests**: Test domain logic in isolation (no database)
- **Integration tests**: Test API endpoints with database
- Use pytest fixtures for common setups
- Async tests with `pytest-asyncio`

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

## Docker

### Services
- **postgres**: PostgreSQL database (port 5432)
- **redis**: Redis cache (port 6379)
- **backend**: FastAPI API (port 8000)
- **telegram_bot**: Telegram bot

### Commands
```bash
# Start all services
docker-compose up --build

# Start in detached mode
docker-compose up -d

# View logs
docker-compose logs -f backend
docker-compose logs -f telegram_bot

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Restart specific service
docker-compose restart telegram_bot
```

## Common Patterns

### Domain Event Pattern
```python
class Mandate(AggregateRoot):
    @classmethod
    def create(cls, ...) -> "Mandate":
        mandate = cls(...)
        mandate.add_domain_event(MandateCreated(...))
        return mandate

    def sign(self, signature: str) -> None:
        self._signature = signature
        self.add_domain_event(MandateSigned(self.id, signature))
```

### Dependency Injection
```python
# In main.py or router
def get_mandate_repository(
    session: AsyncSession = Depends(get_db)
) -> IMandateRepository:
    return SQLAlchemyMandateRepository(session)

def get_create_mandate_handler(
    repo: IMandateRepository = Depends(get_mandate_repository)
) -> CreateMandateCommandHandler:
    return CreateMandateCommandHandler(repo)

# In route
@router.post("/mandates")
async def create_mandate(
    request: CreateMandateRequest,
    handler: CreateMandateCommandHandler = Depends(get_create_mandate_handler)
):
    command = CreateMandateCommand(...)
    result = await handler.handle(command)
    return result
```

### Value Object Validation
```python
class MandateIntent(ValueObject):
    def __init__(
        self,
        risk_tolerance: RiskTolerance,
        max_spend: int,
        strategy: str
    ):
        # Validation in constructor
        if max_spend <= 0:
            raise ValueError("max_spend must be positive")
        if not strategy:
            raise ValueError("strategy cannot be empty")

        self._risk_tolerance = risk_tolerance
        self._max_spend = max_spend
        self._strategy = strategy

    @property
    def risk_tolerance(self) -> RiskTolerance:
        return self._risk_tolerance
```

## Current Implementation Status

### ✅ Complete
- Project structure and scaffolding
- Domain models (Mandate, Agent)
- Value objects (MandateIntent, MandateConstraints, RiskTolerance)
- Domain events (MandateCreated, AgentActivated, etc.)
- Command/Query interfaces
- Repository interfaces
- FastAPI routes (scaffolded)
- Telegram bot handlers (basic)
- Docker setup
- Test infrastructure

### 🚧 Needs Implementation
- SQLAlchemy ORM models and mappers
- Repository concrete implementations
- Blockchain signature verification
- JWT authentication
- Trade execution logic
- Conversation state management in bot
- Integration tests with database

## Environment Variables

Required in `.env`:
- `TELEGRAM_BOT_TOKEN` - From @BotFather
- `ANTHROPIC_API_KEY` - From console.anthropic.com
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `ETHEREUM_RPC_URL` - Ethereum RPC endpoint
- `BACKEND_URL` - Backend API URL (for bot)
- `DEBUG` - Debug mode (true/false)

## Quick Reference

### File Locations
- Add domain entity: `src/backend/features/{feature}/domain/entities/`
- Add value object: `src/backend/features/{feature}/domain/value_objects/`
- Add command: `src/backend/features/{feature}/application/commands/`
- Add query: `src/backend/features/{feature}/application/queries/`
- Add repository impl: `src/backend/features/{feature}/infrastructure/repositories/`
- Add API route: `src/backend/features/{feature}/presentation/api/`
- Add unit test: `tests/unit/backend/features/{feature}/`
- Add integration test: `tests/integration/backend/`

### Development Flow
1. Write test first (TDD)
2. Create domain model
3. Define command/query
4. Implement handler
5. Create infrastructure (if needed)
6. Add API route
7. Run tests: `uv run pytest`
8. Format: `uv run black src/ tests/`
9. Lint: `uv run ruff check src/ tests/`
10. Type check: `uv run mypy src/`

### Before Committing
```bash
uv run black src/ tests/
uv run ruff check --fix src/ tests/
uv run mypy src/
uv run pytest
```

## Resources

- **Architecture**: See `ARCHITECTURE.md` for detailed DDD patterns
- **Commands**: See `COMMANDS.md` for complete command reference
- **API Docs**: http://localhost:8000/docs (when running)

---

**Remember**:
- Start with domain layer
- Keep domain pure (no infrastructure)
- Use async/await everywhere
- Always use `uv` for package management
- Write tests first
- Follow CQRS: separate commands from queries
