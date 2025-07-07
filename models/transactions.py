# models/transactions.py
from pydantic import BaseModel, Field
from typing import Optional, Literal
from uuid import UUID
from datetime import date


class Transaction(BaseModel):
    id: UUID
    statement_id: UUID
    account_id: UUID
    date: date
    amount: float
    description: str
    custom_description: Optional[str] = None
    category: Optional[str] = None
    type: Literal["debit", "credit", "payment", "refund"]
