# ADR-003: Technology Stack Selection

**Status:** ACCEPTED
**Date:** 2025-09-06
**Deciders:** Lead Developer

## Context

Ledgerly requires a full-stack technology selection for:

- **Backend API**: REST API server with file processing capabilities
- **Frontend UI**: Interactive web application with charts and forms
- **Database**: Persistent storage for financial data
- **Infrastructure**: Development and deployment environment

Key requirements:

- Strong typing for financial data accuracy
- Excellent testing ecosystem
- Modern developer experience
- Performance suitable for personal use scale
- Learning opportunities with industry-relevant technologies

## Decision

We will use the following technology stack:

**Backend:**

- **Language**: Python 3.12
- **Web Framework**: FastAPI
- **ORM**: SQLAlchemy 2.0 with async support
- **Database**: PostgreSQL 15+
- **Task Queue**: FastAPI BackgroundTasks (MVP), Celery (future)

**Frontend:**

- **Language**: TypeScript
- **Framework**: React 18+ with hooks
- **Build Tool**: Vite
- **CSS Framework**: TailwindCSS
- **Charts**: Recharts
- **Components**: Headless UI (accessibility-focused unstyled components)

**Infrastructure:**

- **Development**: Docker Compose
- **Object Storage**: MinIO (self-hosted S3-compatible)
- **Production**: Self-hosted on local server
- **CI/CD**: GitHub Actions (optional)

## Rationale

**Backend Rationale:**

**Python + FastAPI:**

- Existing codebase already in Python with mature parsing logic
- FastAPI provides excellent async support and automatic API documentation
- Strong typing with Pydantic models aligns with financial data requirements
- Excellent testing ecosystem (pytest, factory_boy, etc.)

**PostgreSQL:**

- ACID compliance essential for financial data integrity
- JSON/JSONB support for flexible metadata storage
- Excellent performance for analytical queries
- Strong ecosystem and tooling

**Frontend Rationale:**

**React + TypeScript + Tailwind:**

- TypeScript ensures type safety across API boundaries
- TailwindCSS provides maximum design flexibility for custom financial dashboards
- Utility-first approach enables rapid prototyping with full control
- Educational value - deepens CSS mastery for long-term skill development
- Headless UI provides accessibility without style constraints
- Recharts works well with custom Tailwind styling

**Infrastructure Rationale:**

**Docker + MinIO + Self-Hosted:**

- Consistent development/production environments with Docker Compose
- Zero ongoing costs - completely self-hosted solution
- MinIO provides S3-compatible API for future cloud migration flexibility
- Full control over data and infrastructure
- Local server deployment eliminates vendor dependencies
- Pre-signed URLs for secure file access (same S3 API)

## Consequences

### Positive

- **Type Safety**: End-to-end typing from database to UI reduces bugs
- **Developer Experience**: Modern tooling with hot reload, debugging, testing
- **Performance**: Async Python + PostgreSQL handles expected load efficiently
- **Self-Documenting**: FastAPI auto-generates interactive API docs with Swagger UI
- **Zero Cost**: Completely free self-hosted architecture with no ongoing expenses
- **Full Control**: Own your data and infrastructure completely
- **CSS Mastery**: TailwindCSS deepens understanding of modern CSS techniques
- **Future Migration**: S3-compatible MinIO enables easy cloud migration later
- **Learning Value**: Industry-standard technologies with broad applicability

### Negative

- **Initial Development Speed**: TailwindCSS requires more upfront styling work than component libraries
- **Server Management**: Self-hosted solution requires local server maintenance
- **No Managed Services**: Manual backup/monitoring responsibilities
- **Learning Curve**: CSS utility classes + React + FastAPI expertise needed
- **Hardware Requirements**: Local server must handle PostgreSQL + MinIO + applications

### Neutral

- **Ecosystem Lock-in**: Committed to React/Python ecosystems but both are stable
- **Migration Paths**: Can incrementally migrate components if needed
- **Scaling**: Architecture can handle growth but may need optimization

## Alternatives Considered

### Option 1: Full Python Stack (Django + HTMX)

- **Description:** Django backend with HTMX for interactive frontend
- **Pros:**
  - Single language across full stack
  - Django admin for data management
  - Simpler deployment
  - HTMX provides modern UX without JavaScript complexity
- **Cons:**
  - Less flexible for complex financial visualizations
  - HTMX learning curve for advanced interactions
  - Django doesn't auto-generate API documentation like FastAPI
  - Limited charting ecosystem compared to React
- **Rejected because:** FastAPI superior for self-documenting APIs, React+TailwindCSS better for custom financial visualizations

### Option 2: Node.js Full Stack

- **Description:** Node.js/Express backend with React frontend
- **Pros:**
  - Single language (JavaScript/TypeScript)
  - Excellent JSON handling
  - Large npm ecosystem
- **Cons:**
  - Need to rewrite existing Python parsing logic
  - Node.js less mature for CPU-intensive file processing
  - Python ecosystem superior for data processing
- **Rejected because:** Would require rewriting substantial existing Python codebase

### Option 3: Go + React

- **Description:** Go backend API with React frontend
- **Pros:**
  - Excellent performance
  - Strong typing in both layers
  - Simple deployment (single binary)
- **Cons:**
  - Need to rewrite all existing Python code
  - Less mature ecosystem for PDF parsing
  - Go learning curve
- **Rejected because:** Substantial rewrite required, Python better for data processing

## Implementation Notes

**Development Environment:**

- Docker Compose with separate services for backend/frontend/database
- Hot reload enabled for both frontend and backend
- Shared networking for API communication

**Production Deployment:**

- Backend deployed as Docker container
- Frontend built as static assets served by backend or CDN
- PostgreSQL as managed database service
- Environment-based configuration

**Migration Strategy:**

- Phase 1: Keep existing Python parsing logic, add FastAPI wrapper
- Phase 2: Implement full REST API with proper error handling
- Phase 3: Build React frontend consuming APIs
- Phase 4: Add production deployment and monitoring

## Related Decisions

- Builds on ADR-001 (Monorepo) for unified development experience
- Supports ADR-002 (API-driven) with FastAPI's excellent REST capabilities
- Future decisions needed on specific component libraries and deployment details

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Python Web Framework Comparison](https://realpython.com/python-web-framework-comparison/)

---

_This document follows the [MADR template](https://adr.github.io/madr/)_
