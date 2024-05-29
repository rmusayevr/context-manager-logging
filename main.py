import logging


class LoggingContextManager:
    def __init__(self, level, filename, formatter=None):
        self.level = level
        self.filename = filename
        self.formatter = formatter or "%(asctime)s - %(levelname)s - %(message)s"
        self.logger = None

    def __enter__(self):
        self.logger = logging.getLogger(self.filename)
        self.logger.setLevel(self.level)
        handler = logging.FileHandler(self.filename)
        formatter = logging.Formatter(self.formatter)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        return self.logger

    def __exit__(self, exc_type, exc_value, traceback):
        for handler in self.logger.handlers:
            handler.close()
            self.logger.removeHandler(handler)

    def _validate_log_level(self, level):
        if isinstance(level, str):
            level = level.upper()
            if level not in logging._nameToLevel:
                raise ValueError(f"Invalid log level: {level}")
            return logging._nameToLevel[level]
        elif isinstance(level, int):
            if level not in logging._levelToName:
                raise ValueError(f"Invalid log level: {level}")
            return level
        else:
            raise TypeError(
                f"Log level must be a string or an integer, got {type(level)}")


with LoggingContextManager(level='DEBUG', filename='app.log') as logger:
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')
