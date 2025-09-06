from datetime import UTC
from datetime import datetime
from uuid import uuid4

import pytest

from models.statement import StatementData


def test_statement_data_from_dict_missing_field_raises():
    data = {
        "bill_period_end": "2025-06-30"
        # 'bill_period_start' is missing
    }

    with pytest.raises(KeyError, match="bill_period_start"):
        StatementData.from_dict(
            data=data,
            institution_id=uuid4(),
            account_id=uuid4(),
            file_url="s3://bucket/stmt.pdf",
            uploaded_at=datetime(2025, 7, 1, tzinfo=UTC),
        )


def test_statement_data_from_dict_invalid_date_format_raises():
    data = {
        "bill_period_start": "30-06-2025",  # invalid format (should be ISO)
        "bill_period_end": "2025-06-30",
    }

    with pytest.raises(ValueError):
        StatementData.from_dict(
            data=data,
            institution_id=uuid4(),
            account_id=uuid4(),
        )


def test_statement_data_missing_fields():
    with pytest.raises(KeyError):
        StatementData.from_dict(
            data={},  # completely empty
            institution_id=uuid4(),
            account_id=uuid4(),
        )


def test_statement_data_invalid_date_format():
    bad_data = {
        "bill_period_start": "01-2025-06",  # wrong format
        "bill_period_end": "2025-06-30",
    }
    with pytest.raises(ValueError):
        StatementData.from_dict(
            data=bad_data,
            institution_id=uuid4(),
            account_id=uuid4(),
        )


def test_statement_data_uploaded_at_defaults():
    data = {"bill_period_start": "2025-06-01", "bill_period_end": "2025-06-30"}
    result = StatementData.from_dict(
        data=data,
        institution_id=uuid4(),
        account_id=uuid4(),
    )
    assert isinstance(result.uploaded_at, datetime)


def test_statement_data_missing_dates():
    data = {}
    with pytest.raises(KeyError):
        StatementData.from_dict(
            data=data,
            institution_id=uuid4(),
            account_id=uuid4(),
            uploaded_at=datetime.now(UTC),
        )


def test_statement_data_extra_fields():
    data = {
        "bill_period_start": "2025-06-01",
        "bill_period_end": "2025-06-30",
        "unexpected_field": "extra",
    }
    result = StatementData.from_dict(
        data=data,
        institution_id=uuid4(),
        account_id=uuid4(),
        uploaded_at=datetime.now(UTC),
    )
    assert result.period_start.isoformat() == "2025-06-01"
    assert result.period_end.isoformat() == "2025-06-30"


def test_statement_data_null_dates():
    data = {"bill_period_start": None, "bill_period_end": None}
    with pytest.raises(TypeError):
        StatementData.from_dict(
            data=data,
            institution_id=uuid4(),
            account_id=uuid4(),
            uploaded_at=datetime.now(UTC),
        )
