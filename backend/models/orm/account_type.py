"""Account type model for different account configurations."""

from typing import Any

from sqlalchemy import CheckConstraint
from sqlalchemy import Index
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base import Base
from .base import TimestampMixin
from .base import UUIDMixin


class AccountType(Base, UUIDMixin, TimestampMixin):
    """Account type definitions and parser configurations."""

    __tablename__ = "account_types"

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    slug: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    parser_config: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        default=dict,
        nullable=False,
    )

    # Relationships
    accounts = relationship("Account", back_populates="account_type")

    # Constraints
    __table_args__ = (
        CheckConstraint("slug ~* '^[a-z0-9_-]+$'", name="account_types_slug_format"),
        Index("idx_account_types_slug", "slug"),
        Index(
            "idx_account_types_parser_config", "parser_config", postgresql_using="gin"
        ),
    )

    def __repr__(self) -> str:
        """Return string representation of AccountType."""
        return f"<AccountType(id={self.id}, name={self.name}, slug={self.slug})>"
