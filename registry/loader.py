from pathlib import Path
from typing import Any

import yaml  # type: ignore


def load_yaml_registry(filename: str) -> dict[str, Any]:
    path = Path(__file__).parent / filename
    with path.open("r") as f:
        return yaml.safe_load(f)


def get_account_registry() -> dict[str, Any]:
    return load_yaml_registry("account_registry.yaml")


def get_institution_registry() -> dict[str, Any]:
    return load_yaml_registry("institution_registry.yaml")
