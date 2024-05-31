import logging


class LoggingContextManager:
    def __init__(self, level, filename):
        self.level = self._validate_log_level(level)
        self.filename = filename
        self.logger = None
        self.handler = None

    def __enter__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(self.level)
        self.handler = logging.FileHandler(self.filename)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
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
