import os

from dotenv import load_dotenv

from .logger import get_logger


load_dotenv()
logger = get_logger(__name__)


def main():
    app_name = os.getenv("APP_NAME", "Unnamed App")
    logger.debug("Debug-level log")
    logger.info("Info-level log")
    logger.warning("Warning-level log")
    logger.error("Error-level log")
    logger.critical("Critical-level log")


if __name__ == "__main__":
    main()
