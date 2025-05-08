import logging
import os
import tempfile
from src.logger import get_logger


def test_logger_returns_logger_instance():
    logger = get_logger("test_logger")
    assert isinstance(logger, logging.Logger)


def test_logger_respects_env_log_level(monkeypatch):
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    logger = get_logger("debug_logger")
    assert logger.level == logging.DEBUG


def test_logger_writes_to_file(monkeypatch):
    with tempfile.TemporaryDirectory() as tmpdir:
        log_path = os.path.join(tmpdir, "test.log")

        monkeypatch.setenv("LOG_TO_FILE", "true")
        monkeypatch.setenv("LOG_FILE_PATH", log_path)
        monkeypatch.setenv("LOG_LEVEL", "INFO")

        logger = get_logger("file_logger")
        logger.info("This should go to a file")

        # Check file exists and contains log message
        assert os.path.exists(log_path)
        with open(log_path, "r") as f:
            content = f.read()
        assert "This should go to a file" in content


def test_logger_suppresses_lower_levels(monkeypatch, capsys):
    monkeypatch.setenv("LOG_LEVEL", "CRITICAL")
    logger = get_logger("suppress_logger")
    logger.debug("Debug log")
    logger.info("Info log")
    logger.warning("Warning log")
    logger.critical("Critical log")

    captured = capsys.readouterr()
    assert "Debug log" not in captured.out
    assert "Info log" not in captured.out
    assert "Warning log" not in captured.out
    assert "Critical log" in captured.out


def test_logger_disable_color(monkeypatch, capsys):
    monkeypatch.setenv("LOG_USE_COLOR", "false")
    logger = get_logger("no_color_logger")
    logger.info("No color test")

    captured = capsys.readouterr()
    assert "\033[" not in captured.out  # ANSI color codes not present


def test_logger_uses_custom_timestamp_format(monkeypatch, capsys):
    monkeypatch.setenv("LOG_TIMESTAMP_FORMAT", "%H:%M:%S")
    logger = get_logger("timestamp_logger")
    logger.info("Timestamp test")

    captured = capsys.readouterr()
    assert "Timestamp test" in captured.out
    assert "] [INFO] timestamp_logger: Timestamp test" in captured.out


def test_logger_invalid_log_level_fallback(monkeypatch):
    monkeypatch.setenv("LOG_LEVEL", "INVALID_LEVEL")
    logger = get_logger("invalid_logger_level")
    assert logger.level == logging.INFO  # Should default to INFO
