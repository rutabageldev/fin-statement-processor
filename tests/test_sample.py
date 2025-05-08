from src.logger import get_logger

logger = get_logger("test")


def test_placeholder():
    logger.info("Running test...")
    assert True
