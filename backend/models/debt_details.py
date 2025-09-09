"""Debt and payment detail models."""

from datetime import date
from uuid import UUID
from uuid import uuid4

from pydantic import BaseModel


class DebtDetails(BaseModel):
    """Debt and payment details from statements.

    Contains payment information, interest rates, and
    other debt-related details.
    """

    id: UUID
    account_id: UUID
    statement_id: UUID
    payments: float
    min_payment_due: float
    payment_due_date: date
    interest_rate: float
    interest_paid: float
    principal_paid: float

    @classmethod
    def from_dict(
        cls,
        data: dict[str, object],
        account_id: UUID,
        statement_id: UUID,
        debt_detail_id: UUID | None = None,
    ) -> "DebtDetails":
        """Create DebtDetails from parsed debt data.

        Args:
            data: Parsed statement data containing debt information
            account_id: UUID of the account
            statement_id: UUID of the associated statement
            debt_detail_id: Optional UUID for the details (generates new if None)

        Returns:
            DebtDetails instance with debt data
        """
        payments = float(data.get("payments", 0.0))  # type: ignore[arg-type]
        interest_paid = float(data.get("interest_paid", 0.0))  # type: ignore[arg-type]
        principal_paid = abs(payments) - interest_paid
        return cls(
            id=debt_detail_id or uuid4(),
            account_id=account_id,
            statement_id=statement_id,
            payments=payments,
            min_payment_due=float(data["min_payment_due"]),  # type: ignore[arg-type]
            payment_due_date=date.fromisoformat(str(data["payment_due_date"])),
            interest_rate=float(data["interest_rate"]),  # type: ignore[arg-type]
            interest_paid=interest_paid,
            principal_paid=round(principal_paid, 2),
        )
