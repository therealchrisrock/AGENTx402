# TradingBotAgent - Architecture Documentation

## Overview

TradingBotAgent is a **Domain-Driven Design (DDD)** application that implements an AI-powered trading bot platform with HTTP 402 payment mandates and Telegram interface.

## Architectural Principles

### 1. Domain-Driven Design (DDD)

The project is organized around business domains, not technical layers:

- **Ubiquitous Language** - Domain terminology used consistently across code
- **Bounded Contexts** - Clear boundaries between different domains
- **Aggregates** - Consistency boundaries (Mandate, Agent)
- **Domain Events** - First-class domain concepts for changes
- **Repository Pattern** - Abstract data access

### 2. Hexagonal Architecture (Ports & Adapters)

```text
┌─────────────────────────────────────────┐
│         Presentation Layer              │
│  (FastAPI Routes, Telegram Handlers)    │
└──────────────┬──────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────┐
│        Application Layer                │
│   (Commands, Queries, Use Cases)        │
└──────────────┬──────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────┐
│          Domain Layer                   │
│  (Entities, Value Objects, Events)      │
└──────────────┬──────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────┐
│      Infrastructure Layer               │
│ (Repositories, External Services)       │
└─────────────────────────────────────────┘
```

### 3. CQRS-Ready

Commands (writes) and Queries (reads) are separated:
- **Commands** - Change state, emit events
- **Queries** - Read-only, optimized for views

## Project Structure

### Backend (`src/backend/`)

```text
backend/
├── features/                  # Feature modules (domains)
│   └── agents/                # Agent orchestration domain
│       ├── domain/            # Business logic (pure)
│       │   ├── entities/      # Aggregate roots
│       │   ├── value_objects/ # Immutable values
│       │   ├── events/        # Domain events
│       │   ├── repositories/  # Repository interfaces
│       │   └── services/      # Domain services
│       ├── application/       # Use cases
│       │   ├── commands/      # Write operations
│       │   ├── queries/       # Read operations
│       │   └── use_cases/     # Complex workflows
│       ├── infrastructure/    # Technical details
│       │   ├── repositories/  # SQLAlchemy implementations
│       │   ├── adapters/      # External service adapters
│       │   └── services/      # Infrastructure services
│       └── presentation/      # API layer
│           ├── api/           # FastAPI routes
│           └── schemas/       # Pydantic models
└── shared/                    # Cross-cutting concerns
    ├── domain/                # Base DDD classes
    ├── infrastructure/        # Database, cache, blockchain
    └── application/           # Shared interfaces
```

### Telegram Bot (`src/telegram_bot/`)

```text
telegram_bot/
├── handlers/                  # Event handlers
│   ├── commands.py            # /start, /help, /status
│   ├── messages.py            # Natural language
│   └── callbacks.py           # Inline buttons
├── services/                  # External services
│   ├── claude_service.py      # Claude AI integration
│   └── backend_client.py      # FastAPI HTTP client
└── core/                      # Configuration
    └── config.py              # Settings
```

## Core Domain Models

### 1. Mandate (Aggregate Root)

A cryptographically signed authorization for trading within constraints.

**Entities:**
- `Mandate` - Root entity with lifecycle

**Value Objects:**
- `MandateIntent` - User's investment goals
- `MandateConstraints` - Spending limits

**Domain Events:**
- `MandateCreated`
- `MandateSigned`
- `MandateRevoked`

**Invariants:**
- Cannot sign revoked mandate
- Cannot sign twice
- Valid until date must be in future
- Max spend must be positive

### 2. Agent (Aggregate Root)

An autonomous trading bot instance executing within mandate constraints.

**Entities:**
- `Agent` - Root entity with status

**Domain Events:**
- `AgentCreated`
- `AgentActivated`
- `AgentDeactivated`
- `TradeExecuted`

**Invariants:**
- Must have valid mandate to activate
- Only active agents can execute trades
- Cannot activate already active agent

## Key Patterns

### Command Pattern

All state changes go through commands:

```python
command = CreateMandateCommand(
    user_id=user_id,
    user_address=address,
    # ...
)
result = await handler.handle(command)
```

### Repository Pattern

Data access abstracted behind interfaces:

```python
class IMandateRepository(IRepository[Mandate]):
    async def get_by_user_id(self, user_id: UUID) -> List[Mandate]:
        pass
```

### Domain Events

Changes publish events:

```python
mandate = Mandate.create(...)
events = mandate.get_domain_events()
# Events: [MandateCreated]
```

### Dependency Injection

