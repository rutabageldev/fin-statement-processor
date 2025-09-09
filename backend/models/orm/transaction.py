"""Transaction model for individual financial transactions."""

from datetime import date
from decimal import Decimal
from uuid import UUID

from sqlalchemy import CheckConstraint
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Index
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base import Base
from .base import TimestampMixin
from .base import UUIDMixin


class Transaction(Base, UUIDMixin, TimestampMixin):
    """Individual financial transactions."""

    __tablename__ = "transactions"

    statement_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("statements.id", ondelete="CASCADE"),
        nullable=False,
    )
    account_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("accounts.id", ondelete="CASCADE"),
        nullable=False,
    )
    transaction_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    custom_description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    category: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    transaction_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    reference_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # Relationships
    statement = relationship("Statement", back_populates="transactions")
    account = relationship("Account", back_populates="transactions")

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "transaction_type IN ('debit', 'credit', 'payment', 'refund')",
            name="transactions_type_valid",
        ),
        CheckConstraint("amount != 0", name="transactions_amount_not_zero"),
        Index("idx_transactions_statement_id", "statement_id"),
        Index("idx_transactions_account_id", "account_id"),
        Index("idx_transactions_date", "transaction_date"),
        Index("idx_transactions_amount", "amount"),
        Index("idx_transactions_category", "category"),
        Index("idx_transactions_type", "transaction_type"),
        Index(
            "idx_transactions_description_search",
            "description",
            postgresql_using="gin",
            postgresql_ops={"description": "gin_trgm_ops"},
        ),
        Index(
            "idx_transactions_custom_description_search",
            "custom_description",
            postgresql_using="gin",
            postgresql_ops={"custom_description": "gin_trgm_ops"},
        ),
    )

    def __repr__(self) -> str:
        """Return string representation of Transaction."""
        return f"<Transaction(id={self.id}, date={self.transaction_date}, amount={self.amount}, type={self.transaction_type})>"
