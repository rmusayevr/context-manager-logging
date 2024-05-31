import logging

class LoggingContextManager:
    def __init__(self, level, filename):
        self.level = self._validate_log_level(level)
        self.filename = filename
        self.logger = logging.getLogger()
        self.handler = None

    def __enter__(self):
        self.logger.setLevel(self.level)
        self.handler = logging.FileHandler(self.filename)
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s")
        self.handler.setFormatter(formatter)
        self.logger.addHandler(self.handler)
        return self.logger

    def __exit__(self, exc_type, exc_value, traceback):
        self.logger.removeHandler(self.handler)
        self.handler.close()

    def _validate_log_level(self, level):
        if isinstance(level, str):
            if level.upper() not in logging._nameToLevel:
                raise ValueError(f"Invalid log level: {level}")
            return logging._nameToLevel[level]
        elif isinstance(level, int):
            if level not in logging._levelToName:
                raise ValueError(f"Invalid log level: {level}")
            return level
        raise TypeError(f"Log level must be a string or an integer, got {type(level)}")

log_level = input("Enter desired log level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL): ")

with LoggingContextManager(log_level, "app.log") as logging_manager:
    if logging_manager.level == 10:
        logging_manager.debug("This is a debug message.")
    elif logging_manager.level == 20:
        logging_manager.info("This is an informational message.")
    elif logging_manager.level == 30:
        logging_manager.warning("This is a warning message.")
    elif logging_manager.level == 40:
        logging_manager.error("This is an error message.")
    elif logging_manager.level == 50:
        logging_manager.critical("This is a critical message.")

