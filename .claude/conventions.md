# TradingBotAgent - Code Conventions

## Git Commit Convention

### Format
```text
<type>(<scope>): <subject>

<body>

<footer>
```

### Rules
- **Subject**: Max 50 chars, imperative mood ("add" not "added"), no period
- **Body**: Wrap at 72 chars, explain what/why not how, blank line after subject
- **Breaking changes**: Add `!` after type or `BREAKING CHANGE:` in footer

### Types
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation changes
- `style` - Code style changes (formatting, no logic change)
- `refactor` - Code refactoring (no feature/bug change)
- `perf` - Performance improvements
- `test` - Adding or updating tests
- `build` - Build system changes
- `ci` - CI/CD changes
- `chore` - Other changes (dependencies, configs)
- `revert` - Revert previous commit

### Scopes (Project-Specific)
- `agents` - Agent domain/features
- `mandates` - Mandate domain/features
- `api` - Backend API
- `bot` - Telegram bot
- `db` - Database/migrations
- `auth` - Authentication
- `blockchain` - Blockchain integration
- `config` - Configuration
- `types` - Type definitions
- `tests` - Test infrastructure

### Examples

**Good commits**:
```bash
feat(agents): add trade execution command

fix(api): prevent duplicate mandate creation

perf(db): add index on user_id column

docs(architecture): update DDD patterns section
```

**Good with body**:
```bash
feat(bot): add conversation state management

Implement multi-step mandate creation flow:
- Track conversation state in Redis
- Add inline keyboard navigation
- Support cancel at any step

Closes #123
```

**Breaking change**:
```bash
feat(api)!: change mandate response format

BREAKING CHANGE: 'data' field renamed to 'content'
for consistency with other endpoints
```

### Quick Reference
- Atomic commits (one logical change)
- Reference issues with `#123`
- Present tense, imperative mood
- Explain what and why, not how
- Use conventional commit format

---

## Python Code Style

### Type Hints (Required)

**Always use type hints**:
```python
# ✅ Good
async def create_mandate(
    user_id: UUID,
    intent: MandateIntent,
    constraints: MandateConstraints
) -> Mandate:
    ...

# ❌ Bad
async def create_mandate(user_id, intent, constraints):
    ...
```

**For complex types**:
```python
from typing import Optional, List, Dict, Any

async def get_mandates(
    user_id: UUID
) -> List[Mandate]:
    ...

async def find_by_id(
    mandate_id: UUID
) -> Optional[Mandate]:
    ...
```

### Async/Await (Required)

**All I/O operations must be async**:
```python
# ✅ Good
async def get_mandate(mandate_id: UUID) -> Optional[Mandate]:
    result = await self.session.execute(...)
    return result.scalar_one_or_none()

# ❌ Bad
def get_mandate(mandate_id: UUID) -> Optional[Mandate]:
    result = self.session.execute(...)  # Blocking!
    return result.scalar_one_or_none()
```

### Formatting

**Line Length**: 100 characters max

**Imports**: Organized with `ruff`
```python
# Standard library
from uuid import UUID
from datetime import datetime

# Third-party
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

# Local
from src.backend.features.agents.domain import Mandate
from src.shared_kernel.domain import AggregateRoot
```

**String Quotes**: Double quotes preferred
```python
name: str = "TradingBotAgent"  # ✅
name: str = 'TradingBotAgent'  # ❌
```

### Docstrings

**Use for public APIs and complex logic**:
```python
async def execute_trade(
    self,
    agent_id: UUID,
    symbol: str,
    amount: int
) -> TradeResult:
    """
    Execute a trade for the specified agent.

    Args:
        agent_id: The agent executing the trade
        symbol: Trading pair symbol (e.g., "BTC/USD")
        amount: Amount to trade in smallest unit

    Returns:
        TradeResult containing execution details

    Raises:
        InsufficientFundsError: If mandate limits exceeded
        InvalidAgentError: If agent is not active
    """
    ...
```

---

## DDD Naming Conventions

### Entities
- PascalCase
- Singular nouns
- Examples: `Mandate`, `Agent`, `User`

```python
class Mandate(AggregateRoot):
    ...

class Agent(AggregateRoot):
    ...
```

### Value Objects
- PascalCase
- Descriptive names indicating the value
- Examples: `MandateIntent`, `RiskTolerance`, `EmailAddress`

```python
class MandateIntent(ValueObject):
    ...

class RiskTolerance(ValueObject):
    ...
```

### Domain Events
- PascalCase
- Past tense (what happened)
- Pattern: `{Entity}{Action}`
- Examples: `MandateCreated`, `AgentActivated`, `TradeExecuted`

```python
class MandateCreated(DomainEvent):
    ...

class AgentActivated(DomainEvent):
    ...

class TradeExecuted(DomainEvent):
    ...
```

