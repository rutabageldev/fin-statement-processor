"""Main parser dispatcher for routing files to appropriate parsers."""

import logging
from pathlib import Path
from typing import Any
from typing import NoReturn
from uuid import UUID

from services.parsers.csv.parse_citi_cc_csv import parse_citi_cc_csv
from services.parsers.pdf.parse_citi_cc_pdf import parse_citi_cc_pdf


def parse_pdf(account_slug: str, pdf_path: str) -> dict[str, Any]:
    """Parse a PDF statement file using account-specific parser.

    Args:
        account_slug: Account type identifier (e.g., 'citi_cc')
        pdf_path: Path to the PDF file to parse

    Returns:
        Dictionary containing parsed statement data

    Raises:
        NotImplementedError: If no parser exists for the account type
        FileNotFoundError: If the PDF file doesn't exist
    """
    logging.debug("Dispatching PDF parser for account: %s", account_slug)
    try:
        with Path(pdf_path).open("rb") as f:
            file_bytes = f.read()

        match account_slug:
            case "citi_cc":
                return parse_citi_cc_pdf(file_bytes, account_slug)
            case _:
                _raise_parser_not_implemented(account_slug, "PDF")

    except FileNotFoundError:
        logging.exception("PDF file not found: %s", pdf_path)
        raise
    except Exception:
        logging.exception("Unexpected error while parsing PDF")
        raise


def parse_csv(
    account_slug: str, csv_path: str, statement_uuid: UUID
) -> list[dict[str, Any]]:
    """Parse a CSV transaction file using account-specific parser.

    Args:
        account_slug: Account type identifier (e.g., 'citi_cc')
        csv_path: Path to the CSV file to parse
        statement_uuid: UUID of the associated statement

    Returns:
        List of normalized transaction dictionaries

    Raises:
        NotImplementedError: If no parser exists for the account type
        FileNotFoundError: If the CSV file doesn't exist
    """
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
                _raise_parser_not_implemented(account_slug, "CSV")
    except FileNotFoundError:
        logging.exception("CSV file not found: %s", csv_path)
        raise
    except Exception:
        logging.exception("Unexpected error while parsing CSV")
        raise


def _raise_parser_not_implemented(account_slug: str, parser_type: str) -> NoReturn:
    """Raise NotImplementedError for missing parsers."""
    logging.error("No %s parser available for account: %s", parser_type, account_slug)
    error_msg = f"No {parser_type} parser implemented for account: {account_slug}"
    raise NotImplementedError(error_msg)
