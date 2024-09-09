from logger_service import LoggerService
from logger_config import LoggerConfig
from log_level import LogLevel
from file_appender import FileAppender

class LoggerDemo:
    def run():
        logger = LoggerService.get_instance()

        # Logging with default configuration
        logger.info("This is an information message")
        logger.warning("This is a warning message")
        logger.error("This is an error message")

        # Changing log level and appender
        config = LoggerConfig(LogLevel.DEBUG, FileAppender("./app.log"))
        logger.set_config(config)

        logger.debug("This is a debug message")
        logger.info("This is an information message")


if __name__ == "__main__":
    LoggerDemo.run()
