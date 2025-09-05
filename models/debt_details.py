# models/debt_details.py
from datetime import date
from uuid import UUID
from uuid import uuid4

from pydantic import BaseModel


class DebtDetails(BaseModel):
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
        data: dict,
        account_id: UUID,
        statement_id: UUID,
        debt_detail_id: UUID | None = None,
    ) -> "DebtDetails":
        payments = data.get("payments", 0.0)
        interest_paid = data.get("interest_paid", 0.0)
        principal_paid = abs(payments) - interest_paid
        return cls(
            id=debt_detail_id or uuid4(),
            account_id=account_id,
            statement_id=statement_id,
            payments=payments,
            min_payment_due=data["min_payment_due"],
            payment_due_date=date.fromisoformat(data["payment_due_date"]),
            interest_rate=data["interest_rate"],
            interest_paid=interest_paid,
            principal_paid=round(principal_paid, 2),
        )
