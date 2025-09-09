"""Credit card detail model for credit card specific information."""

from decimal import Decimal
from uuid import UUID

from sqlalchemy import CheckConstraint
from sqlalchemy import ForeignKey
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base import Base
from .base import TimestampMixin
from .base import UUIDMixin


class CreditCardDetail(Base, UUIDMixin, TimestampMixin):
    """Credit card specific information."""

    __tablename__ = "credit_card_details"

    account_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("accounts.id", ondelete="CASCADE"),
        nullable=False,
    )
    statement_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("statements.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    credit_limit: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )
    available_credit: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )
    points_earned: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    points_redeemed: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    cash_advances: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0,
        nullable=False,
    )
    fees: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0,
        nullable=False,
    )
    purchases: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0,
        nullable=False,
    )
    credits: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0,
        nullable=False,
    )

    # Relationships
    account = relationship("Account", back_populates="credit_card_details")
    statement = relationship("Statement", back_populates="credit_card_detail")

    # Constraints
    __table_args__ = (
        CheckConstraint("credit_limit >= 0", name="cc_details_credit_limit_positive"),
        CheckConstraint(
            "available_credit <= credit_limit", name="cc_details_available_credit_valid"
        ),
        CheckConstraint(
            "points_earned >= 0 AND points_redeemed >= 0",
            name="cc_details_points_non_negative",
        ),
        Index("idx_cc_details_account_id", "account_id"),
        Index("idx_cc_details_statement_id", "statement_id"),
    )

    def __repr__(self) -> str:
        """Return string representation of CreditCardDetail."""
        return f"<CreditCardDetail(id={self.id}, credit_limit={self.credit_limit}, available_credit={self.available_credit})>"
