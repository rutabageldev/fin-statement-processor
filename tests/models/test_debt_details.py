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


def test_debt_details_interest_exceeds_payments_results_in_negative_principal():
    data = {
        "min_payment_due": 35.0,
        "payment_due_date": "2025-07-15",
        "interest_rate": 0.25,
        "interest_paid": 150.0,
        "payments": 100.0,
    }

    obj = DebtDetails.from_dict(data, account_id=uuid4(), statement_id=uuid4())
    assert obj.principal_paid == -50.0


def test_debt_details_zero_payment():
    data = {
        "min_payment_due": 0.0,
        "payment_due_date": "2025-07-01",
        "interest_rate": 0.0,
        "interest_paid": 0.0,
        "payments": 0.0,
    }

    obj = DebtDetails.from_dict(data, account_id=uuid4(), statement_id=uuid4())
    assert obj.payments == 0.0
    assert obj.principal_paid == 0.0
