"""SecureVault secret storage models."""

from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .base import Base
from .base import TimestampMixin
from .base import UUIDMixin


class Secret(Base, UUIDMixin, TimestampMixin):
    """Encrypted secret storage model."""

    __tablename__ = "secrets"

    # Secret identification
    name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
        comment="Unique secret name/key",
    )

    # Encrypted secret value
    encrypted_value: Mapped[str] = mapped_column(
        Text, nullable=False, comment="AES-256-GCM encrypted secret value"
    )

    # Metadata
    description: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="Human-readable description of the secret"
    )

    # Rotation and access tracking
    rotation_policy: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB, nullable=True, comment="JSON policy for automatic rotation"
    )

    access_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="Number of times this secret has been accessed",
    )

    last_accessed_at: Mapped[datetime | None] = mapped_column(
        nullable=True, comment="Timestamp of last secret access"
    )

    # Security metadata
    key_fingerprint: Mapped[str | None] = mapped_column(
        String(16),
        nullable=True,
        comment="Fingerprint of master key used for encryption",
    )

    def __repr__(self) -> str:
        """String representation of Secret model."""
        return f"<Secret(name='{self.name}', created_at='{self.created_at}')>"


class SecretAuditLog(Base, UUIDMixin):
    """Audit log for secret operations."""

    __tablename__ = "secret_audit_log"

    # Reference to secret
    secret_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
        comment="Name of the secret that was accessed",
    )

    # Audit information
    action: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="Action performed: READ, WRITE, ROTATE, DELETE",
    )

    # Request context
    user_id: Mapped[UUID | None] = mapped_column(
        nullable=True, comment="User who performed the action (if authenticated)"
    )

    ip_address: Mapped[str | None] = mapped_column(
        INET, nullable=True, comment="IP address of the request"
    )

    user_agent: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="User agent string"
    )

    # Timing
    timestamp: Mapped[datetime] = mapped_column(
        nullable=False,
        default=datetime.utcnow,
        index=True,
        comment="When the action occurred",
    )

    # Additional context
    details: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB, nullable=True, comment="Additional context about the operation"
    )

    def __repr__(self) -> str:
        """String representation of SecretAuditLog model."""
        return f"<SecretAuditLog(secret_name='{self.secret_name}', action='{self.action}', timestamp='{self.timestamp}')>"
