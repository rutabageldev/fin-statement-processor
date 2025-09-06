from io import StringIO
from pathlib import Path
from uuid import uuid4

from services.parsers.csv.parse_citi_cc_csv import parse_citi_cc_csv


statement_uuid = uuid4()
account_slug = "citi_cc"


def test_parse_citi_cc_csv():
    # Arrange
    path = Path("tests/data/test-transactions_citi-cc.csv")

    # Act
    with path.open("r", encoding="utf-8") as f:
        result = parse_citi_cc_csv(f, statement_uuid, account_slug)

    # Assert
    assert isinstance(result, list)
    assert len(result) > 0

    for transaction in result:
        assert transaction["statement_id"] == statement_uuid
        assert "account_id" in transaction
        assert "date" in transaction
        assert "amount" in transaction
        assert "description" in transaction
        assert "type" in transaction
        assert transaction["type"] in {"debit", "credit", "refund", "payment"}


def test_parse_citi_cc_csv_skips_row_with_no_amount():
    csv_data = """Date,Description,Debit,Credit
06/30/2025,No amount,,
"""

    f = StringIO(csv_data)

    result = parse_citi_cc_csv(f, statement_uuid, account_slug)

    assert isinstance(result, list)
    assert result == []  # should skip this row


def test_parse_citi_cc_csv_skips_row_with_bad_date():
    csv_data = """Date,Description,Debit,Credit
30-06-2025,Amazon,50.00,
"""

    f = StringIO(csv_data)

    result = parse_citi_cc_csv(f, statement_uuid, account_slug)

    assert result == []  # invalid date format


def test_parse_citi_cc_csv_handles_credit_row_with_refund():
    csv_data = """Date,Description,Debit,Credit
06/30/2025,Refund issued,,25.00
"""

    f = StringIO(csv_data)

    result = parse_citi_cc_csv(f, statement_uuid, account_slug)

    assert len(result) == 1
    transaction = result[0]
    assert transaction["amount"] == 25.00
    assert transaction["type"] == "refund"
    assert transaction["description"] == "Refund issued"
    assert transaction["statement_id"] == statement_uuid
