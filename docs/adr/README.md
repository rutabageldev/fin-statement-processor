# 📋 Architecture Decision Records (ADRs)

This directory contains Architecture Decision Records for Ledgerly. ADRs document the significant architectural decisions made during the development of the project.

## What are ADRs?

Architecture Decision Records (ADRs) are short text documents that capture important architectural decisions made during a project, along with their context and consequences. They help us:

- **Remember why** decisions were made
- **Understand the context** when decisions were made
- **Track the evolution** of our architecture over time
- **Onboard new team members** (even if it's just future you!)

## ADR Format

We follow the [MADR (Markdown Architectural Decision Records)](https://adr.github.io/madr/) template format. Each ADR includes:

- **Context**: The forces at play and the situation requiring a decision
- **Decision**: What was decided (in active voice)
- **Rationale**: Why this decision was made
- **Consequences**: Positive, negative, and neutral outcomes
- **Alternatives Considered**: Other options and why they were rejected

## Current ADRs

| #                                                              | Status      | Title                                            | Date       | Summary                                                                |
| -------------------------------------------------------------- | ----------- | ------------------------------------------------ | ---------- | ---------------------------------------------------------------------- |
| [000](000-template.md)                                         | Template    | ADR Template                                     | 2025-09-06 | Template for creating new ADRs                                         |
| [001](001-adopt-monorepo-architecture.md)                      | ✅ Accepted | Adopt Monorepo Architecture                      | 2025-09-06 | Use single repository for all components vs separate repositories      |
| [002](002-choose-api-driven-over-event-driven-architecture.md) | ✅ Accepted | Choose API-Driven Over Event-Driven Architecture | 2025-09-06 | Use REST APIs instead of event-driven messaging for MVP                |
| [003](003-technology-stack-selection.md)                       | ✅ Accepted | Technology Stack Selection                       | 2025-09-06 | Python/FastAPI backend, React/TypeScript frontend, PostgreSQL database |
| [004](004-choose-tailwindcss-over-component-libraries.md)      | ✅ Accepted | Choose TailwindCSS Over Component Libraries      | 2025-09-06 | Use TailwindCSS for styling flexibility and learning value             |

## Creating New ADRs

When making significant architectural decisions:

1. Copy the [template](000-template.md) to a new file
2. Use the next sequential number: `004-your-decision-title.md`
3. Fill out all sections completely
4. Get review and approval (even from future you!)
5. Update this README with the new ADR

### Naming Convention

- Use sequential numbers: `001`, `002`, `003`, etc.
- Use kebab-case for titles: `adopt-monorepo-architecture`
- Be specific and descriptive: `choose-database-technology` not `database-choice`

### When to Create an ADR

Create an ADR when making decisions about:

- **Architecture patterns** (monorepo vs multi-repo, API vs events)
- **Technology selections** (frameworks, databases, tools)
- **Design principles** (authentication approach, error handling strategy)
- **Infrastructure choices** (deployment strategy, hosting platform)
- **Breaking changes** (API versioning, data migrations)

### Status Values

- **PROPOSED**: Decision under consideration
- **ACCEPTED**: Decision approved and ready for implementation
- **DEPRECATED**: Decision no longer recommended but still in use
- **SUPERSEDED**: Decision replaced by a newer ADR

## Future ADRs

Planned ADRs for upcoming decisions:

- **ADR-005**: Authentication and Authorization Strategy (Phase 4)
- **ADR-006**: File Storage and Processing Strategy with MinIO
- **ADR-007**: Self-Hosted Deployment and Infrastructure Strategy
- **ADR-008**: Monitoring and Observability Approach
- **ADR-009**: API Versioning Strategy
- **ADR-010**: Data Backup and Recovery Strategy

## Guidelines

### Writing Good ADRs

- **Be Specific**: "We will use PostgreSQL" not "We will use a database"
- **Include Context**: Explain the situation that required the decision
- **Show Your Work**: Document alternatives considered and why they were rejected
- **Think About Future You**: Will someone understand this decision in 6 months?
- **Keep It Concise**: Aim for 1-2 pages maximum

### Common Pitfalls to Avoid

- **Don't Document Every Decision**: Only significant architectural choices
- **Don't Skip Alternatives**: Show you considered other options
- **Don't Write Novels**: Keep it focused and actionable
- **Don't Forget to Update Status**: Mark ADRs as superseded when replaced

## References

- [ADR GitHub Organization](https://adr.github.io/) - Templates and best practices
- [Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) - Original ADR concept
- [MADR Template](https://adr.github.io/madr/) - The template format we use
- [When to Write an ADR](https://github.com/joelparkerhenderson/architecture_decision_record#when-to-write-an-architecture-decision-record)

---

_This directory is maintained as part of the Ledgerly documentation suite._
