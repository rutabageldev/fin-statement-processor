#!/usr/bin/env python3
"""Ledgerly Statement Parser CLI."""

import argparse
import json
import logging
import os
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv

from registry.loader import get_account_registry
from services.parsers.dispatch_parser import parse_csv
from services.parsers.dispatch_parser import parse_pdf


load_dotenv()

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    supported_accounts = get_account_registry()

    parser = argparse.ArgumentParser(description="Ledgerly Statement Parser CLI")
    parser.add_argument("--account", required=True, help="Account type (e.g., citi_cc)")
    parser.add_argument("--pdf", help="Path to PDF file")
    parser.add_argument("--csv", help="Path to CSV file (optional)")

    try:
        args = parser.parse_args()
    except Exception:
        logger.exception("❌ Failed to parse command-line arguments")
        raise

    if args.account not in supported_accounts:
        supported_list = ", ".join(supported_accounts.keys())
        logger.error(
            "Unsupported account: '%s'. Supported accounts: %s",
            args.account,
            supported_list,
        )
        parser.error("Unsupported account type")

    if not args.pdf and not args.csv:
        logger.error("No input file provided.")
        parser.error("You must provide at least one of --pdf or --csv")

    return args


def main() -> None:
    """Main function to parse financial statements."""
    args = parse_args()
    statement_id = str(uuid4())
    output_dir = Path(os.getenv("OUTPUT_DIR", "./output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{statement_id}.json"

    results = {}

    try:
        if args.pdf:
            logger.info("📄 Parsing PDF: %s", args.pdf)
            results.update(parse_pdf(args.account, args.pdf))

        if args.csv:
            logger.info("📈 Parsing CSV: %s", args.csv)
            statement_id = results["statement_data"]["id"]
            results["transactions"] = parse_csv(args.account, args.csv, statement_id)

        debug_output = json.dumps(results, indent=2, default=str)
        logger.debug("🔍 Final output contents: %s", debug_output)

        # Write result
        with output_path.open("w") as f:
            json.dump(results, f, indent=2, default=str)

        logger.info("✅ Output written to %s", output_path)

    except Exception:
        logger.exception(
            "❌ Unexpected error while processing statement %s", statement_id
        )
        # Optional: write structured error file to output/errors/{statement_id}.json


if __name__ == "__main__":
    main()
