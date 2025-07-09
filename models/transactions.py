# models/transactions.py
from pydantic import BaseModel
from typing import Optional, Literal
from uuid import UUID, uuid4
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

    @classmethod
    def from_dict(
        cls,
        data: dict,
        statement_id: UUID,
        account_id: UUID,
        transaction_id: Optional[UUID] = None,
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
