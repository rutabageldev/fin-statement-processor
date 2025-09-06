from datetime import UTC
from datetime import date
from datetime import datetime
from unittest.mock import patch
from uuid import UUID

from models.statement import StatementData
from models.statement import StatementDetails
from services.normalization import normalize_statement_data


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

    file_url = "s3://bucket/file.pdf"
    uploaded_at = datetime(2025, 7, 1, tzinfo=UTC)

    # Act
    result = normalize_statement_data(
        parsed_data=sample_pdf_data_cc["account_summary"],
        account_slug="citi_cc",
        file_url=file_url,
        uploaded_at=uploaded_at,
    )

    # Assert
    statement = result["statement_data"]
    details = result["statement_details"]

    assert isinstance(statement, StatementData)
    assert isinstance(statement.id, UUID)
    assert statement.institution_id == UUID("22222222-2222-2222-2222-222222222222")
    assert statement.account_id == UUID("11111111-1111-1111-1111-111111111111")
    assert statement.period_start == date(2025, 6, 1)
    assert statement.period_end == date(2025, 6, 30)
    assert statement.file_url == file_url
    assert statement.uploaded_at == uploaded_at

    assert isinstance(details, StatementDetails)
    assert isinstance(details.id, UUID)
    assert details.statement_id == statement.id
    assert details.previous_balance == 1000.00
    assert details.new_balance == 760.00
