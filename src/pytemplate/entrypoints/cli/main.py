from src.pytemplate.domain.models import LoggingContextManager


def main():
    level = input("Enter log level (DEBUG/INFO/WARNING/ERROR/CRITICAL): ")

    with LoggingContextManager(level, "app.log") as logging_manager:
        if logging_manager.level == 10:
            logging_manager.debug("This is a debug message.")
        elif logging_manager.level == 20:
            logging_manager.info("This is an informational message.")
        elif logging_manager.level == 30:
            logging_manager.warning("This is a warning message.")
        elif logging_manager.level == 40:
            logging_manager.error("This is an error message.")
        else:
            logging_manager.critical("This is a critical message.")
