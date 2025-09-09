"""Account model for user financial accounts."""

from uuid import UUID

from sqlalchemy import Boolean
from sqlalchemy import CheckConstraint
from sqlalchemy import ForeignKey
from sqlalchemy import Index
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base import Base
from .base import TimestampMixin
from .base import UUIDMixin


class Account(Base, UUIDMixin, TimestampMixin):
    """User's financial accounts."""

    __tablename__ = "accounts"

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    institution_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("institutions.id", ondelete="RESTRICT"),
        nullable=False,
    )
    account_type_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("account_types.id", ondelete="RESTRICT"),
        nullable=False,
    )
    account_number_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    nickname: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    currency: Mapped[str] = mapped_column(
        String(3),
        default="USD",
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # Relationships
    user = relationship("User", back_populates="accounts")
    institution = relationship("Institution", back_populates="accounts")
    account_type = relationship("AccountType", back_populates="accounts")
    statements = relationship(
        "Statement", back_populates="account", cascade="all, delete-orphan"
    )
    transactions = relationship(
        "Transaction", back_populates="account", cascade="all, delete-orphan"
    )
    credit_card_details = relationship(
        "CreditCardDetail", back_populates="account", cascade="all, delete-orphan"
    )

    # Constraints
    __table_args__ = (
        CheckConstraint("currency ~* '^[A-Z]{3}$'", name="accounts_currency_valid"),
        UniqueConstraint("user_id", "account_number_hash"),
        Index("idx_accounts_user_id", "user_id"),
        Index("idx_accounts_institution_id", "institution_id"),
        Index("idx_accounts_account_type_id", "account_type_id"),
        Index("idx_accounts_active", "is_active"),
    )

    def __repr__(self) -> str:
        """Return string representation of Account."""
        return f"<Account(id={self.id}, nickname={self.nickname}, currency={self.currency})>"
