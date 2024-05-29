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
        handler.setLevel(self.level)
        formatter = logging.Formatter(self.formatter)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        return self.logger

    def __exit__(self, exc_type, exc_value, traceback):
        for handler in self.logger.handlers:
            handler.close()
            self.logger.removeHandler(handler)