### Commands
- PascalCase
- Imperative mood (what to do)
- Pattern: `{Verb}{Entity}Command`
- Examples: `CreateMandateCommand`, `SignMandateCommand`, `ActivateAgentCommand`

```python
@dataclass
class CreateMandateCommand:
    user_id: UUID
    intent: MandateIntent
    constraints: MandateConstraints

@dataclass
class SignMandateCommand:
    mandate_id: UUID
    signature: str
```

### Queries
- PascalCase
- Pattern: `Get{Entity}Query` or `List{Entities}Query`
- Examples: `GetMandateQuery`, `GetUserAgentsQuery`

```python
@dataclass
class GetMandateQuery:
    mandate_id: UUID

@dataclass
class GetUserAgentsQuery:
    user_id: UUID
```

### Handlers
- PascalCase
- Pattern: `{CommandOrQuery}Handler`
- Examples: `CreateMandateCommandHandler`, `GetMandateQueryHandler`

```python
class CreateMandateCommandHandler:
    def __init__(self, repository: IMandateRepository):
        self.repository = repository

    async def handle(self, command: CreateMandateCommand) -> UUID:
        ...

class GetMandateQueryHandler:
    def __init__(self, repository: IMandateRepository):
        self.repository = repository

    async def handle(self, query: GetMandateQuery) -> Optional[MandateDTO]:
        ...
```

### Repositories
- PascalCase
- Pattern: `I{Entity}Repository` (interface) or `SQLAlchemy{Entity}Repository` (implementation)
- Examples: `IMandateRepository`, `SQLAlchemyMandateRepository`

```python
# Interface
class IMandateRepository(IRepository[Mandate]):
    async def get_by_user_id(self, user_id: UUID) -> List[Mandate]:
        ...

# Implementation
class SQLAlchemyMandateRepository(IMandateRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
```

### Services
- PascalCase
- Pattern: `{Noun}Service`
- Examples: `ClaudeService`, `BlockchainService`, `AuthenticationService`

```python
class ClaudeService:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

class BlockchainService:
    def __init__(self, rpc_url: str):
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))
```

### API Routes
- snake_case
- RESTful patterns
- Examples: `/api/v1/mandates`, `/api/v1/agents/{id}`

```python
router = APIRouter(prefix="/api/v1/mandates", tags=["mandates"])

@router.post("/", status_code=201)
async def create_mandate(...):
    ...

@router.get("/{mandate_id}")
async def get_mandate(...):
    ...
```

### Pydantic Schemas
- PascalCase
- Pattern: `{Entity}{Request|Response}`
- Examples: `CreateMandateRequest`, `MandateResponse`

```python
class CreateMandateRequest(BaseModel):
    user_id: UUID
    intent: MandateIntentSchema
    constraints: MandateConstraintsSchema

class MandateResponse(BaseModel):
    id: UUID
    user_id: UUID
    status: str
    created_at: datetime
```

---

## File Organization

### Directory Names
- snake_case
- Examples: `domain`, `application`, `infrastructure`, `value_objects`

### File Names
- snake_case
- Singular for single class
- Plural for multiple related items
- Examples: `mandate.py`, `mandate_intent.py`, `mandate_events.py`

### Module Structure
```python
# src/backend/features/agents/domain/entities/mandate.py

"""Mandate aggregate root."""

from uuid import UUID
from datetime import datetime
from typing import Optional

from src.shared_kernel.domain import AggregateRoot
from src.backend.features.agents.domain.events import MandateCreated
from src.backend.features.agents.domain.value_objects import MandateIntent

class Mandate(AggregateRoot):
    """
    Aggregate root for trading mandates.

    A mandate represents a cryptographically signed authorization
    for an agent to execute trades within defined constraints.
    """

    def __init__(
        self,
        id: UUID,
        user_id: UUID,
        intent: MandateIntent,
        ...
    ):
        super().__init__(id)
        self._user_id = user_id
        self._intent = intent
        ...

    @classmethod
    def create(cls, ...) -> "Mandate":
        """Create a new mandate."""
        ...
```

---

## Testing Conventions

### Test File Names
- Pattern: `test_{module_name}.py`
- Examples: `test_mandate.py`, `test_value_objects.py`, `test_api_routes.py`

### Test Function Names
- Pattern: `test_{what}_{condition}_{expected}`
- Use underscores for readability
- Examples:
  - `test_create_mandate_with_valid_data_succeeds`
  - `test_sign_mandate_when_already_signed_raises_error`
  - `test_get_mandate_when_not_found_returns_none`

```python
# tests/unit/backend/features/agents/test_mandate.py

async def test_create_mandate_with_valid_data_succeeds():
    """Test that creating a mandate with valid data succeeds."""
    intent = MandateIntent(...)
    constraints = MandateConstraints(...)

    mandate = Mandate.create(
        user_id=UUID(),
        user_address="0x123...",
        intent=intent,
        constraints=constraints
    )

    assert mandate.user_id is not None
    assert mandate.status == "pending"
    assert len(mandate.get_domain_events()) == 1

async def test_sign_mandate_when_already_signed_raises_error():
    """Test that signing an already signed mandate raises an error."""
    mandate = Mandate.create(...)
    mandate.sign("signature1")

    with pytest.raises(InvalidOperationError):
        mandate.sign("signature2")
```

