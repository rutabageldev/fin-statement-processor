"""Statement model for financial statement periods and metadata."""

from datetime import date
from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import CheckConstraint
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Index
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base
from .base import TimestampMixin
from .base import UUIDMixin


class Statement(Base, UUIDMixin, TimestampMixin):
    """Financial statement periods and metadata."""

    __tablename__ = "statements"

    account_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("accounts.id", ondelete="CASCADE"),
        nullable=False,
    )
    period_start: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
    period_end: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
    file_pdf_url: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    file_csv_url: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        default="pending",
        nullable=False,
    )
    processing_metadata: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        default=dict,
        nullable=False,
    )
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.current_timestamp(),
        nullable=False,
    )
    processed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Relationships
    account = relationship("Account", back_populates="statements")
    statement_detail = relationship(
        "StatementDetail",
        back_populates="statement",
        uselist=False,
        cascade="all, delete-orphan",
    )
    transactions = relationship(
        "Transaction", back_populates="statement", cascade="all, delete-orphan"
    )
    credit_card_detail = relationship(
        "CreditCardDetail",
        back_populates="statement",
        uselist=False,
        cascade="all, delete-orphan",
    )

    # Constraints
    __table_args__ = (
        CheckConstraint("period_end >= period_start", name="statements_period_valid"),
        CheckConstraint(
            "status IN ('pending', 'processing', 'completed', 'failed')",
            name="statements_status_valid",
        ),
        CheckConstraint(
            "file_pdf_url IS NOT NULL OR file_csv_url IS NOT NULL",
            name="statements_files_required",
        ),
        UniqueConstraint("account_id", "period_start", "period_end"),
        Index("idx_statements_account_id", "account_id"),
        Index("idx_statements_period", "period_start", "period_end"),
        Index("idx_statements_status", "status"),
        Index("idx_statements_uploaded_at", "uploaded_at"),
        Index(
            "idx_statements_processing_metadata",
            "processing_metadata",
            postgresql_using="gin",
        ),
    )

    def __repr__(self) -> str:
        """Return string representation of Statement."""
        return f"<Statement(id={self.id}, period={self.period_start} to {self.period_end}, status={self.status})>"
