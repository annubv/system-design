from logger_config import LoggerConfig
from log_level import LogLevel
from console_appender import ConsoleAppender
from log_message import LogMessage


class LoggerService:
    _instance = None

    def __init__(self):
        if self._instance is not None:
            raise Exception("This is singleton")
        else:
            LoggerService._instance = self
            self.config = LoggerConfig(
                log_level=LogLevel.INFO, log_appender=ConsoleAppender()
            )

    @staticmethod
    def get_instance():
        if LoggerService._instance is not None:
            return LoggerService._instance
        else:
            return LoggerService()

    def set_config(self, config: LoggerConfig):
        self.config = config

    def log(self, level: LogLevel, message: str):
        if level.value >= self.config.get_log_level().value:
            log_message = LogMessage(log_message=message, log_level=level)
            self.config.get_log_appender().append(log_message=log_message)

    def debug(self, message):
        self.log(LogLevel.DEBUG, message)

    def info(self, message):
        self.log(LogLevel.INFO, message)

    def warning(self, message):
        self.log(LogLevel.WARN, message)

    def error(self, message):
        self.log(LogLevel.ERROR, message)
