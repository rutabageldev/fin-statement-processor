# services/account_registry.py
import yaml  # type: ignore
import os

_registry_path = os.path.join(os.path.dirname(__file__), "account_registry.yaml")

with open(_registry_path, "r") as f:
    SUPPORTED_ACCOUNTS = yaml.safe_load(f)
