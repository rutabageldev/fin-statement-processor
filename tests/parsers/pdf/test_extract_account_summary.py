from unittest.mock import patch

from services.parsers.pdf.parse_citi_cc_pdf import extract_account_summary


@patch("services.parsers.pdf.parse_citi_cc_pdf.load_parser_config")
@patch("services.parsers.pdf.parse_citi_cc_pdf.extract_field_value")
def test_extract_account_summary_happy_path(mock_extract, mock_config):
    # Fake parser config with 2 fields
    mock_config.return_value = {
        "account_summary_fields": [
            {
                "name": "previous_balance",
                "label_patterns": [r"Previous Balance"],
                "value_pattern": r"\$[\d,.]+",
                "data_type": "float",
            },
            {
                "name": "payment_due_date",
                "label_patterns": [r"Payment Due Date"],
                "value_pattern": r"\d{2}/\d{2}/\d{4}",
                "data_type": "date",
            },
        ]
    }

    mock_extract.side_effect = [1000.00, "2025-06-30"]

    lines = [
        "Previous Balance: $1,000.00",
        "Payment Due Date: 06/30/2025",
    ]

    result = extract_account_summary(lines)

    assert result == {
        "previous_balance": 1000.00,
        "payment_due_date": "2025-06-30",
    }
    assert mock_extract.call_count == 2


@patch("services.parsers.pdf.parse_citi_cc_pdf.load_parser_config")
@patch("services.parsers.pdf.parse_citi_cc_pdf.extract_field_value")
def test_extract_account_summary_partial_failure(mock_extract, mock_config):
    mock_config.return_value = {
        "account_summary_fields": [
            {
                "name": "credits",
                "label_patterns": [r"Credits"],
                "value_pattern": r"\$[\d,.]+",
                "data_type": "float",
            },
            {
                "name": "fees",
                "label_patterns": [r"Fees"],
                "value_pattern": r"\$[\d,.]+",
                "data_type": "float",
            },
        ]
    }

    # Simulate one success, one failure (None)
    mock_extract.side_effect = [25.00, None]

    result = extract_account_summary(["Credits: $25.00", "Fees: --"])

    assert result == {"credits": 25.00, "fees": None}


@patch("services.parsers.pdf.parse_citi_cc_pdf.load_parser_config")
@patch("services.parsers.pdf.parse_citi_cc_pdf.extract_field_value")
def test_extract_account_summary_raises_and_recovers(mock_extract, mock_config):
    mock_config.return_value = {
        "account_summary_fields": [
            {
                "name": "interest",
                "label_patterns": [r"Interest"],
                "value_pattern": r"\$[\d,.]+",
                "data_type": "float",
            },
        ]
    }

    def raise_exception(*args, **kwargs):
        raise RuntimeError("parser boom")

    mock_extract.side_effect = raise_exception

    result = extract_account_summary(["Interest: $5.00"])

    assert result == {"interest": None}


@patch("services.parsers.pdf.parse_citi_cc_pdf.load_parser_config")
def test_extract_account_summary_empty_config(mock_config):
    mock_config.return_value = {"account_summary_fields": []}

    result = extract_account_summary(["Something: $10.00"])

    assert result == {}  # No fields defined to extract
