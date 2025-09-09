"""Statement detail model for balance and payment information."""

from datetime import date
from decimal import Decimal
from uuid import UUID

from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Index
from sqlalchemy import Numeric
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base import Base
from .base import TimestampMixin
from .base import UUIDMixin


class StatementDetail(Base, UUIDMixin, TimestampMixin):
    """Statement balance and payment information."""

    __tablename__ = "statement_details"

    statement_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("statements.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    previous_balance: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )
    new_balance: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )
    minimum_payment: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )
    due_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    # Relationships
    statement = relationship("Statement", back_populates="statement_detail")

    # Constraints
    __table_args__ = (
        Index("idx_statement_details_statement_id", "statement_id"),
        Index("idx_statement_details_due_date", "due_date"),
    )

    def __repr__(self) -> str:
        """Return string representation of StatementDetail."""
        return f"<StatementDetail(id={self.id}, previous_balance={self.previous_balance}, new_balance={self.new_balance})>"
