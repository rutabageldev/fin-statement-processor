# models/statement.py
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4
from datetime import date, datetime


class StatementData(BaseModel):
    id: UUID
    institution_id: UUID
    account_id: UUID
    start_date: date
    end_date: date
    file_url: Optional[str] = None
    uploaded_at: datetime

    @classmethod
    def from_dict(
        cls,
        data: dict,
        institution_id: UUID,
        account_id: UUID,
        file_url: Optional[str] = None,
        uploaded_at: Optional[datetime] = None,
        statement_id: Optional[UUID] = None,
    ) -> "StatementData":
        return cls(
            id=statement_id or uuid4(),
            institution_id=institution_id,
            account_id=account_id,
            start_date=date.fromisoformat(data["bill_period_start"]),
            end_date=date.fromisoformat(data["bill_period_end"]),
            file_url=file_url,
            uploaded_at=uploaded_at or datetime.utcnow(),
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
        detail_id: Optional[UUID] = None,
    ) -> "StatementDetails":
        return cls(
            id=detail_id or uuid4(),
            statement_id=statement_id,
            previous_balance=data["previous_balance"],
            new_balance=data["new_balance"],
        )
