"""Citi Credit Card PDF statement parser."""

import logging
import re
from datetime import UTC
from datetime import datetime
from io import BytesIO
from typing import Any

import pdfplumber

from services.normalization import normalize_cc_details
from services.normalization import normalize_debt_details
from services.normalization import normalize_statement_data
from services.parsers.parser_config_loader import load_parser_config


logging.getLogger("pdfminer").setLevel(logging.ERROR)

logger = logging.getLogger(__name__)

TRANSFORM_REGISTRY = {
    "dollars_to_points": lambda val: int(abs(float(val)) * 100),
    "percent_to_decimal": lambda val: round(float(val) / 100, 4),
}


def parse_citi_cc_pdf(file_bytes: bytes, account_slug: str) -> dict[str, Any]:
    """Parse Citi Credit Card PDF statement.

    Args:
        file_bytes: PDF file content as bytes
        account_slug: Account identifier

    Returns:
        Dictionary containing normalized statement data

    Raises:
        Exception: If PDF parsing fails
    """
    try:
        with pdfplumber.open(BytesIO(file_bytes)) as pdf:
            statement_lines: list[str] = []

            for page in pdf.pages:
                raw_text = page.extract_text()
                if raw_text:
                    raw_lines = raw_text.splitlines()
                    cleaned_lines = [line.strip() for line in raw_lines if line.strip()]
                    statement_lines.extend(cleaned_lines)

            account_summary = extract_account_summary(statement_lines)

            statement_data = normalize_statement_data(
                parsed_data=account_summary,
                account_slug=account_slug,
                file_url=None,
                uploaded_at=datetime.now(UTC),
            )

            debt_data = normalize_debt_details(
                parsed_data=account_summary,
                account_slug=account_slug,
                statement_id=statement_data["statement_data"].id,
            )

            cc_data = normalize_cc_details(
                parsed_data=account_summary,
                account_slug=account_slug,
                statement_id=statement_data["statement_data"].id,
            )

            return {
                "statement_data": statement_data["statement_data"].model_dump(),
                "statement_details": statement_data["statement_details"].model_dump(),
                "debt_details": debt_data["debt_details"].model_dump(),
                "credit_card_details": cc_data["credit_card_details"].model_dump(),
            }

    except Exception:
        logger.exception("❌ Failed to parse Citi CC PDF")
        raise


def extract_account_summary(statement_lines: list[str]) -> dict[str, Any]:
    """Extract account summary data from statement text lines.

    Args:
        statement_lines: List of text lines from the PDF

    Returns:
        Dictionary containing extracted account summary data
    """
    config = load_parser_config("citi_cc")
    summary_fields = config.get("account_summary_fields", [])
    summary_data: dict[str, Any] = {}

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

        except (ValueError, re.error, KeyError) as e:
            logger.warning("⚠️ Failed to extract field '%s': %s", field["name"], e)
            summary_data[field["name"]] = None  # Preserve key for consistency

    return summary_data


def _apply_transform(raw_val: str, transform: str | None) -> str | float | int:
    """Apply transformation to raw value."""
    if transform and transform in TRANSFORM_REGISTRY:
        return TRANSFORM_REGISTRY[transform](raw_val)
    return raw_val


def _convert_to_type(
    val: str | float, data_type: str, field_name: str
) -> str | float | int | None:
    """Convert value to specified data type."""
    match data_type:
        case "float":
            return float(val)
        case "int":
            return int(float(val))
        case "date":
            val_str = str(val)
            for fmt in ("%m/%d/%Y", "%m-%d-%Y", "%m-%d-%y", "%m/%d/%y", "%Y-%m-%d"):
                try:
                    return (
                        datetime.strptime(val_str, fmt)
                        .replace(tzinfo=UTC)
                        .date()
                        .isoformat()
                    )
                except ValueError:
                    continue
            logger.warning(
                "Could not parse date format: '%s' for field '%s'", val_str, field_name
            )
            return None
        case _:
            return val


def extract_field_value(
    lines: list[str],
    label_patterns: list[str],
    value_pattern: str,
    data_type: str = "string",
    field_name: str = "unknown",
    transform: str | None = None,
) -> str | float | int | None:
    """Extract and process field value from statement lines.

    Args:
        lines: List of text lines from the statement
        label_patterns: Regex patterns to match field labels
        value_pattern: Regex pattern to extract the value
        data_type: Target data type for conversion
        field_name: Name of field for logging
        transform: Optional transformation to apply

    Returns:
        Processed field value or None if not found/invalid
    """
    for line in lines:
        if any(re.search(label, line) for label in label_patterns):
            match_obj = re.search(value_pattern, line)
            logger.debug("line matched for '%s': %s", field_name, line)
            if not match_obj:
                logger.warning(
                    "Found label match but no value match in line: '%s'",
                    line,
                )
                return None

            raw_val = match_obj.group(0).strip().replace("$", "").replace(",", "")

            try:
                transformed_val = _apply_transform(raw_val, transform)
                return _convert_to_type(transformed_val, data_type, field_name)
            except ValueError:
                logger.warning(
                    "Could not process value '%s' for field '%s'",
                    raw_val,
                    field_name,
                )
                return None

    logger.debug("No match found for field: %s", field_name)
    return None
