# models/statement.py
from datetime import UTC
from datetime import date
from datetime import datetime
from uuid import UUID
from uuid import uuid4

from pydantic import BaseModel


class StatementData(BaseModel):
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
        return cls(
            id=detail_id or uuid4(),
            statement_id=statement_id,
            previous_balance=data["previous_balance"],
            new_balance=data["new_balance"],
        )
