# models/statement.py
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import date, datetime


class StatementData(BaseModel):
    id: UUID
    institution_id: UUID
    account_id: UUID
    start_date: date
    end_date: date
    file_url: Optional[str] = None
    uploaded_at: datetime


class StatementDetails(BaseModel):
    id: UUID
    statement_id: UUID
    previous_balance: float
    new_balance: float
