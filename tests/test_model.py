import logging

from src.pytemplate.domain.models import LoggingContextManager


def test_init_logging_with_default_formatter():
    logging_manager = LoggingContextManager(logging.DEBUG, "app.log")
    assert logging_manager.level == logging.DEBUG
    assert logging_manager.filename == "app.log"
    assert logging_manager.handler is None


def test_logging_context_manager_enter_exit():
    with LoggingContextManager(logging.DEBUG, "app.log") as logging_manager:
        assert logging_manager.level == logging.DEBUG
        assert len(logging_manager.handlers) == 1
        assert isinstance(logging_manager.handlers[0], logging.FileHandler)

    assert len(logging_manager.handlers) == 0
