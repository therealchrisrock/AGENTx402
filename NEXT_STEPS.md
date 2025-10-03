# 🚀 Next Steps - Implementation Guide

## Current Status

✅ **Scaffolding Complete** - All architectural components in place
🚧 **Implementation Phase** - Ready to build features

## 🎯 Immediate Next Steps

### Step 1: Verify Setup ✅

```bash
# 1. Check Python version
python --version  # Should be 3.12+

# 2. Install dependencies
uv sync --dev

# 3. Copy environment file
cp .env.example .env

# 4. Edit .env with your keys
# - TELEGRAM_BOT_TOKEN (from @BotFather)
# - ANTHROPIC_API_KEY (from console.anthropic.com)
# - DATABASE_URL
# - REDIS_URL
```

### Step 2: Test Scaffolding 🧪

```bash
# Run existing tests
uv run pytest

# Expected result:
# - All tests should pass
# - Domain entity tests ✅
# - Value object tests ✅
# - Health endpoint test ✅
```

### Step 3: Start Services 🐳

```bash
# Option A: Docker Compose (Recommended)
docker-compose up --build

# Option B: Manual
# Terminal 1: Database
docker-compose up postgres redis

# Terminal 2: Backend
uv run backend

# Terminal 3: Bot
uv run bot
```

### Step 4: Verify Services ✅

```bash
# Check backend health
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","service":"tradingbotagent-api","version":"0.1.0"}

# Check API docs
open http://localhost:8000/docs

# Test Telegram bot
# Send /start to your bot on Telegram
```

## 📋 Implementation Roadmap

### Phase 1: Database Layer (Week 1) 🗄️

**Priority: CRITICAL**

#### Task 1.1: Create SQLAlchemy ORM Models

Create `src/backend/features/agents/infrastructure/models/orm_models.py`:

```python
from sqlalchemy import Column, String, Integer, Boolean, DateTime, UUID, JSON
from sqlalchemy.orm import relationship
from src.backend.shared.infrastructure.database import Base

class MandateORM(Base):
    __tablename__ = "mandates"

    id = Column(UUID, primary_key=True)
    user_id = Column(UUID, nullable=False, index=True)
    user_address = Column(String(42), nullable=False)
    intent_data = Column(JSON, nullable=False)
    constraints_data = Column(JSON, nullable=False)
    signature = Column(String, nullable=True)
    nonce = Column(Integer, nullable=False)
    revoked = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

class AgentORM(Base):
    __tablename__ = "agents"

    id = Column(UUID, primary_key=True)
    mandate_id = Column(UUID, ForeignKey("mandates.id"))
    user_id = Column(UUID, nullable=False, index=True)
    strategy_type = Column(String, nullable=False)
    status = Column(String, nullable=False)
    total_trades = Column(Integer, default=0)
    total_volume = Column(Integer, default=0)
    configuration = Column(JSON, default={})
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
```

**Files to create:**
- [ ] `src/backend/features/agents/infrastructure/models/orm_models.py`
- [ ] `src/backend/features/agents/infrastructure/models/__init__.py`
- [ ] `src/backend/features/agents/infrastructure/models/mappers.py` (Domain ↔ ORM)

#### Task 1.2: Implement Repository Methods

Update `SQLAlchemyMandateRepository` with real implementations:

```python
async def add(self, entity: Mandate) -> Mandate:
    orm_model = MandateMapper.to_orm(entity)
    self.session.add(orm_model)
    await self.session.flush()
    return entity

async def get_by_id(self, entity_id: UUID) -> Optional[Mandate]:
    result = await self.session.execute(
        select(MandateORM).where(MandateORM.id == entity_id)
    )
    orm_model = result.scalar_one_or_none()
    return MandateMapper.to_domain(orm_model) if orm_model else None
```

**Files to update:**
- [ ] `src/backend/features/agents/infrastructure/repositories/sqlalchemy_mandate_repository.py`
- [ ] `src/backend/features/agents/infrastructure/repositories/sqlalchemy_agent_repository.py`

