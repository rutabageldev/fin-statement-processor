# 🔄 Ledgerly Development Workflow

## Overview

This document defines the development workflow, coding standards, and deployment processes for Ledgerly. The workflow is designed to be simple for single-developer use while being scalable for future contributors.

**Philosophy**: Quality over speed, automation over manual processes, documentation over tribal knowledge.

---

## 🌿 Git Workflow

### **Branch Strategy: GitHub Flow**

We use a simplified GitHub Flow strategy optimized for continuous deployment:

```
main (production-ready)
  ├── feature/user-authentication
  ├── feature/api-endpoints
  ├── bugfix/transaction-parsing
  └── hotfix/security-patch
```

### **Branch Types**

- **`main`**: Production-ready code, always deployable
- **`feature/*`**: New features or enhancements
- **`bugfix/*`**: Bug fixes for non-critical issues
- **`hotfix/*`**: Critical fixes that need immediate deployment
- **`chore/*`**: Maintenance tasks, dependency updates, refactoring

### **Branch Naming Convention**

```bash
feature/add-plaid-integration
feature/monthly-spending-charts
bugfix/fix-csv-parsing-error
hotfix/security-vulnerability-fix
chore/upgrade-python-dependencies
```

---

## 💻 Local Development Setup

### **Prerequisites**

```bash
# Required software
- Docker Desktop
- Git
- VS Code (recommended)
- Node.js 18+ (for frontend development in Phase 3+)
```

### **First-Time Setup**

```bash
# 1. Clone repository
git clone https://github.com/your-username/ledgerly.git
cd ledgerly

# 2. Copy environment file
cp .env.example .env

# 3. Start development environment
docker-compose up -d

# 4. Install pre-commit hooks
docker-compose exec parser pre-commit install

# 5. Run initial tests
docker-compose exec parser pytest

# 6. Verify setup
curl http://localhost:8000/api/v1/health
```

### **Daily Development**

```bash
# Start full development environment (backend + frontend + MinIO + PostgreSQL)
docker-compose up -d

# Backend development
docker-compose exec backend pytest                    # Run Python tests
docker-compose exec backend ruff check .              # Python linting
docker-compose exec backend ruff format .             # Python formatting
docker-compose exec backend mypy .                    # Type checking

# Frontend development (when added in Phase 3)
docker-compose exec frontend npm test                 # Run frontend tests
docker-compose exec frontend npm run build            # Build for production

# Check MinIO file storage
curl http://localhost:9000/minio/health/live          # MinIO health check

# Stop environment
docker-compose down
```

---

## 📝 Coding Standards

### **Code Quality Requirements**

- **Test Coverage**: Minimum 90% for new code
- **Type Hints**: Required for all function signatures
- **Documentation**: Docstrings for all public APIs
- **Linting**: All ruff checks must pass
- **Security**: All bandit security checks must pass

### **File Organization**

```
backend/
├── api/                    # FastAPI routes and endpoints
│   ├── v1/                # API version 1
│   └── dependencies.py    # Shared dependencies
├── core/                  # Core configuration and utilities
├── models/                # SQLAlchemy models
├── schemas/               # Pydantic schemas
├── services/              # Business logic
├── tests/                 # Test files
└── alembic/              # Database migrations

frontend/
├── src/
│   ├── components/       # React components
│   ├── pages/           # Page components
│   ├── hooks/           # Custom hooks
│   ├── services/        # API calls
│   └── utils/           # Utility functions
└── public/              # Static assets
```

### **Naming Conventions**

#### **Python (Backend)**

```python
# Files: snake_case
user_service.py
transaction_repository.py

# Classes: PascalCase
class UserService:
class TransactionRepository:

# Functions/Variables: snake_case
def get_user_by_id():
user_count = 10

# Constants: UPPER_SNAKE_CASE
MAX_FILE_SIZE = 10_000_000
DEFAULT_CURRENCY = "USD"
```

#### **TypeScript (Frontend)**

```typescript
// Files: kebab-case
user - profile.component.tsx;
transaction - list.tsx;

// Components: PascalCase
function UserProfile() {}
const TransactionList = () => {};

// Functions/Variables: camelCase
const getUserProfile = () => {};
const transactionCount = 10;

// Constants: UPPER_SNAKE_CASE
const MAX_FILE_SIZE = 10_000_000;
```

---

## 🔀 Development Process

### **Feature Development Workflow**

#### **1. Create Feature Branch**

