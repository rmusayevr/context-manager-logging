import logging
import os

from src.pytemplate.domain.models import LoggingContextManager


def test_init_logging_with_default_formatter():
    logging_manager = LoggingContextManager(logging.DEBUG, "app.log")
    assert logging_manager.level == logging.DEBUG
    assert logging_manager.filename == "app.log"
    assert logging_manager.formatter == "%(asctime)s - %(levelname)s - %(message)s"


def test_init_logging_with_custom_formatter():
    custom_formatter = "%(asctime)s - %(levelname)s - Custom Message: %(message)s"
    logging_manager = LoggingContextManager(logging.DEBUG, "app.log", custom_formatter)
    assert logging_manager.level == logging.DEBUG
    assert logging_manager.filename == "app.log"
    assert logging_manager.formatter == custom_formatter


def test_logging_context_manager_enter():
    level = logging.DEBUG
    filename = "test.log"
    formatter = "%(asctime)s - %(levelname)s - %(message)s"

    with LoggingContextManager(level, filename, formatter) as logger:
        assert logger.level == level
        assert len(logger.handlers) == 1
        handler = logger.handlers[0]
        assert isinstance(handler, logging.FileHandler)
        assert handler.formatter._fmt == formatter

    assert os.path.exists(filename)

    os.remove(filename)


def test_logging_context_manager_exit():
    level = logging.DEBUG
    filename = "test.log"
    formatter = "%(asctime)s - %(levelname)s - %(message)s"

    with LoggingContextManager(level, filename, formatter) as logger:
        pass

    assert len(logger.handlers) == 0
    assert os.path.exists(filename)

    os.remove(filename)
