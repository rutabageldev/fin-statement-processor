import logging
from typing import Any
from uuid import UUID

from services.parsers.csv.parse_citi_cc_csv import parse_citi_cc_csv
from services.parsers.pdf.parse_citi_cc_pdf import parse_citi_cc_pdf


def parse_pdf(account_slug: str, pdf_path: str) -> dict:
    logging.debug(f"Dispatching PDF parser for account: {account_slug}")
    try:
        with open(pdf_path, "rb") as f:
            file_bytes = f.read()

        match account_slug:
            case "citi_cc":
                return parse_citi_cc_pdf(file_bytes, account_slug)
            case _:
                logging.error(f"No PDF parser available for account: {account_slug}")
                raise NotImplementedError(
                    f"No PDF parser implemented for account: {account_slug}"
                )

    except FileNotFoundError:
        logging.exception(f"PDF file not found: {pdf_path}")
        raise
    except Exception as e:
        logging.exception(f"Unexpected error while parsing PDF: {e}")
        raise


def parse_csv(
    account_slug: str, csv_path: str, statement_uuid: UUID
) -> list[dict[str, Any]]:
    logging.debug(f"Dispatching CSV parser for account: {account_slug}")
    try:
        match account_slug:
            case "citi_cc":
                logging.debug(f"✅ Passing statement_id {statement_uuid} to CSV parser")
                with open(csv_path, encoding="utf-8") as f:
                    return parse_citi_cc_csv(f, statement_uuid, account_slug)
            case _:
                logging.error(f"No CSV parser available for account: {account_slug}")
                raise NotImplementedError(
                    f"No CSV parser implemented for account: {account_slug}"
                )
    except FileNotFoundError:
        logging.exception(f"CSV file not found: {csv_path}")
        raise
    except Exception as e:
        logging.exception(f"Unexpected error while parsing CSV: {e}")
        raise
