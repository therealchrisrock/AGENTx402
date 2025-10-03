# 🚀 Command Reference

All project commands are defined in `pyproject.toml` and can be run using `uv` or standard Python tools.

## 📦 Installation

```bash
# Install uv (if not already installed)
pip install uv

# Install all dependencies
uv sync

# Install with dev dependencies
uv sync --dev
```

## 🏃 Running Services

### Backend API

```bash
uv run uvicorn src.backend.main:app --reload --host 0.0.0.0 --port 8000
```

Access at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Telegram Bot

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

## 🔍 Code Quality

### Formatting

```bash
# Format all code
uv run black src/ tests/

# Check formatting without changes
uv run black --check src/ tests/
```

### Linting

```bash
# Lint code
uv run ruff check src/ tests/

# Auto-fix issues
uv run ruff check --fix src/ tests/
```

### Type Checking

```bash
# Run type checker
uv run mypy src/
```

### All Checks (format, lint, type-check, test)

```bash
# Using hatch (if installed)
hatch run check

# Manual
uv run black src/ tests/ && \
uv run ruff check src/ tests/ && \
uv run mypy src/ && \
uv run pytest
```

## 🗄️ Database Migrations

### Run Migrations

```bash
# Apply all pending migrations
uv run alembic upgrade head
```

### Create Migration

```bash
# Auto-generate migration
uv run alembic revision --autogenerate -m "Add user table"

# Create empty migration
uv run alembic revision -m "Custom migration"
```

### Rollback

```bash
# Rollback one migration
uv run alembic downgrade -1

# Rollback to specific revision
uv run alembic downgrade <revision>

# Rollback all
uv run alembic downgrade base
```

### View Migration History

```bash
# Show current revision
uv run alembic current

# Show migration history
uv run alembic history
```

## 🐳 Docker

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
```

## 🧹 Cleanup

```bash
# Remove cache files
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete
rm -rf .pytest_cache .coverage htmlcov .mypy_cache .ruff_cache
```

## 🔧 Development Workflow

### Daily Development

```bash
# 1. Start database
docker-compose up postgres redis

# 2. Run migrations
uv run alembic upgrade head

# 3. Start backend (in one terminal)
uv run uvicorn src.backend.main:app --reload

# 4. Start bot (in another terminal)
uv run python -m src.telegram_bot.main
```

### Before Committing

```bash
# Format, lint, type-check, and test
uv run black src/ tests/
uv run ruff check --fix src/ tests/
uv run mypy src/
uv run pytest
```

### Creating a Feature

```bash
# 1. Create feature branch
git checkout -b feat/my-feature

# 2. Write tests first
# Create tests/unit/backend/test_my_feature.py

# 3. Implement feature
# Create src/backend/features/my_feature/

# 4. Run tests
uv run pytest tests/unit/backend/test_my_feature.py

# 5. Check code quality
uv run black src/ tests/
uv run ruff check src/ tests/
uv run mypy src/

# 6. Commit
git add .
git commit -m "feat(my-feature): add my feature"
```

## 🎯 Quick Reference

| Task | Command |
|------|---------|
| Install deps | `uv sync --dev` |
| Run backend | `uv run uvicorn src.backend.main:app --reload` |
| Run bot | `uv run python -m src.telegram_bot.main` |
| Run tests | `uv run pytest` |
| Format code | `uv run black src/ tests/` |
| Lint code | `uv run ruff check src/ tests/` |
| Type check | `uv run mypy src/` |
| Migrate DB | `uv run alembic upgrade head` |
| Docker up | `docker-compose up -d` |
| Docker down | `docker-compose down` |

## 📚 Additional Commands

### Python REPL with Project Context

```bash
# IPython with project loaded
uv run ipython

# In IPython:
from src.backend.features.agents.domain.entities import Mandate, Agent
from src.backend.features.agents.domain.value_objects import MandateIntent
# ... explore your code
```

### Database Shell

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U postgres -d tradingbotagent

# Or using DATABASE_URL from .env
psql $DATABASE_URL
```

### Redis CLI

```bash
# Connect to Redis
docker-compose exec redis redis-cli

# Or locally
redis-cli
```

### View Logs

```bash
# Backend logs
docker-compose logs -f backend

# Bot logs
docker-compose logs -f telegram_bot

# All logs
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail=100 backend
```

## 🐛 Debugging

### Run with Debugger

```bash
# Backend with debugger
uv run python -m debugpy --listen 5678 --wait-for-client -m uvicorn src.backend.main:app --reload

# Bot with debugger
uv run python -m debugpy --listen 5679 --wait-for-client -m src.telegram_bot.main
```

### Verbose Logging

```bash
# Set DEBUG=true in .env
echo "DEBUG=true" >> .env

# Or inline
DEBUG=true uv run backend
```

---

**Pro Tip:** Add `alias uvr="uv run"` to your shell profile for shorter commands!

```bash
# Then you can use:
uvr pytest
uvr uvicorn src.backend.main:app --reload
uvr python -m src.telegram_bot.main
```
