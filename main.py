# Test Command: python main.py --account citi_cc --pdf ./tests/data/test-statement_citi-cc.pdf --csv ./tests/data/test-transactions_citi-cc.csv
import argparse
import json
import uuid
import os
from dotenv import load_dotenv
from services.parsers.dispatch_parser import (
    parse_pdf,
    parse_csv,
)  # CSV to be added later
from services.account_registry import (
    SUPPORTED_ACCOUNTS,
)  # list of accounts that have been implemented


load_dotenv()


def main():
    parser = argparse.ArgumentParser(description="Ledgerly Statement Parser CLI")
    parser.add_argument("--account", required=True, help="Account type (e.g., citi_cc)")
    parser.add_argument("--pdf", help="Path to PDF file")
    parser.add_argument("--csv", help="Path to CSV file (optional, stubbed)")
    args = parser.parse_args()

    if args.account not in SUPPORTED_ACCOUNTS:
        parser.error(
            f"Unsupported account: '{args.account}'. Supported accounts: {', '.join(SUPPORTED_ACCOUNTS.keys())}"
        )

    if not args.pdf and not args.csv:
        parser.error("You must provide at least one of --pdf or --csv")

    results = {}
    if args.pdf:
        print(f"📄 Parsing PDF: {args.pdf}")
        parse_pdf(args.account, args.pdf)
        results.update(parse_pdf(args.account, args.pdf))

    if args.csv:
        print(f"📈 Parsing CSV: {args.csv}")
        results["transactions"] = parse_csv(args.account, args.csv)

    # Determine output path
    statement_id = str(uuid.uuid4())
    output_dir = os.getenv("OUTPUT_DIR", "./output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{statement_id}.json")

    # Write result
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"✅ Output written to {output_path}")


if __name__ == "__main__":
    main()