```bash
# Create and checkout feature branch
git checkout -b feature/add-transaction-filtering

# Push branch to remote
git push -u origin feature/add-transaction-filtering
```

#### **2. Development Cycle**

```bash
# Make changes
# Write tests first (TDD approach recommended)
# Run tests frequently
docker-compose exec parser pytest tests/

# Commit frequently with clear messages
git add .
git commit -m "feat: add transaction filtering by date range

- Add date range filters to transaction API
- Implement filtering logic in TransactionService
- Add validation for date range parameters
- Add unit tests for filtering functionality

Closes #123"

# Push regularly
git push
```

#### **3. Pre-Merge Checklist**

Before creating a pull request, ensure:

```bash
# ✅ All tests pass
docker-compose exec parser pytest

# ✅ Code quality checks pass
docker-compose exec parser ruff check .
docker-compose exec parser ruff format --check .
docker-compose exec parser mypy .

# ✅ Security scan passes
docker-compose exec parser bandit -r .

# ✅ Pre-commit hooks pass
docker-compose exec parser pre-commit run --all-files

# ✅ Manual testing completed
# Test the feature end-to-end in development environment

# ✅ Documentation updated
# Update API docs, README, or other relevant docs
```

#### **4. Pull Request**

```bash
# Create pull request on GitHub
gh pr create --title "Add transaction filtering by date range" \
  --body "## Summary
- Implements date range filtering for transactions API
- Adds validation and error handling
- Includes comprehensive test coverage

## Testing
- [ ] Unit tests pass
- [ ] Manual testing completed
- [ ] API documentation updated

Closes #123"
```

#### **5. Code Review & Merge**

- **Self-review**: Review your own code first
- **Automated checks**: Ensure all CI checks pass
- **Manual verification**: Test the feature locally
- **Merge strategy**: Squash merge for clean history

---

## 🧪 Testing Strategy

### **Testing Pyramid**

```
               /\
              /  \
          E2E Tests (Few)
         /            \
        /              \
    Integration Tests   \
   /                    \
  /                      \
Unit Tests (Many)         \
```

### **Test Types**

#### **Unit Tests** (90% of tests)

```python
# Location: tests/unit/
# Purpose: Test individual functions/classes in isolation
# Tools: pytest, pytest-asyncio, factory_boy

def test_calculate_monthly_spending():
    # Arrange
    transactions = create_test_transactions()

    # Act
    result = calculate_monthly_spending(transactions)

    # Assert
    assert result.total_spending == 1500.00
    assert len(result.categories) == 3
```

#### **Integration Tests** (8% of tests)

```python
# Location: tests/integration/
# Purpose: Test component interactions (API + Database)
# Tools: pytest, httpx, test database

async def test_upload_statement_endpoint():
    # Test complete API endpoint with database
    async with AsyncClient(app=app) as client:
        response = await client.post(
            "/api/v1/statements",
            files={"pdf_file": test_pdf_content},
            data={"account_type": "citi_cc"}
        )
    assert response.status_code == 201
```

#### **End-to-End Tests** (2% of tests) - Phase 4+

```python
# Location: tests/e2e/
# Purpose: Test complete user workflows
# Tools: Playwright

def test_upload_and_view_statement_flow():
    # Test complete user journey from upload to visualization
    page.goto("http://localhost:3000")
    page.click("#upload-button")
    page.upload_file("#file-input", "test-statement.pdf")
    page.click("#submit-button")

    # Verify data appears in dashboard
    expect(page.locator("#transaction-count")).to_have_text("42")
```

### **Test Configuration**

#### **pytest.ini**

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    --verbose
    --tb=short
    --strict-markers
    --disable-warnings
    --cov=src
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=90
```

#### **Test Database Setup**

```python
# conftest.py
@pytest.fixture(scope="session")
async def test_db():
    # Create test database
    engine = create_test_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Cleanup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
```

---

## 🤖 Continuous Integration

### **GitHub Actions Workflow**

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Run code quality checks
        run: |
          ruff check .
          ruff format --check .
          mypy .
          bandit -r .

      - name: Run tests
        run: |
          pytest --cov=src --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

### **Pre-commit Configuration**

```yaml
# .pre-commit-config.yaml (already exists, but enhanced)
repos:
  # ... existing hooks ...

  # Additional quality gates
  - repo: local
    hooks:
      - id: pytest-check
        name: pytest-check
        entry: pytest tests/ -x -v
        language: system
        pass_filenames: false
        always_run: true

      - id: coverage-check
        name: coverage-check
        entry: pytest --cov=src --cov-fail-under=90
        language: system
        pass_filenames: false
        always_run: true
