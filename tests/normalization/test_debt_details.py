from datetime import date
from uuid import UUID, uuid4
from unittest.mock import patch
from services.normalization import normalize_debt_details
from models.debt_details import DebtDetails


@patch("services.normalization.get_account_registry")
def test_normalize_debt_details_happy_path(
    mock_get_account_registry,
    sample_pdf_data_cc,
):
    # Arrange
    mock_get_account_registry.return_value = {
        "citi_cc": {
            "uuid": "11111111-1111-1111-1111-111111111111",
            "metadata": {"institution": "citibank"},
        }
    }

    statement_id = uuid4()

    # Act
    result = normalize_debt_details(
        parsed_data=sample_pdf_data_cc["account_summary"],
        account_slug="citi_cc",
        statement_id=statement_id,
    )

    # Assert
    assert "debt_details" in result
    assert isinstance(result["debt_details"], DebtDetails)
    assert result["debt_details"].statement_id == statement_id
    assert result["debt_details"].payment_due_date == date(2025, 6, 30)
    assert result["debt_details"].min_payment_due == 35.00
    assert result["debt_details"].payments == 500.00
