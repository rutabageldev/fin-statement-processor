# models/transactions.py
from datetime import date
from typing import Literal
from uuid import UUID
from uuid import uuid4

from pydantic import BaseModel


class Transaction(BaseModel):
    id: UUID
    statement_id: UUID
    account_id: UUID
    date: date
    amount: float
    description: str
    custom_description: str | None = None
    category: str | None = None
    type: Literal["debit", "credit", "payment", "refund"]

    @classmethod
    def from_dict(
        cls,
        data: dict,
        statement_id: UUID,
        account_id: UUID,
        transaction_id: UUID | None = None,
    ) -> "Transaction":
        return cls(
            id=transaction_id or uuid4(),
            statement_id=statement_id,
            account_id=account_id,
            date=date.fromisoformat(data["date"]),
            amount=float(data["amount"]),
            description=data["description"],
            custom_description=data.get("custom_description"),
            category=data.get("category"),
            type=data["type"],
        )
