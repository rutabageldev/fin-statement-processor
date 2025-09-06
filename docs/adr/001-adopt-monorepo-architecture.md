# ADR-001: Adopt Monorepo Architecture

**Status:** ACCEPTED
**Date:** 2025-09-06
**Deciders:** Lead Developer

## Context

Ledgerly is a personal finance webapp consisting of multiple components:

- Python backend for file processing and API
- React frontend for user interface
- PostgreSQL database for data persistence
- Shared configuration and deployment files

The codebase was initially structured as a single Python microservice. As we expand to include frontend and database components, we need to decide on the overall repository and deployment architecture.

Key constraints:

- Single developer project (personal/hobby)
- Rapid iteration and development velocity desired
- Simplified deployment and maintenance preferred
- Future scalability should be considered but not over-engineered

## Decision

We will adopt a monorepo architecture with all components (backend, frontend, infrastructure) in a single repository with the following structure:

```
ledgerly/
├── backend/          # Python FastAPI application
├── frontend/         # React TypeScript application
├── database/         # PostgreSQL schemas and migrations
├── docs/            # Documentation
├── scripts/         # Build and deployment scripts
├── docker-compose.yml
└── README.md
```

## Rationale

**Primary factors:**

1. **Development Velocity**: Single developer can make atomic changes across all components
2. **Operational Simplicity**: One repository to manage, deploy, and version
3. **Consistency**: Shared tooling, linting, and CI/CD configuration
4. **Refactoring Safety**: Cross-component changes can be made atomically

**Alignment with Project Goals:**

- Hobby project with emphasis on learning and rapid iteration
- Personal use means no need for independent team scaling
- Simplified deployment aligns with single-developer constraints

## Consequences

### Positive

- **Atomic Changes**: Can modify backend API and frontend consumers in single commit
- **Simplified CI/CD**: Single pipeline handles testing and deployment of all components
- **Shared Configuration**: Common linting, formatting, and quality tools
- **Easier Development**: No dependency management between repositories
- **Simplified Deployment**: Single Docker compose file for entire application

### Negative

- **Repository Size**: Will grow larger over time with multiple components
- **Build Complexity**: Need to handle different technology stacks in one build
- **Tool Conflicts**: May have conflicting tooling requirements between frontend/backend
- **Future Scaling**: May need to split if team grows significantly

### Neutral

- **Technology Isolation**: Still maintain clear boundaries between components
- **Deployment Options**: Can still deploy components independently if needed
- **Version Management**: Single version for entire application

## Alternatives Considered

### Option 1: Separate Repositories (Multi-repo)

- **Description:** Maintain separate repositories for backend, frontend, and infrastructure
- **Pros:**
  - Clear separation of concerns
  - Independent versioning and deployment
  - Technology-specific tooling
  - Standard enterprise pattern
- **Cons:**
  - Coordination overhead between repositories
  - Complex cross-component changes
  - Multiple CI/CD pipelines to maintain
  - Dependency version management complexity
- **Rejected because:** Adds unnecessary complexity for single-developer project without clear benefits

### Option 2: Microservice Architecture

- **Description:** Deploy components as separate services with independent scaling
- **Pros:**
  - Independent scaling and deployment
  - Technology flexibility
  - Fault isolation
- **Cons:**
  - Network latency and complexity
  - Distributed system challenges (monitoring, debugging)
  - Over-engineering for personal project scale
  - Operational overhead for single developer
- **Rejected because:** Massive over-engineering for current scale and requirements

## Implementation Notes

- **Phase 1**: Restructure existing Python code into `/backend` directory
- **Phase 3**: Add `/frontend` directory with React application
- **Migration Strategy**: Gradual restructure with maintaining working state at each step
- **Build System**: Use Docker compose for local development, single deployment unit
- **CI/CD**: Single GitHub Actions workflow with parallel jobs for different components

## Related Decisions

- Related to ADR-002 (API-driven architecture) - monorepo enables easier API contract management
- Future decision needed on deployment strategy (single container vs separate containers)

## References

- [Monorepo Explained](https://monorepo.tools/)
- [Google's Monorepo Philosophy](https://research.google/pubs/pub45424/)
- [Advantages and Disadvantages of a Monorepo](https://circleci.com/blog/monorepo-dev-practices/)

---

_This document follows the [MADR template](https://adr.github.io/madr/)_