### Test Organization
```text
tests/
├── unit/
│   └── backend/
│       └── features/
│           └── agents/
│               ├── test_mandate.py          # Entity tests
│               ├── test_agent.py
│               ├── test_value_objects.py    # Value object tests
│               └── test_domain_services.py
└── integration/
    └── backend/
        ├── test_api_routes.py               # API endpoint tests
        └── test_repositories.py             # Database integration tests
```

### Fixtures
- Use descriptive names
- Place common fixtures in `conftest.py`

```python
# tests/conftest.py

import pytest
from uuid import UUID

@pytest.fixture
def valid_mandate_intent():
    """Provide a valid MandateIntent for testing."""
    return MandateIntent(
        risk_tolerance=RiskTolerance.MODERATE,
        max_spend=10000,
        strategy="DCA",
        budget=5000
    )

@pytest.fixture
async def db_session():
    """Provide a test database session."""
    async with get_test_session() as session:
        yield session
```

---

## Error Handling

### Domain Exceptions
- Inherit from `DomainException`
- PascalCase with `Error` suffix
- Examples: `InvalidOperationError`, `EntityNotFoundError`, `ValidationError`

```python
from src.shared_kernel.domain import DomainException

class MandateAlreadySignedError(DomainException):
    """Raised when attempting to sign an already signed mandate."""
    pass

class InsufficientFundsError(DomainException):
    """Raised when mandate spending limit would be exceeded."""
    pass
```

### API Error Responses
```python
from fastapi import HTTPException

@router.get("/{mandate_id}")
async def get_mandate(mandate_id: UUID, ...):
    try:
        mandate = await handler.handle(GetMandateQuery(mandate_id))
        if not mandate:
            raise HTTPException(status_code=404, detail="Mandate not found")
        return mandate
    except DomainException as e:
        raise HTTPException(status_code=400, detail=str(e))
```

---

## Code Quality Checklist

Before committing:

- [ ] All functions have type hints
- [ ] All I/O operations use async/await
- [ ] Code formatted with `uv run black src/ tests/`
- [ ] Linting passed: `uv run ruff check src/ tests/`
- [ ] Type checking passed: `uv run mypy src/`
- [ ] All tests pass: `uv run pytest`
- [ ] Commit message follows conventional commit format
- [ ] No commented-out code
- [ ] No debug print statements
- [ ] Sensitive data not committed (.env in .gitignore)

---

## Anti-Patterns to Avoid

### ❌ Infrastructure in Domain
```python
# ❌ BAD - SQLAlchemy in domain entity
class Mandate(Base):  # Don't inherit from SQLAlchemy Base
    __tablename__ = "mandates"
    ...
```

```python
# ✅ GOOD - Pure domain entity
class Mandate(AggregateRoot):
    def __init__(self, ...):
        ...
```

### ❌ Business Logic in Presentation
```python
# ❌ BAD - Business logic in route
@router.post("/mandates")
async def create_mandate(request: CreateMandateRequest):
    if request.max_spend <= 0:  # Domain validation in API
        raise HTTPException(400, "Invalid amount")
    ...
```

```python
# ✅ GOOD - Validation in domain/value object
class MandateConstraints(ValueObject):
    def __init__(self, max_spend: int):
        if max_spend <= 0:
            raise ValueError("max_spend must be positive")
        ...

@router.post("/mandates")
async def create_mandate(request: CreateMandateRequest, handler = Depends(...)):
    command = CreateMandateCommand(...)
    return await handler.handle(command)
```

### ❌ Anemic Domain Model
```python
# ❌ BAD - Just data, no behavior
class Mandate:
    def __init__(self, ...):
        self.user_id = user_id
        self.status = "pending"

    # No behavior, just getters/setters
```

```python
# ✅ GOOD - Rich domain model
class Mandate(AggregateRoot):
    def sign(self, signature: str) -> None:
        """Sign the mandate and update status."""
        if self._signature:
            raise MandateAlreadySignedError()
        self._signature = signature
        self._status = "signed"
        self.add_domain_event(MandateSigned(self.id, signature))
```

---

## Summary

- **Git commits**: Conventional commit format with type, scope, and subject
- **Python style**: Type hints, async/await, 100-char lines, double quotes
- **DDD naming**: PascalCase for domain objects, descriptive event names
- **Testing**: `test_{what}_{condition}_{expected}` pattern
- **Quality**: Format, lint, type-check, test before committing
- **Package manager**: Always use `uv`, never `pip` or `poetry`
