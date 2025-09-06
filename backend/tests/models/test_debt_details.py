from uuid import uuid4

import pytest

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

    with pytest.raises(ValueError, match="invalid literal"):
        DebtDetails.from_dict(
            data=data,
            account_id=uuid4(),
            statement_id=uuid4(),
        )


def test_debt_details_optional_id():
    data = {
        "min_payment_due": 35.00,
        "payment_due_date": "2025-06-30",
        "interest_rate": 0.21,
        "interest_paid": 10.00,
        "payments": 500.00,
    }

    obj = DebtDetails.from_dict(data, account_id=uuid4(), statement_id=uuid4())
    assert isinstance(obj.id, uuid4().__class__)


def test_debt_details_negative_interest_and_payments():
    data = {
        "min_payment_due": 35.00,
        "payment_due_date": "2025-06-30",
        "interest_rate": 0.21,
        "interest_paid": -5.00,
        "payments": -200.00,
    }

    obj = DebtDetails.from_dict(data, account_id=uuid4(), statement_id=uuid4())
    assert obj.payments == -200.00
    assert obj.interest_paid == -5.00
    assert obj.principal_paid == round(abs(-200.00) - (-5.00), 2)


def test_debt_details_principal_rounding():
    data = {
        "min_payment_due": 40.00,
        "payment_due_date": "2025-06-30",
        "interest_rate": 0.15,
        "interest_paid": 10.115,
        "payments": 100.115,
    }

    obj = DebtDetails.from_dict(data, account_id=uuid4(), statement_id=uuid4())
    assert round(obj.principal_paid, 2) == round(90.0, 2)


def test_debt_details_missing_optional_id_generates_uuid():
    data = {
        "min_payment_due": 50.0,
        "payment_due_date": "2025-07-15",
        "interest_rate": 0.2,
        "interest_paid": 5.0,
        "payments": 100.0,
    }

    obj = DebtDetails.from_dict(data, account_id=uuid4(), statement_id=uuid4())
    assert isinstance(obj.id, uuid4().__class__)


def test_debt_details_payment_less_than_interest():
    """Ensure principal_paid is negative if interest > payments"""
    data = {
        "payments": 50.00,
        "interest_paid": 75.00,
        "min_payment_due": 35.00,
        "payment_due_date": "2025-06-30",
        "interest_rate": 0.21,
    }

    result = DebtDetails.from_dict(
        data=data,
        account_id=uuid4(),
        statement_id=uuid4(),
    )

    assert result.payments == 50.00
    assert result.interest_paid == 75.00
    assert result.principal_paid == -25.00


def test_debt_details_all_zero_values():
    """Validate edge case with all zero debt-related values"""
    data = {
        "payments": 0.00,
        "interest_paid": 0.00,
        "min_payment_due": 0.00,
        "payment_due_date": "2025-06-30",
        "interest_rate": 0.00,
    }

    result = DebtDetails.from_dict(
        data=data,
        account_id=uuid4(),
        statement_id=uuid4(),
    )

    assert result.payments == 0.00
    assert result.interest_paid == 0.00
    assert result.principal_paid == 0.00
    assert result.min_payment_due == 0.00
    assert result.interest_rate == 0.00