#### Task 1.3: Create Database Migration

```bash
# Create migration
alembic revision --autogenerate -m "Create mandates and agents tables"

# Review migration file in migrations/versions/

# Apply migration
alembic upgrade head
```

**Files to create:**
- [ ] Migration file in `migrations/versions/`

#### Task 1.4: Test Database Layer

Create `tests/integration/backend/test_repositories.py`:

```python
async def test_mandate_repository_add(db_session):
    repo = SQLAlchemyMandateRepository(db_session)
    mandate = Mandate.create(...)

    result = await repo.add(mandate)

    assert result.id == mandate.id
    # ... more assertions
```

**Files to create:**
- [ ] `tests/integration/backend/test_repositories.py`

### Phase 2: API Completion (Week 2) 🌐

#### Task 2.1: Wire Up Database Sessions

Update `src/backend/main.py`:

```python
from src.backend.shared.infrastructure.database import DatabaseSessionManager

settings = get_settings()
session_manager = DatabaseSessionManager(settings.database_url)

async def get_db():
    async for session in session_manager.get_session():
        yield session

# Update routes to use real dependency
```

**Files to update:**
- [ ] `src/backend/main.py`
- [ ] `src/backend/features/agents/presentation/api/mandate_routes.py`
- [ ] `src/backend/features/agents/presentation/api/agent_routes.py`

#### Task 2.2: Add User Management

Create a new feature:

```bash
mkdir -p src/backend/features/identity/{domain,application,infrastructure,presentation}
```

**New files to create:**
- [ ] `src/backend/features/identity/domain/entities/user.py`
- [ ] `src/backend/features/identity/application/commands/create_user_command.py`
- [ ] `src/backend/features/identity/infrastructure/repositories/user_repository.py`
- [ ] `src/backend/features/identity/presentation/api/auth_routes.py`

#### Task 2.3: Implement JWT Authentication

```python
# Install: pip install python-jose[cryptography] passlib[bcrypt]

# Create src/backend/shared/infrastructure/security/jwt.py
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

**Files to create:**
- [ ] `src/backend/shared/infrastructure/security/jwt.py`
- [ ] `src/backend/shared/infrastructure/security/dependencies.py`

### Phase 3: Blockchain Integration (Week 3) ⛓️

#### Task 3.1: Implement Signature Verification

Update `BlockchainService.verify_signature()`:

```python
def verify_signature(self, message: str, signature: str, address: str) -> bool:
    try:
        message_hash = encode_defunct(text=message)
        recovered = Account.recover_message(message_hash, signature=signature)
        return recovered.lower() == address.lower()
    except Exception as e:
        logger.error(f"Signature verification failed: {e}")
        return False
```

**Files to update:**
- [ ] `src/backend/features/agents/infrastructure/services/blockchain_service.py`

#### Task 3.2: Add Mandate Signing Flow

1. Backend generates mandate data
2. Frontend signs with Web3
3. Backend verifies signature
4. Backend stores signed mandate

**Files to update:**
- [ ] `src/backend/features/agents/presentation/api/mandate_routes.py`

### Phase 4: Telegram Enhancement (Week 4) 💬

#### Task 4.1: Conversation State Management

Install conversation handler:

```python
from telegram.ext import ConversationHandler

# Define states
COLLECTING_AMOUNT, COLLECTING_RISK, CONFIRMING = range(3)

