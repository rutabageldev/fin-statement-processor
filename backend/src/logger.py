import logging
import os
import sys
from pathlib import Path
from typing import ClassVar

from dotenv import load_dotenv


load_dotenv()


class ColorFormatter(logging.Formatter):
    COLORS: ClassVar[dict[int, str]] = {
        logging.DEBUG: "\033[90m",  # Gray
        logging.INFO: "\033[94m",  # Blue
        logging.WARNING: "\033[93m",  # Yellow
        logging.ERROR: "\033[91m",  # Red
        logging.CRITICAL: "\033[95m",  # Magenta
    }
    RESET: ClassVar[str] = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelno, self.RESET)
        message = super().format(record)
        return f"{color}{message}{self.RESET}"


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        # Load env config
        level_name = os.getenv("LOG_LEVEL", "INFO").upper()
        use_color = os.getenv("LOG_USE_COLOR", "true").lower() == "true"
        log_to_file = os.getenv("LOG_TO_FILE", "false").lower() == "true"
        log_file_path = os.getenv("LOG_FILE_PATH", "logs/app.log")
        timestamp_format = os.getenv("LOG_TIMESTAMP_FORMAT", "%Y-%m-%d %H:%M:%S")

        # Create log formatter
        formatter: logging.Formatter
        if use_color:
            formatter = ColorFormatter(
                "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
                datefmt=timestamp_format,
            )
        else:
            formatter = logging.Formatter(
                "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
                datefmt=timestamp_format,
            )

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Optional file handler
        if log_to_file:
            Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file_path)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        logger.setLevel(getattr(logging, level_name, logging.INFO))

    return logger
