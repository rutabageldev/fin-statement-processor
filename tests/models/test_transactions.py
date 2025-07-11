import pytest
from uuid import uuid4
from models.transactions import Transaction


def test_transaction_missing_required_field():
    data = {
        "date": "2025-06-30",
        "amount": 99.99,
        # "description": is missing
        "type": "debit",
    }

    with pytest.raises(KeyError, match="description"):
        Transaction.from_dict(
            data=data,
            statement_id=uuid4(),
            account_id=uuid4(),
        )


def test_transaction_optional_fields_none():
    data = {
        "date": "2025-07-05",
        "amount": 50.00,
        "description": "Coffee shop",
        "type": "debit",
    }

    obj = Transaction.from_dict(data, statement_id=uuid4(), account_id=uuid4())
    assert obj.custom_description is None
    assert obj.category is None


def test_transaction_invalid_date_format():
    data = {
        "date": "June 30, 2025",
        "amount": 99.99,
        "description": "Example Purchase",
        "type": "debit",
    }

    with pytest.raises(ValueError):
        Transaction.from_dict(
            data=data,
            statement_id=uuid4(),
            account_id=uuid4(),
        )


def test_transaction_invalid_type_literal():
    data = {
        "date": "2025-06-30",
        "amount": 99.99,
        "description": "Invalid type example",
        "type": "withdrawal",  # invalid value
    }

    with pytest.raises(ValueError):
        Transaction.from_dict(
            data=data,
            statement_id=uuid4(),
            account_id=uuid4(),
        )


def test_transaction_negative_amount_allowed():
    data = {
        "date": "2025-07-05",
        "amount": -12.75,
        "description": "Overdraft fee",
        "type": "debit",
    }

    obj = Transaction.from_dict(data, statement_id=uuid4(), account_id=uuid4())
    assert obj.amount == -12.75


def test_transaction_missing_required_field_raises():
    data = {
        # missing amount
        "date": "2025-07-05",
        "description": "Forgot to include amount",
        "type": "debit",
    }

    with pytest.raises(KeyError):
        Transaction.from_dict(data, statement_id=uuid4(), account_id=uuid4())
