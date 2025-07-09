import pytest
from uuid import uuid4
from models.debt_details import DebtDetails


def test_debt_details_missing_required_field():
    data = {
        "payment_due_date": "2025-06-30",
        "interest_rate": 0.21,
        "interest_paid": 10.00,
        "payments": 500.00,
    }

    with pytest.raises(KeyError, match="min_payment_due"):
        DebtDetails.from_dict(
            data=data,
            account_id=uuid4(),
            statement_id=uuid4(),
        )


def test_debt_details_invalid_date_format():
    data = {
        "min_payment_due": 35.00,
        "payment_due_date": "June 30th, 2025",
        "interest_rate": 0.21,
        "interest_paid": 10.00,
        "payments": 500.00,
    }

    with pytest.raises(ValueError):
        DebtDetails.from_dict(
            data=data,
            account_id=uuid4(),
            statement_id=uuid4(),
        )
