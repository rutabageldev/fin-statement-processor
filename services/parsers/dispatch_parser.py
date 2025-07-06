from typing import Dict, Any, List
from services.parsers.pdf.parse_citi_cc_pdf import parse_citi_cc_pdf
from services.parsers.csv.parse_citi_cc_csv import parse_citi_cc_csv


def parse_pdf(account_name: str, pdf_path: str) -> dict:
    with open(pdf_path, "rb") as f:
        file_bytes = f.read()

    match account_name:
        case "citi_cc":
            return parse_citi_cc_pdf(file_bytes)
        case _:
            raise ValueError(f"No PDF parser implemented for account '{account_name}'")


def parse_csv(account_name: str, csv_path: str) -> List[Dict[str, Any]]:
    match account_name:
        case "citi_cc":
            with open(csv_path, "r", encoding="utf-8") as f:
                return parse_citi_cc_csv(f)
        case _:
            raise NotImplementedError(
                f"No CSV parser implemented for account: {account_name}"
            )
