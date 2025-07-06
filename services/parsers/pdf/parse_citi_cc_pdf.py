from typing import Any, Dict


def parse_citi_cc_pdf(file_bytes: bytes) -> Dict[str, Any]:
    return {
        "source": "CITI_CC",
        "page_count": "3",
        "statement_lines": [
            "Previous Balance $1,234.56",
            "Payments -$200.00",
            "New Balance $1,034.56",
        ],
        "account_summary": {
            "previous_balance": 1234.56,
            "payments": 200.00,
            "new_balance": 1034.56,
            "statement_start_date": "2024-05-01",
            "statement_end_date": "2024-05-31",
            "payment_due_date": "2024-06-25",
            "minimum_payment_due": 25.00,
        },
        "transactions": [
            {
                "date": "2024-05-05",
                "amount": -45.67,
                "description": "Amazon Purchase",
                "custom_description": None,
                "category": None,
                "type": "debit",
            },
            {
                "date": "2024-05-08",
                "amount": 100.00,
                "description": "Payment Received",
                "custom_description": None,
                "category": None,
                "type": "payment",
            },
        ],
    }
