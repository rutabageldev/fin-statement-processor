"""Statement data models for financial documents processing."""

from datetime import UTC
from datetime import date
from datetime import datetime
from uuid import UUID
from uuid import uuid4

from pydantic import BaseModel


class StatementData(BaseModel):
    """Represents core statement data from financial documents.

    Contains metadata about statement periods, file locations,
    and references to institution/account information.
    """

    id: UUID
    institution_id: UUID
    account_id: UUID
    period_start: date
    period_end: date
    file_url: str | None = None
    uploaded_at: datetime

    @classmethod
    def from_dict(
        cls,
        data: dict,
        institution_id: UUID,
        account_id: UUID,
        file_url: str | None = None,
        uploaded_at: datetime | None = None,
        statement_id: UUID | None = None,
    ) -> "StatementData":
        return cls(
            id=statement_id or uuid4(),
            institution_id=institution_id,
            account_id=account_id,
            period_start=date.fromisoformat(data["bill_period_start"]),
            period_end=date.fromisoformat(data["bill_period_end"]),
            file_url=file_url,
            uploaded_at=uploaded_at or datetime.now(UTC),
        )


class StatementDetails(BaseModel):
    id: UUID
    statement_id: UUID
    previous_balance: float
    new_balance: float

    @classmethod
    def from_dict(
        cls,
        data: dict,
        statement_id: UUID,
        detail_id: UUID | None = None,
    ) -> "StatementDetails":
        """Create StatementDetails from parsed balance data.

        Args:
            data: Parsed statement data containing balance information
            statement_id: UUID of the associated statement
            detail_id: Optional UUID for the details (generates new if None)

        Returns:
            StatementDetails instance with balance data
        """
        return cls(
            id=detail_id or uuid4(),
            statement_id=statement_id,
            previous_balance=data["previous_balance"],
            new_balance=data["new_balance"],
        )
