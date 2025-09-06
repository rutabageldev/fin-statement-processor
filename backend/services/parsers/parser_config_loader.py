import logging
from pathlib import Path
from typing import Any

import yaml


logger = logging.getLogger(__name__)


def load_parser_config(config_name: str) -> dict[str, Any]:
    """Load the YAML config for the given parser."""
    config_path = (
        Path(__file__).parent / "pdf" / "config" / f"{config_name}_config.yaml"
    )
    logger.debug("🔍 Looking for config at: %s", config_path)

    if not config_path.exists():
        logger.error("❌ Config file not found: %s", config_path)
        error_msg = f"Config file not found: {config_path}"
        raise FileNotFoundError(error_msg)

    try:
        with config_path.open(encoding="utf-8") as f:
            config: dict[str, Any] | None = yaml.safe_load(f)
            logger.debug("✅ Successfully loaded config: %s", config_name)
            return config or {}
    except yaml.YAMLError:
        logger.exception("❌ YAML parsing error in config: %s", config_path)
        raise
    except Exception:
        logger.exception("❌ Unexpected error loading config: %s", config_path)
        raise
