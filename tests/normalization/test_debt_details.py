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
    debt = result["debt_details"]

    assert isinstance(debt, DebtDetails)
    assert isinstance(debt.id, UUID)
    assert debt.account_id == UUID("11111111-1111-1111-1111-111111111111")
    assert debt.statement_id == statement_id

    # Field-level checks
    assert debt.payments == 500.00
    assert debt.min_payment_due == 35.00
    assert debt.payment_due_date == date(2025, 6, 30)
    assert debt.interest_rate == 0.21
    assert debt.interest_paid == 10.00
    assert debt.principal_paid == 490.00
