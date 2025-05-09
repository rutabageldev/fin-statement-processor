import os
from pathlib import Path
from parser import route_to_parser

# import pandas as pd

INPUT_FILE = Path("samples/sample_citi_cc_statement.pdf")
STATEMENT_TYPE = "CITI_CC"
OUTPUT_FILE = Path("output/parsed_output.txt")


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Could not find input file: {INPUT_FILE}")

    with open(INPUT_FILE, "rb") as f:
        file_bytes = f.read()

    parsed_data = route_to_parser(file_bytes, STATEMENT_TYPE)

    OUTPUT_FILE.parent.mkdir(exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write("Parsed Output\n")
        out.write("=" * 80 + "\n")
        for key, value in parsed_data.items():
            out.write(f"{key}:\n")
            out.write(f"    {value}\n")
            out.write("-" * 80 + "\n")

        print(f"✅ Parsed output written to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
