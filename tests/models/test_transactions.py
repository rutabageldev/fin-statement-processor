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
