import logging


class LoggingContextManager:
    def __init__(self, level, filename):
        self.level = level
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
