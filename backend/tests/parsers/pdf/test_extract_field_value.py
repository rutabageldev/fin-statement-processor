from services.parsers.pdf.parse_citi_cc_pdf import extract_field_value


def test_extract_field_value_happy_path_float() -> None:
    lines = [
        "Minimum Payment Due: $35.00",
        "Previous Balance: $1000.00",
    ]
    label_patterns = [r"Minimum Payment Due"]
    value_pattern = r"\$[\d,.]+"
    data_type = "float"

    result = extract_field_value(
        lines=lines,
        label_patterns=label_patterns,
        value_pattern=value_pattern,
        data_type=data_type,
        field_name="min_payment_due",
    )

    assert result == 35.00


def test_extract_field_value_happy_path_int() -> None:
    lines = ["Points Earned: 1,250"]
    label_patterns = [r"Points Earned"]
    value_pattern = r"[\d,]+"
    data_type = "int"

    result = extract_field_value(
        lines=lines,
        label_patterns=label_patterns,
        value_pattern=value_pattern,
        data_type=data_type,
        field_name="points_earned",
    )

    assert result == 1250


def test_extract_field_value_happy_path_date() -> None:
    lines = ["Statement Period: 06/30/2025"]
    label_patterns = [r"Statement Period"]
    value_pattern = r"\d{2}/\d{2}/\d{4}"
    data_type = "date"

    result = extract_field_value(
        lines=lines,
        label_patterns=label_patterns,
        value_pattern=value_pattern,
        data_type=data_type,
        field_name="bill_period_end",
    )

    assert result == "2025-06-30"


def test_extract_field_value_returns_string() -> None:
    lines = ["Account Type: Credit"]
    label_patterns = [r"Account Type"]
    value_pattern = r"Credit"
    data_type = "string"

    result = extract_field_value(
        lines=lines,
        label_patterns=label_patterns,
        value_pattern=value_pattern,
        data_type=data_type,
        field_name="account_type",
    )

    assert result == "Credit"


def test_extract_field_value_label_match_no_value_match() -> None:
    lines = [
        "Minimum Payment Due: TBD",  # Label matches but value is non-numeric
    ]
    label_patterns = [r"Minimum Payment Due"]
    value_pattern = r"\$[\d,.]+"  # Only matches dollar amounts
    data_type = "float"

    result = extract_field_value(
        lines=lines,
        label_patterns=label_patterns,
        value_pattern=value_pattern,
        data_type=data_type,
        field_name="min_payment_due",
    )

    assert result is None


def test_extract_field_value_dollars_to_points_transform() -> None:
    lines = ["Points Earned: $2.50"]
    label_patterns = [r"Points Earned"]
    value_pattern = r"\$[\d.]+"
    data_type = "int"
    transform = "dollars_to_points"

    result = extract_field_value(
        lines=lines,
        label_patterns=label_patterns,
        value_pattern=value_pattern,
        data_type=data_type,
        field_name="points_earned",
        transform=transform,
    )

    assert result == 250


def test_extract_field_value_percent_to_decimal_transform() -> None:
    lines = ["APR: 21.99"]
    label_patterns = [r"APR"]
    value_pattern = r"[\d.]+"
    data_type = "float"
    transform = "percent_to_decimal"

    result = extract_field_value(
        lines=lines,
        label_patterns=label_patterns,
        value_pattern=value_pattern,
        data_type=data_type,
        field_name="interest_rate",
        transform=transform,
    )

    assert result == 0.2199


def test_extract_field_value_invalid_transform_value_returns_none() -> None:
    lines = ["APR: not_a_number"]
    label_patterns = [r"APR"]
    value_pattern = r"not_a_number"
    data_type = "float"
    transform = "percent_to_decimal"

    result = extract_field_value(
        lines=lines,
        label_patterns=label_patterns,
        value_pattern=value_pattern,
        data_type=data_type,
        field_name="interest_rate",
        transform=transform,
    )

    assert result is None


def test_extract_field_value_unknown_transform_skips_safely() -> None:
    lines = ["Some Value: 123.45"]
    label_patterns = [r"Some Value"]
    value_pattern = r"[\d.]+"
    data_type = "float"
    transform = "nonexistent_transform"

    result = extract_field_value(
        lines=lines,
        label_patterns=label_patterns,
        value_pattern=value_pattern,
        data_type=data_type,
        field_name="some_field",
        transform=transform,
    )

    assert result == 123.45  # skips transform and casts raw
