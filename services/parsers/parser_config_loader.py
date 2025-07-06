import yaml  # type: ignore
from pathlib import Path


def load_parser_config(config_name: str) -> dict:
    """Load the YAML config for the given parser."""
    config_path = (
        Path(__file__).parent / "pdf" / "config" / f"{config_name}_config.yaml"
    )
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