# Create handler with states
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('invest', start_investment)],
    states={
        COLLECTING_AMOUNT: [MessageHandler(filters.TEXT, collect_amount)],
        COLLECTING_RISK: [MessageHandler(filters.TEXT, collect_risk)],
        CONFIRMING: [CallbackQueryHandler(confirm_mandate)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)
```

**Files to create:**
- [ ] `src/telegram_bot/handlers/conversation_handler.py`
- [ ] `src/telegram_bot/services/state_manager.py`

#### Task 4.2: Implement Mandate Generation

Update Claude service:

```python
async def generate_mandate_from_conversation(
    self,
    conversation: List[Dict[str, str]]
) -> Dict[str, Any]:
    # Use Claude with structured output
    response = self.client.messages.create(
        model=self.model,
        tools=[{
            "name": "generate_mandate",
            "description": "Generate mandate from conversation",
            "input_schema": {
                "type": "object",
                "properties": {
                    "max_spend": {"type": "integer"},
                    "risk_tolerance": {"type": "string"},
                    # ...
                }
            }
        }],
        messages=conversation
    )
    # Extract structured data
    return response.content[0].input
```

**Files to update:**
- [ ] `src/telegram_bot/services/claude_service.py`

### Phase 5: Production Readiness (Week 5+) 🚀

#### Task 5.1: Add Monitoring

```bash
# Install dependencies
pip install prometheus-client structlog

# Add metrics
from prometheus_client import Counter, Histogram

mandate_created = Counter('mandates_created_total', 'Total mandates created')
trade_latency = Histogram('trade_execution_seconds', 'Trade execution time')
```

#### Task 5.2: Add Rate Limiting

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/v1/mandates")
@limiter.limit("5/minute")
async def create_mandate(...):
    ...
```

#### Task 5.3: Environment-Specific Configs

Create configs:
- [ ] `configs/development.env`
- [ ] `configs/staging.env`
- [ ] `configs/production.env`

## 🧪 Testing Checklist

After each phase:

- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] API endpoints tested with Swagger
- [ ] Telegram bot tested manually
- [ ] Code formatted (`make format`)
- [ ] Code linted (`make lint`)
- [ ] Type checking passes (`make type-check`)

## 📝 Development Tips

### 1. Use Type Hints Everywhere

```python
async def create_mandate(
    user_id: UUID,
    intent: MandateIntent,
) -> Mandate:
    ...
```

### 2. Write Tests First (TDD)

```python
# Write test
async def test_create_mandate():
    mandate = Mandate.create(...)
    assert mandate.user_id == expected_user_id

# Then implement
class Mandate(AggregateRoot):
    @classmethod
    def create(...) -> "Mandate":
        ...
```

### 3. Follow DDD Patterns

- ✅ Keep domain logic pure (no infrastructure)
- ✅ Use value objects for validation
- ✅ Emit domain events for changes
- ✅ Repository pattern for data access

### 4. Git Workflow

```bash
# Feature branch
git checkout -b feat/database-layer

# Commit often with conventional commits
git commit -m "feat(agents): add SQLAlchemy ORM models"
git commit -m "test(agents): add repository integration tests"

# Push and create PR
git push origin feat/database-layer
```

## 🎓 Learning Resources

- **DDD**: "Domain-Driven Design" by Eric Evans
- **Python Async**: Python asyncio documentation
- **FastAPI**: Official FastAPI tutorial
- **SQLAlchemy**: SQLAlchemy 2.0 async tutorial
- **Telegram Bots**: python-telegram-bot documentation

## 🆘 Troubleshooting

### Database Connection Errors

```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Check connection
psql $DATABASE_URL
```

### Import Errors

```bash
# Reinstall in editable mode
pip install -e .

# Or add to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

### Type Errors

```bash
# Run mypy to see all errors
mypy src/

# Fix incrementally
```

## ✅ Success Criteria

You'll know you're making progress when:

1. ✅ All tests pass
2. ✅ API returns real data from database
3. ✅ Telegram bot creates mandates
4. ✅ Signatures are verified
5. ✅ Agents execute trades

## 🎉 Conclusion

The scaffolding is complete. Now it's time to bring it to life!

Start with **Phase 1 (Database Layer)** and work methodically through each phase.

**Good luck!** 🚀

---

*Need help? Check ARCHITECTURE.md or create an issue.*
