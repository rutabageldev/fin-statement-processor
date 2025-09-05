import logging
from pathlib import Path

import yaml  # type: ignore


def load_parser_config(config_name: str) -> dict:
    """Load the YAML config for the given parser."""
    config_path = (
        Path(__file__).parent / "pdf" / "config" / f"{config_name}_config.yaml"
    )
    logging.debug(f"🔍 Looking for config at: {config_path}")

    if not config_path.exists():
        logging.error(f"❌ Config file not found: {config_path}")
        raise FileNotFoundError(f"Config file not found: {config_path}")

    try:
        with config_path.open(encoding="utf-8") as f:
            config = yaml.safe_load(f)
            logging.debug(f"✅ Successfully loaded config: {config_name}")
            return config or {}
    except yaml.YAMLError:
        logging.exception(f"❌ YAML parsing error in config: {config_path}")
        raise
    except Exception:
        logging.exception(f"❌ Unexpected error loading config: {config_path}")
        raise
