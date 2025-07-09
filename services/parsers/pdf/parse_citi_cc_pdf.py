import logging
import pdfplumber
import re
from datetime import datetime
from io import BytesIO
from typing import Any, Dict, List, Optional, cast

from services.normalization import (
    normalize_cc_details,
    normalize_debt_details,
    normalize_statement_data,
)
from ..parser_config_loader import load_parser_config

logging.getLogger("pdfminer").setLevel(logging.ERROR)

logger = logging.getLogger(__name__)

TRANSFORM_REGISTRY = {
    "dollars_to_points": lambda val: int(abs(float(val)) * 100),
    "percent_to_decimal": lambda val: round(float(val) / 100, 4),
}


def parse_citi_cc_pdf(file_bytes: bytes) -> Dict[str, Any]:
    try:
        with pdfplumber.open(BytesIO(file_bytes)) as pdf:
            statement_lines: List[str] = []

            for page in pdf.pages:
                raw_text = page.extract_text()
                if raw_text:
                    raw_lines = raw_text.splitlines()
                    cleaned_lines = [line.strip() for line in raw_lines if line.strip]
                    statement_lines.extend(cleaned_lines)

            account_summary = extract_account_summary(statement_lines)

            statement_data = normalize_statement_data(
                parsed_data=account_summary,
                account_slug="citi_cc",
                file_url=None,
                uploaded_at=datetime.utcnow(),
            )

            debt_data = normalize_debt_details(
                parsed_data=account_summary,
                account_slug="citi_cc",
                statement_id=statement_data["statement_data"].id,
            )

            cc_data = normalize_cc_details(
                parsed_data=account_summary,
                account_slug="citi_cc",
                statement_id=statement_data["statement_data"].id,
            )

            return {
                "statement_data": statement_data["statement_data"].model_dump(),
                "statement_details": statement_data["statement_details"].model_dump(),
                "debt_details": debt_data["debt_details"].model_dump(),
                "credit_card_details": cc_data["credit_card_details"].model_dump(),
            }

    except Exception as e:
        logger.exception("❌ Failed to parse Citi CC PDF")
        raise


def extract_account_summary(statement_lines: List[str]) -> Dict[str, Any]:
    config = load_parser_config("citi_cc")
    summary_fields = config.get("account_summary_fields", [])
    summary_data: Dict[str, Any] = {}

    for field in summary_fields:
        try:
            summary_data[field["name"]] = extract_field_value(
                lines=statement_lines,
                label_patterns=field.get("label_patterns", []),
                value_pattern=field.get("value_pattern", ""),
                data_type=field.get("data_type", "string"),
                field_name=field["name"],
                transform=field.get("transform"),
            )

        except Exception as e:
            logger.warning(f"⚠️ Failed to extract field '{field['name']}': {e}")
            summary_data[field["name"]] = None  # Preserve key for consistency

    return summary_data


def extract_field_value(
    lines: List[str],
    label_patterns: List[str],
    value_pattern: str,
    data_type: str = "string",
    field_name: str = "unknown",
    transform: Optional[str] = None,
) -> Any | None:
    for line in lines:
        if any(re.search(label, line) for label in label_patterns):
            match_obj = re.search(value_pattern, line)
            logger.debug(f"line matched for '{field_name}': {line}")
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
                transformed_val = cast(str | float | int, transformed_val)
            except ValueError:
                logger.warning(
                    f"Could not apply transform '{transform}' to value '{raw_val}'"
                )
                return None

            try:
                match data_type:
                    case "float":
                        return float(transformed_val)
                    case "int":
                        return int(float(transformed_val))
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
                                return (
                                    datetime.strptime(val_str, fmt).date().isoformat()
                                )
                            except ValueError:
                                continue
                        logging.warning(
                            f"Could not parse date format: '{val_str}' for field '{field_name}'"
                        )
                        return None
                    case _:
                        return transformed_val
            except ValueError:
                logger.warning(
                    f"Could not cast '{transformed_val}' to {data_type} for '{field_name}'"
                )
                return None

    logger.debug(f"No match found for field: {field_name}")
    return None
