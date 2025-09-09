from datetime import date
from typing import Any
from unittest.mock import MagicMock
from unittest.mock import patch
from uuid import UUID
from uuid import uuid4

from models.transactions import Transaction
from services.normalization import normalize_transactions


@patch("services.normalization.get_account_registry")
def test_normalize_transactions_happy_path(
    mock_get_account_registry: MagicMock,
    sample_pdf_data_cc: dict[str, Any],
) -> None:
    # Arrange
    mock_get_account_registry.return_value = {
        "citi_cc": {
            "uuid": "11111111-1111-1111-1111-111111111111",
            "metadata": {"institution": "citibank"},
        }
    }

    statement_id = uuid4()
    parsed_transactions = sample_pdf_data_cc["transactions"]

    # Act
    result = normalize_transactions(
        parsed_data=parsed_transactions,
        account_slug="citi_cc",
        statement_id=statement_id,
    )

    # Assert
    assert "transactions" in result
    transactions = result["transactions"]
    assert isinstance(transactions, list)
    assert len(transactions) == 1

    txn = transactions[0]
    assert isinstance(txn, Transaction)

    assert isinstance(txn.id, UUID)
    assert txn.statement_id == statement_id
    assert txn.account_id == UUID("11111111-1111-1111-1111-111111111111")
    assert txn.date == date(2025, 6, 5)
    assert txn.amount == 250.00
    assert txn.description == "Example Purchase"
    assert txn.category == "Shopping"
    assert txn.type == "debit"
    assert txn.custom_description is None
