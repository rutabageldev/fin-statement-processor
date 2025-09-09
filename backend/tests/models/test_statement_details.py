from uuid import uuid4

import pytest

from models.statement import StatementDetails


def test_statement_details_from_dict_missing_previous_balance() -> None:
    data: dict[str, object] = {
        "new_balance": 1000.00,
    }

    with pytest.raises(KeyError, match="previous_balance"):
        StatementDetails.from_dict(
            data=data,
            statement_id=uuid4(),
        )


def test_statement_details_from_dict_invalid_balance_type() -> None:
    data: dict[str, object] = {
        "previous_balance": "one thousand",
        "new_balance": 1000.00,
    }

    with pytest.raises(ValueError, match="could not convert string to float"):
        StatementDetails.from_dict(
            data=data,
            statement_id=uuid4(),
        )


def test_statement_details_missing_balance_fields() -> None:
    with pytest.raises(KeyError):
        StatementDetails.from_dict(data={}, statement_id=uuid4())


def test_statement_details_invalid_balance_type() -> None:
    bad_data: dict[str, object] = {
        "previous_balance": "one thousand",
        "new_balance": 750.0,
    }
    with pytest.raises(ValueError, match="could not convert string to float"):
        StatementDetails.from_dict(data=bad_data, statement_id=uuid4())
