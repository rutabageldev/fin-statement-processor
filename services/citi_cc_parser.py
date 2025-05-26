import csv
import logging
import pdfplumber
import re
from datetime import datetime
from io import BytesIO
from typing import Any, Dict, List, Optional
from .parser_config_loader import load_parser_config

DEBUG_MODE = True

TRANSFORM_REGISTRY = {
    "dollars_to_points": lambda val: int(abs(float(val)) * 100),
    "percent_to_decimal": lambda val: round(float(val) / 100, 4),
}

# Suppress noisy logs from pdfminer
logging.getLogger("pdfminer").setLevel(logging.ERROR)


def parse(file_bytes: bytes, csv_path: Optional[str] = None) -> Dict[str, Any]:
    with pdfplumber.open(BytesIO(file_bytes)) as pdf:
        statement_lines: List[str] = []

        for page in pdf.pages:
            raw_text = page.extract_text()
            if raw_text:
                raw_lines = raw_text.splitlines()
                cleaned_lines = [line.strip() for line in raw_lines if line.strip()]
                statement_lines.extend(cleaned_lines)

        account_summary = extract_account_summary(statement_lines)
        if csv_path:
            transactions = extract_transaction_csv(csv_path)
        else:
            logging.warning(
                "No CSV provided. PDF-based transaction extraction is not yet implemented."
            )
            transactions = []

        return {
            "source": "CITI_CC",
            "page_count": str(len(pdf.pages)),
            "statement_lines": statement_lines,
            "account_summary": account_summary,
            "transactions": transactions,
        }


def extract_account_summary(statement_lines: List[str]) -> Dict[str, Any]:
    config = load_parser_config("citi_cc")
    summary_fields = config.get("account_summary_fields", [])
    summary_data: Dict[str, Any] = {}

    for field in summary_fields:
        summary_data[field["name"]] = extract_field_value(
            lines=statement_lines,
            label_patterns=field.get("label_patterns", []),
            value_pattern=field.get("value_pattern", ""),
            data_type=field.get("data_type", "string"),
            field_name=field["name"],
            transform=field.get("transform"),
        )

    return summary_data


def extract_field_value(
    lines: List[str],
    label_patterns: List[str],
    value_pattern: str,
    data_type: str = "string",
    field_name: str = "unknown",
    transform: Optional[str] = None,
) -> Any | None:
    """
    Extracts and casts a value from lines based on label and value regex patterns.

    Args:
        lines: List of statement lines.
        label_patterns: List of regex patterns that identify a line with the desired label.
        value_pattern: Regex to extract the value from a matched line.
        data_type: Expected data type (float, int, string, date).

    Returns:
        Parsed value of the appropriate type, or None if not found or invalid.
    """
    for line in lines:
        if any(re.search(label, line) for label in label_patterns):
            match_obj = re.search(value_pattern, line)
            if DEBUG_MODE:
                print(f"[DEBUG] line matched for '{field_name}': {line}")
            if not match_obj:
                logging.warning(
                    f"Found label match but no value match in line: '{line}'"
                )
                return None

            raw_val = match_obj.group(0).strip().replace("$", "").replace(",", "")

            transformed_val: Any

            try:
                transformed_val = (
                    TRANSFORM_REGISTRY[transform](raw_val)
                    if transform in TRANSFORM_REGISTRY
                    else raw_val
                )
            except ValueError:
                logging.warning(
                    f"Could not apply transform '{transform}' to '{raw_val}'"
                )
                return None

            try:
                match data_type:
                    case "float":
                        return float(transformed_val)
                    case "int":
                        return int(transformed_val)
                    case "date":
                        val_str = str(transformed_val)

                        for fmt in (
                            "%m/%d/%Y",
                            "%m-%d-%Y",
                            "%m-%d-%y",
                            "%m/%d/%y",
                            "%Y-%m-%d",
                        ):
                            try:
                                return datetime.strptime(val_str, fmt).date()
                            except ValueError:
                                continue
                        logging.warning(f"Could not parse date format: '{val_str}'")
                        return None
                    case _:
                        return transformed_val
            except ValueError:
                logging.warning(f"Could not convert '{transformed_val}' to {data_type}")
                return None

    return None


def extract_transaction_csv(csv_path: str) -> List[Dict[str, Any]]:
    transactions = []

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                date = datetime.strptime(row["Date"], "%m/%d/%Y").date()
                description = row["Description"].strip()
                debit = row["Debit"].strip()
                credit = row["Credit"].strip()

                if debit:
                    amount = -float(debit.replace(",", ""))
                    t_type = "debit"
                elif credit:
                    amount = float(credit.replace(",", ""))
                    credit_desc = description.lower()
                    if "online payment" in credit_desc:
                        t_type = "payment"
                    elif "redeemed" in credit_desc or "thankyou" in credit_desc:
                        t_type = "refund"
                    else:
                        t_type = "credit"
                else:
                    continue  # No amount found, skip

                transactions.append(
                    {
                        "date": date.isoformat(),
                        "amount": amount,
                        "description": description,
                        "custom_description": None,
                        "category": None,
                        "type": t_type,
                    }
                )

            except Exception as e:
                print(f"⚠️ Skipping row due to error: {e}\nRow: {row}")

    return transactions
