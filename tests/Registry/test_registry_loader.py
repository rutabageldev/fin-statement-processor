import types

import pytest
import yaml  # type: ignore

from registry import loader


# ---------- Account Registry Tests ----------


def test_get_account_registry_valid_file(monkeypatch, tmp_path):
    # --- Arrange ---
    account_file = tmp_path / "account_registry.yaml"
    account_file.write_text(
        """
citi_cc:
  uuid: "1234"
  metadata:
    institution: citibank
"""
    )
    fake_loader = types.SimpleNamespace(__file__=str(tmp_path / "fake_loader.py"))
    monkeypatch.setattr(loader, "__file__", fake_loader.__file__)

    # --- Act ---
    result = loader.get_account_registry()

    # --- Assert ---
    assert isinstance(result, dict)
    assert "citi_cc" in result
    assert result["citi_cc"]["metadata"]["institution"] == "citibank"


def test_get_account_registry_file_not_found(monkeypatch):
    # --- Arrange ---
    fake_loader = types.SimpleNamespace(__file__="/nonexistent/fake_loader.py")
    monkeypatch.setattr(loader, "__file__", fake_loader.__file__)

    # --- Act & Assert ---
    with pytest.raises(FileNotFoundError):
        loader.get_account_registry()


def test_get_account_registry_invalid_yaml(monkeypatch, tmp_path):
    # --- Arrange ---
    bad_file = tmp_path / "account_registry.yaml"
    bad_file.write_text("this: is: invalid: yaml: : :")

    fake_loader = types.SimpleNamespace(__file__=str(tmp_path / "fake_loader.py"))
    monkeypatch.setattr(loader, "__file__", fake_loader.__file__)

    # --- Act & Assert ---
    with pytest.raises(yaml.YAMLError):
        loader.get_account_registry()


# ---------- Institution Registry Tests ----------


def test_get_institution_registry_valid_file(monkeypatch, tmp_path):
    # --- Arrange ---
    institution_file = tmp_path / "institution_registry.yaml"
    institution_file.write_text(
        """
citibank:
  uuid: "abcd"
"""
    )
    fake_loader = types.SimpleNamespace(__file__=str(tmp_path / "fake_loader.py"))
    monkeypatch.setattr(loader, "__file__", fake_loader.__file__)

    # --- Act ---
    result = loader.get_institution_registry()

    # --- Assert ---
    assert isinstance(result, dict)
    assert "citibank" in result
    assert result["citibank"]["uuid"] == "abcd"


def test_get_institution_registry_file_not_found(monkeypatch):
    fake_loader = types.SimpleNamespace(__file__="/nonexistent/fake_loader.py")
    monkeypatch.setattr(loader, "__file__", fake_loader.__file__)

    with pytest.raises(FileNotFoundError):
        loader.get_institution_registry()


def test_get_institution_registry_invalid_yaml(monkeypatch, tmp_path):
    bad_file = tmp_path / "institution_registry.yaml"
    bad_file.write_text("this: is: invalid: yaml")

    fake_loader = types.SimpleNamespace(__file__=str(tmp_path / "fake_loader.py"))
    monkeypatch.setattr(loader, "__file__", fake_loader.__file__)

    with pytest.raises(yaml.YAMLError):
        loader.get_institution_registry()
