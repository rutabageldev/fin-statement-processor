# Ledgerly - Personal Finance Management Platform

## Project Overview

Ledgerly is a full-stack web application for personal finance management that processes financial statements and transactions from multiple sources. The platform provides secure data storage, parsing capabilities, and visualization tools for financial analysis.

**Architecture**: Monorepo with React frontend, FastAPI backend, PostgreSQL database, and integrated secrets management.

## Key Architecture

### **Frontend** (`/frontend/`)

- **Framework**: React 18 with TypeScript and Vite
- **Styling**: TailwindCSS with custom design system
- **Components**: Modular component architecture
- **UI Library**: Headless UI for accessibility

### **Backend** (`/backend/`)

- **API**: FastAPI with automatic OpenAPI documentation
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Storage**: MinIO S3-compatible object storage
- **Caching**: Redis for session and data caching
- **Security**: SecureVault integrated secrets management (see ADR-005)

### **Services Architecture**

- **Parser Engine**: Account-specific parsing logic (`services/parsers/`)
- **Data Models**: Transaction and statement models (`models/`)
- **Account Registry**: Multi-provider account configuration (`registry/`)
- **Logging**: Structured logging with configurable levels

## Development Environment

### **Host Environment**

- **Platform**: Ubuntu WSL2 on Windows 11
- **Development Model**: Host-based multi-container development
- **IDE**: VSCode/Cursor running natively on host (no dev containers)

### **Container Services** (via `docker compose`)

- **Backend**: Python 3.12 with FastAPI (localhost:8000)
- **Frontend**: Node.js with Vite dev server (localhost:3000)
- **Database**: PostgreSQL 15 (localhost:5432)
- **Object Storage**: MinIO (localhost:9000/9001)
- **Cache**: Redis 7 (localhost:6379)

### **Quality Tools**

- **Code Formatting**: Ruff (replaces Black)
- **Linting**: Ruff with custom configuration
- **Type Checking**: MyPy with strict settings
- **Security**: Bandit + safety for vulnerability scanning
- **Secrets Detection**: detect-secrets with baseline
- **Testing**: pytest with comprehensive test suite
- **Pre-commit**: Automated quality checks on all commits

## Common Commands

### **Development Workflow**

```bash
# Start all services
make up
# or: docker compose up -d

# View service status
make status

# Access service shells
make shell-backend    # Backend development
make shell-frontend   # Frontend development
make shell-postgres   # Database access

# View logs
make logs
# or: docker compose logs -f [service-name]

# Run tests
make test
# or: docker compose exec backend pytest

# Stop services
make down
```

### **Legacy Parser (CLI Mode)**

```bash
# Access backend container for CLI parsing
make shell-backend
python main.py --account citi_cc --pdf ./path/to/statement.pdf --csv ./path/to/transactions.csv
```

## Development Notes

### **Current Status**

- **Phase 1 Complete**: Multi-container development environment
- **Phase 2 Ready**: Backend API development with SecureVault integration
- **Architecture**: Host-based development with containerized services

### **Key Features**

- **Secrets Management**: SecureVault provides encrypted secret storage
- **Multi-container**: All services isolated and orchestrated via Docker Compose
- **Hot Reload**: Both frontend and backend support live reloading
- **Quality Gates**: Comprehensive pre-commit hooks and testing
- **Self-hosted**: Designed for personal deployment without cloud dependencies

### **Security**

- **SecureVault**: Integrated secrets management with AES-256 encryption
- **Container Isolation**: Services run in isolated Docker containers
- **Secret Injection**: Runtime secret injection from encrypted storage
- **Audit Logging**: Comprehensive security event logging

## File Structure

### **Root Level**

- `docker-compose.yml` - Multi-service orchestration
- `Makefile` - Development workflow commands
- `PRODUCT_ROADMAP.md` - Development phases and goals
- `.env` - Development environment configuration

### **Backend** (`/backend/`)

- `app.py` - FastAPI application entry point
- `main.py` - Legacy CLI parser interface
- `services/` - Core services and parsers
- `models/` - SQLAlchemy data models
- `api/` - FastAPI route definitions
- `tests/` - Comprehensive test suite
- `Dockerfile.dev` - Development container definition

### **Frontend** (`/frontend/`)

- `src/` - React application source
- `src/components/` - Reusable UI components
- `src/pages/` - Application pages/routes
- `package.json` - Node.js dependencies
- `tailwind.config.js` - TailwindCSS configuration
- `Dockerfile.dev` - Development container definition

### **Documentation** (`/docs/`)

- `adr/` - Architecture Decision Records
- `API_SPECIFICATION.md` - Complete API documentation
- `DATABASE_SCHEMA.md` - Database design and schema
- `DEVELOPMENT_WORKFLOW.md` - Development processes

## Coding Conventions

### **General**

- **Type Safety**: TypeScript for frontend, type hints for Python backend
- **Code Quality**: Ruff formatting and linting for Python, Prettier for TypeScript
- **Testing**: Comprehensive unit and integration tests required
- **Documentation**: Docstrings for all public APIs and complex functions
- **Error Handling**: Graceful error handling with structured logging

### **Python Backend**

- **Style**: Ruff (black-compatible) formatting with PEP 8 compliance
- **Imports**: Absolute imports preferred, organized by type
- **Type Hints**: Required for all function signatures and complex variables
- **Async**: Use async/await for I/O operations

### **TypeScript Frontend**

- **Components**: Functional components with TypeScript interfaces
- **Styling**: TailwindCSS utility classes, custom design tokens
- **State**: React hooks for local state, context for shared state
- **API**: Typed API client with automatic request/response validation

## Next Steps

See `PRODUCT_ROADMAP.md` for detailed development phases. Currently ready for **Phase 2: Backend API** implementation including SecureVault integration.
