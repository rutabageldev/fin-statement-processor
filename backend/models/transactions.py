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
        data: dict[str, object],
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
            date=date.fromisoformat(str(data["date"])),
            amount=float(data["amount"]),  # type: ignore[arg-type]
            description=str(data["description"]),
            custom_description=str(data["custom_description"])
            if data.get("custom_description") is not None
            else None,
            category=str(data["category"])
            if data.get("category") is not None
            else None,
            type=str(data["type"]),  # type: ignore[arg-type]
        )
