import logging
from pathlib import Path
from typing import Any
from uuid import UUID

from services.parsers.csv.parse_citi_cc_csv import parse_citi_cc_csv
from services.parsers.pdf.parse_citi_cc_pdf import parse_citi_cc_pdf


def parse_pdf(account_slug: str, pdf_path: str) -> dict[str, Any]:
    logging.debug("Dispatching PDF parser for account: %s", account_slug)
    try:
        with Path(pdf_path).open("rb") as f:
            file_bytes = f.read()

        match account_slug:
            case "citi_cc":
                return parse_citi_cc_pdf(file_bytes, account_slug)
            case _:
                logging.error("No PDF parser available for account: %s", account_slug)
                error_msg = f"No PDF parser implemented for account: {account_slug}"
                raise NotImplementedError(error_msg)

    except FileNotFoundError:
        logging.exception("PDF file not found: %s", pdf_path)
        raise
    except Exception as e:
        logging.exception("Unexpected error while parsing PDF: %s", e)
        raise


def parse_csv(
    account_slug: str, csv_path: str, statement_uuid: UUID
) -> list[dict[str, Any]]:
    logging.debug("Dispatching CSV parser for account: %s", account_slug)
    try:
        match account_slug:
            case "citi_cc":
                logging.debug(
                    "✅ Passing statement_id %s to CSV parser", statement_uuid
                )
                with Path(csv_path).open("r", encoding="utf-8") as f:
                    return parse_citi_cc_csv(f, statement_uuid, account_slug)
            case _:
                logging.error("No CSV parser available for account: %s", account_slug)
                error_msg = f"No CSV parser implemented for account: {account_slug}"
                raise NotImplementedError(error_msg)
    except FileNotFoundError:
        logging.exception("CSV file not found: %s", csv_path)
        raise
    except Exception as e:
        logging.exception("Unexpected error while parsing CSV: %s", e)
        raise
