# 🚀 Ledgerly Product Roadmap

## Executive Summary

Ledgerly is a personal finance webapp designed to ingest, process, and visualize financial data from multiple sources including direct API connections (Plaid) and manual file uploads (PDFs, CSVs). This roadmap outlines the path to MVP and beyond.

**Current State**: Robust Python parsing microservice with comprehensive testing and quality tooling
**Target MVP**: Full-stack application supporting file upload, data processing, database storage, and basic visualizations
**Architecture**: Monorepo with React frontend, Python backend, PostgreSQL database

---

## 🎯 MVP Definition

**Core User Flow**:

1. Upload Citi credit card statement (PDF) and transactions (CSV) simultaneously
2. Automatic parsing and normalization of financial data
3. Data persistence in PostgreSQL database
4. Basic visualizations: monthly spend breakdown and category trends

**Success Criteria**:

- Complete end-to-end flow working reliably
- Responsive web interface
- Data accuracy validated against source documents
- Sub-5-second processing for typical files

---

## 🏗️ Architecture Decisions

### **Decision 1: Monorepo Structure** ✅

- **Rationale**: Single developer, simplified deployment, atomic changes across components
- **Structure**: `/frontend` (React), `/backend` (Python), shared Docker compose

### **Decision 2: API-Driven Architecture** ✅

- **Rationale**: Traditional REST API approach over event-driven for MVP simplicity
- **Future**: Consider event-driven for real-time features post-MVP

### **Decision 3: Technology Stack**

- **Frontend**: React with TypeScript, Vite build tool, TailwindCSS styling
- **Backend**: FastAPI (Python), SQLAlchemy ORM, PostgreSQL
- **Object Storage**: MinIO (self-hosted S3-compatible) for secure file storage
- **Infrastructure**: Docker compose for development, self-hosted deployment

---

## 📋 Phase-Based Roadmap

### **Phase 1: Foundation & Cleanup** (Sprint 1) - **HIGH PRIORITY**

_Duration: 1-2 weeks_

#### Goals

- Clean up completed technical debt
- Establish monorepo structure
- Implement database layer
- Set up development workflow

#### Deliverables

- ✅ Remove technical debt roadmap (completed)
- [ ] Monorepo restructure (`/frontend`, `/backend` directories)
- [ ] PostgreSQL integration with SQLAlchemy models
- [ ] Database migrations system
- [ ] Updated Docker compose for multi-service development
- [ ] Development workflow documentation

#### Definition of Done

- All existing tests pass
- Database models created and tested
- Local development environment fully functional
- Documentation updated

---

### **Phase 2: Backend API** (Sprint 2-3) - **HIGH PRIORITY**

_Duration: 2-3 weeks_

#### Goals

- Create RESTful API endpoints
- Implement integrated secrets management (SecureVault)
- Implement file upload handling
- Build data aggregation services

#### Deliverables

- [ ] **SecureVault Integration** (see ADR-005):
  - [ ] Core SecureVault service with AES-256 encryption
  - [ ] Secret storage database schema and models
  - [ ] Admin API endpoints (`/api/v1/admin/secrets`)
  - [ ] Migration of existing hardcoded secrets
  - [ ] Runtime secret injection for all services
  - [ ] Secret rotation capabilities for JWT keys
- [ ] FastAPI application setup
- [ ] Core API endpoints:
  - `POST /api/v1/statements` - Upload and parse files
  - `GET /api/v1/statements` - List statements with pagination
  - `GET /api/v1/statements/{id}` - Get statement details
  - `GET /api/v1/transactions` - Get transactions with filtering
- [ ] File upload middleware with MinIO integration
- [ ] MinIO setup with S3-compatible API and pre-signed URLs
- [ ] Async processing pipeline for large files
- [ ] File security (virus scanning, configurable encryption)
- [ ] Data aggregation services:
  - Monthly spend breakdown
  - Category trend analysis
- [ ] Self-documenting API with FastAPI (automatic Swagger UI at /docs)
- [ ] Comprehensive API testing suite

#### Definition of Done

- **SecureVault fully operational** with all secrets migrated from hardcoded values
- All API endpoints tested and documented
- File upload supports expected formats and sizes
- Data aggregation accurate and performant
- 95%+ test coverage for new code
- API security best practices implemented
- **Zero hardcoded secrets** remaining in configuration files

---

### **Phase 3: Frontend Foundation** (Sprint 4) - **HIGH PRIORITY**

_Duration: 2-3 weeks_

#### Goals

- Create React application
- Implement core user interface
- Build basic data visualizations

#### Deliverables

- [ ] React application with TypeScript and Vite
- [ ] TailwindCSS setup with custom design system
- [ ] Headless UI components for accessibility
- [ ] File upload interface with custom styling and progress indicators
- [ ] Dashboard for viewing parsed statements
- [ ] Data visualization components:
  - Monthly spend breakdown (Recharts with custom Tailwind styling)
  - Category trends (Recharts line charts with Tailwind themes)
- [ ] **SecureVault Admin UI**:
  - [ ] Secret management interface (`/admin/secrets`)
  - [ ] Secret creation and editing forms
  - [ ] Secret rotation controls
  - [ ] Audit log display
