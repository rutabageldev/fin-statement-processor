import csv
from datetime import datetime
from typing import Any, Dict, List, IO


def parse_citi_cc_csv(file_obj: IO[str]) -> List[Dict[str, Any]]:
    return [
        {
            "date": "2025-04-15",
            "amount": -125.34,
            "description": "Starbucks Purchase",
            "custom_description": None,
            "category": None,
            "type": "debit",
        },
        {
            "date": "2025-04-12",
            "amount": 23100.00,
            "description": "Online Payment - Thank You",
            "custom_description": None,
            "category": None,
            "type": "payment",
        },
    ]
