"""Transaction data models for financial operations."""

from datetime import date
from typing import Literal
from uuid import UUID
from uuid import uuid4

from pydantic import BaseModel


class Transaction(BaseModel):
    """Represents a financial transaction from a statement.

    Contains transaction details including date, amount, description,
    and categorization information.
    """

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
        """Create Transaction from parsed transaction data.

        Args:
            data: Parsed transaction data containing date, amount, description etc
            statement_id: UUID of the associated statement
            account_id: UUID of the account
            transaction_id: Optional UUID for the transaction (generates new if None)

        Returns:
            Transaction instance with normalized data
        """
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
