# ADR-005: Implement Integrated Secrets Management (SecureVault)

**Status:** ACCEPTED
**Date:** 2025-09-07
**Deciders:** Project Lead, Claude Code Assistant

## Context

Ledgerly currently has 12+ hardcoded secrets across configuration files including database passwords, JWT keys, MinIO credentials, and Redis passwords. These are stored in plain text in `.env` files and `docker-compose.yml`, creating security vulnerabilities and operational challenges.

As a self-hosted personal finance application handling sensitive financial data, proper secrets management is critical. However, external solutions like HashiCorp Vault add significant operational complexity for a single-developer, self-hosted application.

Key forces in tension:

- **Security Need:** Must protect sensitive credentials and keys
- **Operational Simplicity:** Self-hosted app should be simple to deploy and maintain
- **Development Workflow:** Secrets management shouldn't complicate development
- **Financial Data Privacy:** Extra security layer for sensitive financial information

## Decision

We will implement **SecureVault**, an integrated secrets management system built directly into Ledgerly that provides vault-like functionality without external dependencies.

## Rationale

**Why build integrated secrets management:**

1. **Operational Simplicity:** No external infrastructure to manage
2. **Self-Contained:** All secrets management within the application
3. **Development Friendly:** Works seamlessly in dev, staging, and production
4. **Web-Based Management:** Simple UI for non-technical secret rotation
5. **Container Integration:** Direct injection into Docker services
6. **Financial App Security:** Extra protection layer for sensitive financial data

**Why not external vault solutions:**

- HashiCorp Vault: Too complex for single-developer self-hosted app
- Cloud KMS: Introduces cloud dependencies and costs
- File-based solutions: Still leave secrets on disk

## Consequences

### Positive

- **Enhanced Security:** Encrypted storage of all application secrets
- **Zero External Dependencies:** No additional infrastructure required
- **Web-Based Management:** Admin UI for secret rotation and management
- **Development Workflow:** Seamless secret injection in all environments
- **Audit Trail:** Built-in logging of secret access and modifications
- **Auto-Rotation Capability:** Programmatic secret rotation for JWT keys, etc.
- **Container Integration:** Direct secret injection without file mounts

### Negative

- **Implementation Complexity:** Additional code to maintain and test
- **Single Point of Failure:** All secrets depend on master key security
- **Development Time:** Delays other Phase 2 features slightly
- **Backup Dependency:** Must ensure encrypted secret backups
- **Key Management:** Master key security becomes critical

### Neutral

- **Storage Overhead:** Minimal database storage for encrypted secrets
- **API Surface:** Additional `/api/v1/admin/secrets` endpoints
- **Admin Interface:** New admin panel for secret management
- **Migration Required:** One-time migration of existing hardcoded secrets

## Alternatives Considered

### Option 1: HashiCorp Vault

- **Description:** Industry-standard external secrets management
- **Pros:** Battle-tested, extensive features, industry standard
- **Cons:** Complex setup, operational overhead, overkill for single app
- **Rejected because:** Too much operational complexity for self-hosted personal app

### Option 2: Cloud-Based KMS (AWS/GCP/Azure)

- **Description:** Use cloud provider key management services
- **Pros:** Managed service, enterprise-grade security
- **Cons:** Cloud dependency, recurring costs, complexity
- **Rejected because:** Violates self-hosted principle and adds external dependencies

### Option 3: File-Based Secrets with Docker Secrets

- **Description:** Use Docker secrets or encrypted files
- **Pros:** Docker-native approach, simpler than external vault
- **Cons:** Still leaves secrets on disk, limited rotation capability
- **Rejected because:** Limited functionality and still vulnerable to file access

### Option 4: Environment Variable Encryption

- **Description:** Encrypt individual environment variables
- **Pros:** Minimal changes to current setup
- **Cons:** No central management, difficult rotation, limited audit trail
- **Rejected because:** Doesn't solve management and rotation challenges

## Implementation Notes

**Phase Integration:**

- Add to **Phase 2** (Backend API) deliverables
- Implement before other Phase 2 features to secure the foundation

**Technical Architecture:**

```python
# Core SecureVault Service
backend/services/secure_vault/
├── __init__.py
├── vault.py          # Main SecureVault class
├── encryption.py     # AES-256 encryption utilities
├── models.py         # Secret storage data models
├── rotation.py       # Auto-rotation capabilities
└── admin_api.py      # Admin management endpoints
```

**Database Schema:**

```sql
CREATE TABLE secrets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) UNIQUE NOT NULL,
    encrypted_value TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    rotation_policy JSONB,
    access_count INTEGER DEFAULT 0
);

CREATE TABLE secret_audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    secret_name VARCHAR(255) NOT NULL,
    action VARCHAR(50) NOT NULL, -- 'READ', 'WRITE', 'ROTATE', 'DELETE'
    user_id UUID REFERENCES users(id),
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    ip_address INET
);
```

**API Endpoints:**

- `POST /api/v1/admin/secrets` - Create secret
- `GET /api/v1/admin/secrets` - List secrets (names only)
- `PUT /api/v1/admin/secrets/{name}` - Update secret
- `DELETE /api/v1/admin/secrets/{name}` - Delete secret
- `POST /api/v1/admin/secrets/{name}/rotate` - Rotate secret

**Master Key Strategy:**

- Environment variable `LEDGERLY_MASTER_KEY` (required)
- 256-bit AES key for secret encryption
- Must be provided at application startup
- Consider future: Hardware security module integration

**Migration Plan:**

1. Implement SecureVault core functionality
2. Create migration script to move existing secrets
3. Update all service configurations to use SecureVault
4. Remove hardcoded secrets from config files
5. Add admin UI for secret management

## Related Decisions

- **ADR-001:** Monorepo architecture enables integrated secrets management
- **ADR-003:** Technology stack selection (FastAPI, PostgreSQL) supports secure storage
- **Future ADR:** Will need decision on backup encryption strategy

## References

- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [NIST SP 800-57: Key Management Guidelines](https://csrc.nist.gov/publications/detail/sp/800-57-part-1/rev-5/final)
- [Docker Secrets Documentation](https://docs.docker.com/engine/swarm/secrets/)
- [FastAPI Security Best Practices](https://fastapi.tiangolo.com/tutorial/security/)

---

_This document is based on the [MADR template](https://adr.github.io/madr/)_
