from uuid import UUID, uuid4
from unittest.mock import patch
from services.normalization import normalize_cc_details
from models.cc_details import CreditCardDetails


@patch("services.normalization.get_account_registry")
def test_normalize_cc_details_happy_path(
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
    result = normalize_cc_details(
        parsed_data=sample_pdf_data_cc["account_summary"],
        account_slug="citi_cc",
        statement_id=statement_id,
    )

    # Assert
    cc = result["credit_card_details"]

    assert isinstance(cc, CreditCardDetails)
    assert isinstance(cc.id, UUID)
    assert cc.account_id == UUID("11111111-1111-1111-1111-111111111111")
    assert cc.statement_id == statement_id

    assert cc.credit_limit == 5000.00
    assert cc.available_credit == 4240.00
    assert cc.points_earned == 500
    assert cc.points_redeemed == 200
    assert cc.cash_advances == 0.00
    assert cc.fees == 0.00
    assert cc.purchases == 250.00
    assert cc.credits == 0.00