- [ ] Responsive design with Tailwind breakpoints
- [ ] Dark mode implementation with Tailwind's dark mode utilities
- [ ] Custom toast notifications and error handling UI
- [ ] Frontend testing setup (Jest, React Testing Library)

#### Definition of Done

- Complete user flow from upload to visualization
- **SecureVault admin interface fully functional** with secret management capabilities
- Responsive design tested on mobile/desktop
- Error states handled gracefully
- Frontend tests covering critical paths
- Performance optimized (< 3s initial load)

---

### **Phase 4: MVP Polish** (Sprint 5) - **MEDIUM PRIORITY**

_Duration: 1-2 weeks_

#### Goals

- End-to-end integration testing
- Production readiness
- Basic security implementation

#### Deliverables

- [ ] End-to-end testing automation (Playwright/Cypress)
- [ ] Production Docker configuration
- [ ] **SecureVault Production Hardening**:
  - [ ] Encrypted secret backups
  - [ ] Master key rotation procedures
  - [ ] Secret audit reporting
  - [ ] Security scanning integration
- [ ] Basic authentication system
- [ ] Error monitoring and logging
- [ ] Performance monitoring
- [ ] Deployment documentation

#### Definition of Done

- Complete E2E test suite passing
- Production environment configured
- Security audit completed
- Monitoring dashboards functional
- Deployment process documented

---

### **Phase 5: Post-MVP Enhancements** (Future) - **LOW PRIORITY**

#### Goals

- Enhanced functionality and user experience
- Advanced data processing
- External integrations

#### Potential Features

- [ ] Plaid integration for direct account connections
- [ ] Advanced visualizations (custom date ranges, comparison views)
- [ ] Data export functionality (CSV, PDF reports)
- [ ] Multiple account type support
- [ ] Mobile app (React Native)
- [ ] Real-time notifications (event-driven architecture)
- [ ] Machine learning categorization improvements

---

## ✅ Definition of Done

### **Code Quality Standards**

- [ ] All new code has comprehensive unit tests (90%+ coverage)
- [ ] Integration tests for API endpoints
- [ ] End-to-end tests for critical user flows (Phase 4+)
- [ ] Code review completed by maintainer
- [ ] All automated quality checks passing (ruff, mypy, prettier)
- [ ] No security vulnerabilities (bandit, safety)

### **Documentation Requirements**

- [ ] Function/class docstrings for all public APIs
- [ ] API endpoint documentation (OpenAPI)
- [ ] README updates for setup/usage changes
- [ ] Architecture decision records for significant changes

### **Testing Automation**

- [ ] **Phase 1-3**: Unit and integration tests required
- [ ] **Phase 4+**: End-to-end testing automation
- [ ] All tests pass in CI/CD pipeline
- [ ] Performance benchmarks maintained

### **Deployment Readiness**

- [ ] Feature works in production-like environment
- [ ] Database migrations tested and documented
- [ ] Environment configuration documented
- [ ] Rollback plan documented for significant changes

### **User Experience**

- [ ] Error states handled gracefully with user-friendly messages
- [ ] Loading states implemented for async operations
- [ ] Responsive design tested on mobile and desktop
- [ ] Accessibility standards met (WCAG 2.1 AA)

---

## 📊 Success Metrics

### **Technical Metrics**

- **Test Coverage**: >90% for critical code paths
- **Performance**: API responses <500ms, frontend <3s load time
- **Reliability**: 99.9% uptime, zero data loss
- **Security**: Zero critical vulnerabilities

### **User Experience Metrics**

- **File Processing**: <5 seconds for typical statement files
- **Error Rate**: <1% processing failures
- **User Flow**: Complete upload-to-visualization in <30 seconds

### **Development Velocity**

- **Build Time**: <2 minutes for full test suite
- **Deployment**: <5 minutes from commit to production
- **Developer Onboarding**: <30 minutes from clone to running locally

---

## 📋 Pre-Phase 1 Documentation Requirements

Before starting Phase 1, we should establish:

1. **API Specification** - OpenAPI schema for all planned endpoints
2. **Database Schema** - ERD and migration strategy
3. **Development Workflow** - Git flow, code review process, deployment pipeline
4. **Architecture Decision Records** - Document key technical decisions
5. **Contributing Guidelines** - Standards for future contributors
6. **Security Guidelines** - Data handling, authentication, authorization approach

---

## 🎯 Next Actions

1. **Immediate (This Sprint)**:
   - [ ] Create pre-Phase 1 documentation
   - [ ] Set up project structure for documentation
   - [ ] Define API contracts and database schema

2. **Phase 1 Preparation**:
   - [ ] Monorepo restructure planning
   - [ ] Docker compose architecture design
   - [ ] Database migration strategy

3. **Long-term Planning**:
   - [ ] CI/CD pipeline design
   - [ ] Production hosting strategy
   - [ ] Performance monitoring approach

---

_Last Updated: September 6, 2025_
_Current Phase: Pre-Phase 1 Documentation_