Services injected via constructors:

```python
class CreateMandateCommandHandler:
    def __init__(self, mandate_repository: IMandateRepository):
        self.mandate_repository = mandate_repository
```

## Data Flow

### Creating a Mandate

```text
User (Telegram)
  → Telegram Bot Handler
  → Backend API (/api/v1/mandates)
  → CreateMandateCommand
  → CreateMandateCommandHandler
  → Mandate.create() [Domain Logic]
  → MandateRepository.add()
  → Database (SQLAlchemy)
```

### Executing a Trade

```text
Agent Orchestrator
  → ExecuteTradeCommand
  → ExecuteTradeCommandHandler
  → Mandate.can_execute_trade() [Domain Logic]
  → Agent.record_trade()
  → BlockchainService.execute_trade()
  → TradeExecuted Event
```

## Technology Stack

| Layer | Technology |
|-------|-----------|
| **API** | FastAPI 0.118+ |
| **Bot** | python-telegram-bot 20.7+ |
| **AI** | Anthropic Claude SDK |
| **Database** | PostgreSQL 15+ with SQLAlchemy 2.0 async |
| **Cache** | Redis 7+ |
| **Blockchain** | web3.py, eth-account |
| **Validation** | Pydantic 2.6+ |
| **Migrations** | Alembic |
| **Testing** | pytest, pytest-asyncio |
| **Deployment** | Docker, Docker Compose |

## Design Decisions

### 1. Why DDD?

- **Complex domain logic** - Trading rules, mandates, constraints
- **Event-driven** - Natural fit for blockchain/trading events
- **Scalability** - Bounded contexts allow independent scaling
- **Maintainability** - Clear separation of concerns

### 2. Why Separate Backend & Bot?

- **Different runtime models** - HTTP server vs. polling
- **Independent scaling** - Can scale bot separately
- **Clear responsibility** - Bot is presentation layer
- **Resilience** - Bot crash doesn't affect API

### 3. Why CQRS?

- **Read optimization** - Separate read models for dashboards
- **Event sourcing ready** - Can add event store later
- **Performance** - Optimize reads and writes separately

### 4. Why Async?

- **I/O bound** - Database, API calls, blockchain
- **Scalability** - Handle many concurrent requests
- **Modern Python** - SQLAlchemy 2.0, FastAPI, httpx

## Future Enhancements

### Planned Features

1. **Event Sourcing** - Store all domain events
2. **Read Models** - CQRS read-optimized projections
3. **Message Bus** - Decouple event handlers
4. **Saga Pattern** - Long-running transactions
5. **Multi-Chain Support** - Solana, Polygon, etc.
6. **Strategy Marketplace** - Discover and subscribe to strategies

### Scalability Considerations

- **Horizontal scaling** - Stateless services
- **Database sharding** - By user_id
- **Redis clustering** - Distributed cache
- **Event bus** - RabbitMQ or Kafka for event distribution
- **Read replicas** - PostgreSQL read replicas for queries

## Testing Strategy

### Unit Tests

Test domain logic in isolation:
- Entities and value objects
- Domain service behavior
- Business rule validation

### Integration Tests

Test component interactions:
- API endpoints
- Database queries
- External service calls

### Test Pyramid

```text
        /\
       /E2E\         (Few - Full user flows)
      /─────\
     / Integ \       (Some - Component interactions)
    /─────────\
   /   Unit    \     (Many - Domain logic)
  /─────────────\
```

## Security Considerations

1. **Signature Verification** - All mandates cryptographically signed
2. **Input Validation** - Pydantic schemas at API boundary
3. **SQL Injection** - SQLAlchemy ORM, parameterized queries
4. **Rate Limiting** - TODO: Add rate limiting middleware
5. **Authentication** - TODO: Add JWT authentication
6. **Authorization** - TODO: Add mandate ownership checks

## Monitoring & Observability

### Planned

- **Structured Logging** - JSON logs with correlation IDs
- **Metrics** - Prometheus for business metrics
- **Tracing** - OpenTelemetry for distributed tracing
- **Alerting** - PagerDuty for critical issues
- **Dashboards** - Grafana for visualization

## Contributing

When adding new features:

1. **Start with domain** - Define entities, value objects, events
2. **Define use cases** - Commands and queries
3. **Add tests** - Test domain logic first
4. **Implement infrastructure** - Repositories, adapters
5. **Create API** - Presentation layer last
6. **Document** - Update this file with new patterns

---

**Last Updated:** 2025-10-03
**Version:** 0.1.0 (Scaffolding Complete)
