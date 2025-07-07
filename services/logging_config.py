# services/logging_config.py
import logging
import os
from dotenv import load_dotenv

load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_TO_FILE = os.getenv("LOG_TO_FILE", "false").lower() == "true"
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "logs/app.log")
LOG_USE_COLOR = os.getenv("LOG_USE_COLOR", "true").lower() == "true"
LOG_TIMESTAMP_FORMAT = os.getenv("LOG_TIMESTAMP_FORMAT", "%Y-%m-%d %H:%M:%S")

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"

if LOG_TO_FILE:
    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        datefmt=LOG_TIMESTAMP_FORMAT,
        filename=LOG_FILE_PATH,
        filemode="a",
    )
else:
    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        datefmt=LOG_TIMESTAMP_FORMAT,
    )
