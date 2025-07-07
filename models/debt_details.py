# models/debt_details.py
from pydantic import BaseModel
from uuid import UUID
from datetime import date


class DebtDetails(BaseModel):
    id: UUID
    statement_id: UUID
    payment: float
    min_payment_due: float
    payment_due_date: date
    interest_rate: float
    interest_paid: float
    principal_paid: float


class CreditCardDetails(BaseModel):
    id: UUID
    statement_id: UUID
    credit_limit: float
    available_credit: float
    points_earned: int
    points_redeemed: int
    cash_advances: float
    fees: float
    purchases: float
    credits: float
