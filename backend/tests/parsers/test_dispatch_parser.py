from typing import Any
from unittest.mock import mock_open
from unittest.mock import patch
from uuid import uuid4

import pytest

from services.parsers.dispatch_parser import parse_csv
from services.parsers.dispatch_parser import parse_pdf


@patch("services.parsers.dispatch_parser.parse_citi_cc_pdf")
@patch("pathlib.Path.open", new_callable=mock_open, read_data=b"%PDF-content%")
def test_dispatch_parser_pdf_happy_path(mock_file: Any, mock_pdf_parser: Any) -> None:
    mock_pdf_parser.return_value = {"status": "ok"}

    result = parse_pdf("citi_cc", "dummy.pdf")

    mock_file.assert_called_once_with("rb")
    mock_pdf_parser.assert_called_once_with(b"%PDF-content%", "citi_cc")
    assert result == {"status": "ok"}


def test_dispatch_parser_pdf_bad_slug() -> None:
    with (
        patch("pathlib.Path.open", new_callable=mock_open, read_data=b"%PDF-content%"),
        pytest.raises(NotImplementedError, match="No PDF parser implemented"),
    ):
        parse_pdf("unknown_bank", "fake.pdf")


def test_parse_pdf_missing_file_raises() -> None:
    with pytest.raises(FileNotFoundError):
        parse_pdf("citi_cc", "nonexistent.pdf")


@patch("services.parsers.dispatch_parser.parse_citi_cc_csv")
@patch("pathlib.Path.open", new_callable=mock_open, read_data="date,amount,desc")
def test_parse_csv_dispatches_correctly(mock_file: Any, mock_csv_parser: Any) -> None:
    mock_csv_parser.return_value = [{"row": 1}]
    statement_id = uuid4()

    result = parse_csv("citi_cc", "dummy.csv", statement_id)

    mock_file.assert_called_once_with("r", encoding="utf-8")
    mock_csv_parser.assert_called_once()
    args, kwargs = mock_csv_parser.call_args
    assert args[1] == statement_id
    assert args[2] == "citi_cc"
    assert result == [{"row": 1}]


def test_parse_csv_unknown_slug_raises() -> None:
    with pytest.raises(NotImplementedError, match="No CSV parser implemented"):
        parse_csv("unknown_bank", "dummy.csv", uuid4())


def test_parse_csv_missing_file_raises() -> None:
    with pytest.raises(FileNotFoundError):
        parse_csv("citi_cc", "missing.csv", uuid4())
