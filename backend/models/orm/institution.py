"""Institution model for financial institutions."""

from sqlalchemy import CheckConstraint
from sqlalchemy import Index
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base import Base
from .base import TimestampMixin
from .base import UUIDMixin


class Institution(Base, UUIDMixin, TimestampMixin):
    """Financial institutions (banks, credit card companies)."""

    __tablename__ = "institutions"

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    slug: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )
    website: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    logo_url: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # Relationships
    accounts = relationship("Account", back_populates="institution")

    # Constraints
    __table_args__ = (
        CheckConstraint("slug ~* '^[a-z0-9_-]+$'", name="institutions_slug_format"),
        Index("idx_institutions_slug", "slug"),
    )

    def __repr__(self) -> str:
        """Return string representation of Institution."""
        return f"<Institution(id={self.id}, name={self.name}, slug={self.slug})>"
