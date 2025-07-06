# services/parsers/dispatch_parser.py

from services.parsers.pdf.parse_citi_cc_pdf import parse_citi_cc_pdf


def parse_pdf(account_name: str, pdf_path: str) -> dict:
    with open(pdf_path, "rb") as f:
        file_bytes = f.read()

    if account_name == "citi_cc":
        return parse_citi_cc_pdf(file_bytes)
    else:
        raise ValueError(f"No PDF parser implemented for account '{account_name}'")
