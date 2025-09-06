# ADR-002: Choose API-Driven Over Event-Driven Architecture

**Status:** ACCEPTED
**Date:** 2025-09-06
**Deciders:** Lead Developer

## Context

Ledgerly needs to define the communication pattern between its components:

- Frontend client requesting data and submitting files
- Backend processing files and managing data
- Database storing processed financial information

Two primary architectural patterns were considered:

1. **API-Driven**: Traditional REST API with synchronous request/response
2. **Event-Driven**: Asynchronous messaging using RedPanda/Kafka for decoupled communication

The original plan included using RedPanda (Kafka-compatible) as a learning opportunity, but analysis showed potential architectural misalignment.

## Decision

We will implement an API-driven architecture using REST endpoints with FastAPI for the MVP, with the following characteristics:

- **Synchronous APIs** for immediate operations (user queries, file uploads)
- **Async processing** within the backend for long-running tasks (file parsing)
- **WebSocket connections** for real-time status updates during processing
- **Traditional database queries** for data retrieval

Event-driven patterns will be reconsidered post-MVP for specific use cases like real-time notifications or external integrations.

## Rationale

**MVP Requirements Analysis:**
The core user flow is: Upload → Parse → Store → Visualize

This is fundamentally a request-response pattern:

- User uploads file and expects immediate feedback
- User queries data and expects immediate results
- Processing status needs real-time updates (WebSocket is better fit than events)

**Technical Factors:**

1. **Simplicity**: REST APIs are well-understood and have extensive tooling
2. **Development Speed**: Faster to implement and debug than distributed messaging
3. **Error Handling**: Easier to handle and propagate errors in synchronous flows
4. **Testing**: Simpler integration testing without message queue complexity
5. **Single Developer**: No need for decoupling that benefits large teams

## Consequences

### Positive

- **Faster Development**: Well-established patterns and tooling
- **Simpler Debugging**: Request tracing through synchronous calls
- **Immediate Feedback**: Real-time error responses and validation
- **Lower Operational Overhead**: Fewer infrastructure components to manage
- **Better Testing**: Straightforward API testing without message queue setup
- **Familiar Patterns**: Standard REST API patterns widely documented

### Negative

- **Missed Learning Opportunity**: Won't gain experience with event-driven systems
- **Tight Coupling**: Frontend directly coupled to backend API contracts
- **Scaling Limitations**: May need refactoring for high-throughput scenarios
- **Processing Blocks**: Long file processing may impact API responsiveness

### Neutral

- **Future Migration Path**: Can introduce events for specific use cases later
- **Async Processing**: Still use async patterns within backend components
- **Real-time Updates**: WebSocket provides real-time capabilities where needed

## Alternatives Considered

### Option 1: Event-Driven with RedPanda

- **Description:** Use RedPanda/Kafka for asynchronous messaging between components
- **Pros:**
  - Excellent learning opportunity for distributed systems
  - Decoupled architecture with independent scaling
  - Built-in durability and replay capabilities
  - Event sourcing possibilities for audit trails
- **Cons:**
  - Massive over-engineering for file upload → database → display flow
  - Additional infrastructure complexity (RedPanda cluster, schema registry)
  - Debugging complexity with asynchronous message flows
  - Error handling complexity across distributed components
  - No clear business justification for eventual consistency
- **Rejected because:** Introduces unnecessary complexity without solving actual business problems for the MVP scope

### Option 2: Hybrid Approach (API + Events)

- **Description:** REST APIs for queries, events for background processing
- **Pros:**
  - Best of both worlds
  - Events only where beneficial
  - REST for immediate operations
- **Cons:**
  - Architecture complexity with two communication patterns
  - Need to maintain both message queue and API infrastructure
  - Unclear boundaries between sync/async operations
- **Rejected because:** Adds complexity without clear benefits at current scale

## Implementation Notes

**Phase 2 Implementation:**

- FastAPI with async/await for non-blocking operations
- Background tasks using FastAPI's BackgroundTasks or Celery
- WebSocket endpoints for real-time processing status
- Standard HTTP status codes and error responses

**File Processing Flow:**

```
1. POST /api/v1/statements (returns 202 Accepted with processing ID)
2. WebSocket connection for real-time status updates
3. Background task processes files asynchronously
4. Results stored in database
5. Frontend polls or receives WebSocket updates
```

**Future Event-Driven Opportunities:**

- Real-time notifications (account balance alerts)
- External system integrations (Plaid webhooks)
- Audit log streaming
- Analytics and reporting pipeline

## Related Decisions

- Supports ADR-001 (Monorepo) by simplifying inter-component communication
- Future decision needed on background task processing (Celery vs FastAPI BackgroundTasks)
- Future decision on real-time notification patterns

## References

- [REST API Design Best Practices](https://restfulapi.net/)
- [FastAPI Async Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/)
- [When to Use Event-Driven Architecture](https://martinfowler.com/articles/201701-event-driven.html)
- [Choosing Between REST and Events](https://www.confluent.io/blog/when-to-use-rest-vs-messaging/)

---

_This document follows the [MADR template](https://adr.github.io/madr/)_
