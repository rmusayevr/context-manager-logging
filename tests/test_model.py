import logging
from io import StringIO
from unittest.mock import patch

import pytest

from pytemplate.entrypoints.cli.main import main
from src.pytemplate.service.logging import LoggingContextManager


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


def test_init_valid_level_int():
    logging_manager = LoggingContextManager(logging.DEBUG, "app.log")
    assert logging_manager.level == logging.DEBUG


def test_init_valid_level_str():
    logging_manager = LoggingContextManager("INFO", "app.log")
    assert logging_manager.level == logging.INFO


def test_init_invalid_level_str():
    with pytest.raises(ValueError):
        LoggingContextManager("INVALID", "app.log")


def test_validate_log_level_invalid_integer():
    with pytest.raises(ValueError):
        LoggingContextManager(9999, "test.log")


def test_init_invalid_level_type():
    with pytest.raises(TypeError):
        LoggingContextManager(None, "app.log")


@patch("builtins.input", side_effect=["DEBUG"])
@pytest.mark.usefixtures("caplog")
def test_log_level_debug(mock_input, caplog):
    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        main()
        assert "This is a debug message." in caplog.text


@patch("builtins.input", side_effect=["INFO"])
@pytest.mark.usefixtures("caplog")
def test_log_level_info(mock_input, caplog):
    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        main()
        assert "This is an informational message." in caplog.text


@patch("builtins.input", side_effect=["WARNING"])
@pytest.mark.usefixtures("caplog")
def test_log_level_warning(mock_input, caplog):
    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        main()
        assert "This is a warning message." in caplog.text


@patch("builtins.input", side_effect=["ERROR"])
@pytest.mark.usefixtures("caplog")
def test_log_level_error(mock_input, caplog):
    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        main()
        assert "This is an error message." in caplog.text


@patch("builtins.input", side_effect=["CRITICAL"])
@pytest.mark.usefixtures("caplog")
def test_log_level_critical(mock_input, caplog):
    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        main()
        assert "This is a critical message." in caplog.text


@patch("builtins.input", side_effect=["INVALID_LEVEL"])
def test_invalid_log_level(mock_input, caplog):
    with pytest.raises(ValueError):
        main()
        assert "Invalid log level" in caplog.text


@patch("builtins.input", side_effect=[None])
def test_invalid_log_level(mock_input, caplog):
    with pytest.raises(TypeError):
        main()
        assert "Log level must be a string or an integer" in caplog.text
