# Test Command: python main.py --account citi_cc --pdf ./tests/data/test-statement_citi-cc.pdf --csv ./tests/data/test-transactions_citi-cc.csv
from dotenv import load_dotenv

load_dotenv()

import services.logging_config
import argparse
import json
import logging
from uuid import UUID, uuid4
import os
from registry.loader import get_account_registry
from services.parsers.dispatch_parser import parse_pdf, parse_csv


def parse_args():
    SUPPORTED_ACCOUNTS = get_account_registry()

    parser = argparse.ArgumentParser(description="Ledgerly Statement Parser CLI")
    parser.add_argument("--account", required=True, help="Account type (e.g., citi_cc)")
    parser.add_argument("--pdf", help="Path to PDF file")
    parser.add_argument("--csv", help="Path to CSV file (optional)")

    try:
        args = parser.parse_args()
    except Exception as e:
        logging.exception("❌ Failed to parse command-line arguments")
        raise

    if args.account not in SUPPORTED_ACCOUNTS:
        logging.error(
            f"Unsupported account: '{args.account}'. Supported accounts: {', '.join(SUPPORTED_ACCOUNTS.keys())}"
        )
        parser.error("Unsupported account type")

    if not args.pdf and not args.csv:
        logging.error("No input file provided.")
        parser.error("You must provide at least one of --pdf or --csv")

    return args


def main():
    args = parse_args()
    statement_id = str(uuid4())
    output_dir = os.getenv("OUTPUT_DIR", "./output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{statement_id}.json")

    results = {}

    try:
        if args.pdf:
            logging.info(f"📄 Parsing PDF: {args.pdf}")
            results.update(parse_pdf(args.account, args.pdf))

        if args.csv:
            logging.info(f"📈 Parsing CSV: {args.csv}")
            statement_id = results["statement_data"]["id"]
            results["transactions"] = parse_csv(args.account, args.csv, statement_id)

        logging.debug(
            f"🔍 Final output contents: {json.dumps(results, indent=2, default=str)}"
        )

        # Write result
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2, default=str)

        logging.info(f"✅ Output written to {output_path}")

    except Exception as e:
        logging.exception(
            f"❌ Unexpected error while processing statement {statement_id}"
        )
        # Optional: write structured error file to output/errors/{statement_id}.json here


if __name__ == "__main__":
    main()
