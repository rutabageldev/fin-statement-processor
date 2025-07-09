import pytest


@pytest.fixture
def sample_pdf_data_cc():
    """Expected output format for a credit card PDF Parser"""
    return {
        "account_summary": {
            "previous_balance": 1000.00,
            "payments": 500.00,
            "credits": 0.00,
            "purchases": 250.00,
            "cash_advances": 0.00,
            "fees": 0.00,
            "interest_rate": 0.21,
            "interest_paid": 10.00,
            "new_balance": 760.00,
            "min_payment_due": 35.00,
            "payment_due_date": "2025-06-30",
            "bill_period_start": "2025-06-01",
            "bill_period_end": "2025-06-30",
            "credit_limit": 5000.00,
            "available_credit": 4240.00,
        },
        "transactions": [
            {
                "date": "2025-06-05",
                "amount": 250.00,
                "description": "Example Purchase",
                "category": "Shopping",
                "type": "debit",
            }
        ],
    }


@pytest.fixture
def normalized_statement_data_cc():
    """Expected results of the normalize_statement_data(sample_pdf_data_cc)"""
    return {
        "statement_data": {"previous_balance": 1000.00, "new_balance": 760.00},
        "credit_card_details": {
            "credit_limit": 5000.00,
            "available_credit": 4240.00,
            "cash_advances": 0.00,
            "fees": 0.00,
            "purchases": 250.00,
            "credits": 0.00,
        },
        "debt_details": {
            "payment": 500.00,
            "min_payment_due": 35.00,
            "interest_rate": 0.21,
            "payment_due_date": "2025-06-30",
            "interest_paid": 10.00,
            "principal_paid": 490.00,
        },
        "transactions": [
            {
                "date": "2025-06-05",
                "amount": 250.00,
                "description": "Example Purchase",
                "category": "Shopping",
                "type": "debit",
            }
        ],
    }
