from datetime import datetime
from uuid import UUID
from unittest.mock import patch

from services.normalization import normalize_statement_data
from models.statement import StatementData, StatementDetails


@patch("services.normalization.get_account_registry")
@patch("services.normalization.get_institution_registry")
def test_normalize_statement_data_happy_path(
    mock_get_institution_registry,
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

    mock_get_institution_registry.return_value = {
        "citibank": {"uuid": "22222222-2222-2222-2222-222222222222"}
    }

    # Act
    result = normalize_statement_data(
        parsed_data=sample_pdf_data_cc["account_summary"],
        account_slug="citi_cc",
        file_url="s3://bucket/file.pdf",
        uploaded_at=datetime(25, 7, 1),
    )

    # Assert
    assert "statement_data" in result
    assert "statement_details" in result
    assert isinstance(result["statement_data"], StatementData)
    assert isinstance(result["statement_details"], StatementDetails)

    # Check some expected values
    assert result["statement_data"].institution_id == UUID(
        "22222222-2222-2222-2222-222222222222"
    )
    assert result["statement_data"].account_id == UUID(
        "11111111-1111-1111-1111-111111111111"
    )
