"""Registry loading functions for account and institution configurations."""

from pathlib import Path
from typing import Any

import yaml  # type: ignore[import-untyped]


def load_yaml_registry(filename: str) -> dict[str, Any]:
    """Load YAML registry file from the registry directory.

    Args:
        filename: Name of the YAML file to load

    Returns:
        Dictionary containing the loaded registry data
    """
    path = Path(__file__).parent / filename
    with path.open("r") as f:
        return yaml.safe_load(f)


def get_account_registry() -> dict[str, Any]:
    """Get the account registry configuration.

    Returns:
        Dictionary containing account configurations
    """
    return load_yaml_registry("account_registry.yaml")


def get_institution_registry() -> dict[str, Any]:
    """Get the institution registry configuration.

    Returns:
        Dictionary containing institution configurations
    """
    return load_yaml_registry("institution_registry.yaml")
