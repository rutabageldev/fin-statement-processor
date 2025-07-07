import logging
import yaml  # type: ignore
from pathlib import Path


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
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            logging.debug(f"✅ Successfully loaded config: {config_name}")
            return config or {}
    except yaml.YAMLError as e:
        logging.exception(f"❌ YAML parsing error in config: {config_path}")
        raise
    except Exception as e:
        logging.exception(f"❌ Unexpected error loading config: {config_path}")
        raise