```

---

## 🚀 Deployment Process

### **Environment Strategy**

- **Development**: Local Docker Compose (backend + frontend + MinIO + PostgreSQL)
- **Staging**: Same local server, separate docker-compose.staging.yml
- **Production**: Self-hosted on local server with docker-compose.prod.yml

### **Deployment Pipeline**

#### **Phase 1-3: Local Development**

```bash
# Build and test
docker-compose build
docker-compose up -d

# Run full test suite
docker-compose exec parser pytest

# Manual testing
curl http://localhost:8000/api/v1/health
```

#### **Phase 4+: Self-Hosted Production Deployment**

```bash
# Production deployment on local server
git pull origin main

# Build and deploy with production configuration
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# Run migrations
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head

# Verify deployment
curl https://your-domain.com/api/v1/health
```

**Production docker-compose.prod.yml features:**

- Persistent volumes for PostgreSQL and MinIO data
- Environment-specific configuration
- Resource limits and restart policies
- HTTPS setup with Let's Encrypt (optional)
- Backup scripts for database and files

### **Database Migrations**

```bash
# Create migration
alembic revision --autogenerate -m "Add user authentication"

# Apply migrations
alembic upgrade head

# Rollback if needed
alembic downgrade -1
```

---

## 📋 Definition of Done Checklist

### **For All Changes**

- [ ] Code follows style guidelines (ruff, mypy pass)
- [ ] All tests pass (unit, integration)
- [ ] Test coverage ≥ 90% for new code
- [ ] Security scan passes (bandit)
- [ ] Documentation updated (docstrings, API docs)
- [ ] Self-code review completed
- [ ] Manual testing completed

### **For Features**

- [ ] Feature works as specified
- [ ] Error cases handled gracefully
- [ ] API documentation updated
- [ ] Database migrations tested
- [ ] Performance acceptable (<500ms API responses)

### **For Bug Fixes**

- [ ] Root cause identified and documented
- [ ] Fix verified manually
- [ ] Regression test added
- [ ] Related documentation updated

### **For Database Changes**

- [ ] Migration script tested
- [ ] Rollback plan documented
- [ ] Performance impact assessed
- [ ] Backup procedure verified

---

## 🔧 Tools and Configuration

### **Development Tools**

- **IDE**: VS Code with Python, TypeScript extensions
- **Linting**: Ruff (replaces flake8, isort, black)
- **Type Checking**: mypy for Python, TypeScript compiler
- **Testing**: pytest (Python), Jest (JavaScript)
- **Database**: PostgreSQL with pgAdmin
- **API Testing**: curl, Postman, or HTTPie

### **VS Code Settings**

```json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.formatting.provider": "ruff",
  "python.testing.pytestEnabled": true,
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  }
}
```

---

## 🎯 Phase-Specific Workflows

### **Phase 1: Monorepo Setup**

```bash
# 1. Create new branch
git checkout -b feature/monorepo-restructure

# 2. Create directory structure
mkdir -p {backend,frontend,docs,scripts}

# 3. Move existing code
mv !(backend|frontend|docs|scripts) backend/

# 4. Update Docker configuration
# Update docker-compose.yml for multi-service setup

# 5. Test everything still works
docker-compose up -d
pytest
```

### **Phase 2: API Development**

```bash
# 1. API-first development
# - Define OpenAPI spec first
# - Generate client stubs
# - Implement endpoints
# - Write tests

# 2. Database-first development
# - Create migration
# - Update models
# - Write repository layer
# - Add integration tests
```

### **Phase 3: Frontend Development**

```bash
# 1. Component-driven development
# - Create Storybook stories
# - Build components in isolation
# - Write unit tests
# - Integration with API
```

---

## 📚 Resources

### **Documentation**

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0 Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/)
- [pytest Documentation](https://docs.pytest.org/)
- [React Documentation](https://react.dev/)

### **Code Quality**

- [Python Code Quality Tools](https://realpython.com/python-code-quality/)
- [Clean Architecture in Python](https://breadcrumbscollector.tech/python-the-clean-architecture-in-2021/)
- [API Design Guidelines](https://restfulapi.net/)

---

_Last Updated: September 6, 2025_
_Workflow Version: 1.0_
