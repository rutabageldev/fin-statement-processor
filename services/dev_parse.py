import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from .parser import route_to_parser, StatementType

# import pandas as pd

INPUT_FILE = Path("samples/sample_citi_cc_statement.pdf")
STATEMENT_TYPE: StatementType = "CITI_CC"
OUTPUT_FILE = Path("output/parsed_output.txt")
SUMMARY_JSON = Path("output/account_summary.json")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Parse and extract data from a statement PDF."
    )
    parser.add_argument(
        "--timestamped",
        action="store_true",
        help="Write output to a timestamped file instead of overwriting the default file",
    )
    return parser.parse_args()


def main(timestamped: bool):
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Could not find input file: {INPUT_FILE}")

    with open(INPUT_FILE, "rb") as f:
        file_bytes = f.read()

    parsed_statement = route_to_parser(file_bytes, STATEMENT_TYPE)

    if timestamped:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        output_file = OUTPUT_FILE.with_name(f"parsed_output_{timestamp}.txt")
    else:
        output_file = OUTPUT_FILE

    output_file.parent.mkdir(exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as out:
        out.write("Parsed Output\n")
        out.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        out.write("=" * 80 + "\n")

        for key, value in parsed_statement.items():
            out.write(f"{key}:\n")

            if isinstance(value, list):
                for line in value:
                    out.write(f"  {line}\n")
            else:
                out.write(f"    {value}\n")

            out.write("-" * 80 + "\n")

        print(f"✅ Parsed output written to: {output_file}")

    if "account_summary" in parsed_statement:
        with open(SUMMARY_JSON, "w", encoding="utf-8") as f:
            json.dump(parsed_statement["account_summary"], f, indent=2)
        print(f"✅ Account summary written to: {SUMMARY_JSON}")


if __name__ == "__main__":
    args = parse_args()
    main(timestamped=args.timestamped)
