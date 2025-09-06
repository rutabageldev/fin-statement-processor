import types
from pathlib import Path

import pytest
import yaml  # type: ignore[import-untyped]

from services.parsers import parser_config_loader


def test_load_parser_config_valid_file(monkeypatch, tmp_path):
    # --- Arrange ---
    fake_base = tmp_path / "pdf" / "config"
    fake_base.mkdir(parents=True)
    config_file = fake_base / "citi_cc_config.yaml"
    config_file.write_text(
        """account_summary_fields:
  - name: previous_balance
    label_patterns:
      - 'Previous Balance'
    value_pattern: '\\$[\\d,.]+'
    data_type: float
"""
    )

    # Patch __file__ so config_path resolves to tmp
    fake_loader = types.SimpleNamespace(__file__=str(tmp_path / "fake_loader.py"))
    monkeypatch.setattr(parser_config_loader, "__file__", fake_loader.__file__)

    # --- Act ---
    result = parser_config_loader.load_parser_config("citi_cc")

    # --- Assert ---
    assert isinstance(result, dict)
    assert "account_summary_fields" in result
    assert result["account_summary_fields"][0]["name"] == "previous_balance"


def test_load_parser_config_file_not_found(monkeypatch):
    # Patch to point to a known temp path
    fake_path = Path("/nonexistent/fake_loader.py")
    monkeypatch.setattr(parser_config_loader, "__file__", str(fake_path))

    with pytest.raises(FileNotFoundError):
        parser_config_loader.load_parser_config("missing_config")


def test_load_parser_config_invalid_yaml(monkeypatch, tmp_path):
    bad_path = tmp_path / "pdf" / "config"
    bad_path.mkdir(parents=True)
    bad_file = bad_path / "bad_config.yaml"
    bad_file.write_text("this: is: invalid: yaml: : :")

    fake_loader = types.SimpleNamespace(__file__=str(tmp_path / "fake_loader.py"))
    monkeypatch.setattr(parser_config_loader, "__file__", fake_loader.__file__)

    with pytest.raises((ValueError, FileNotFoundError, yaml.YAMLError)):
        parser_config_loader.load_parser_config("bad_config")
