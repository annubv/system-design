from log_level import LogLevel
import time


class LogMessage:
    def __init__(self, log_message: str, log_level: LogLevel):
        self.message = log_message
        self.level = log_level
        self.timestamp = int(time.time() * 1000)

    def get_message(self):
        return self.message

    def get_level(self):
        return self.level

    def get_timestamp(self):
        return self.timestamp

    def __str__(self):
        return f"[{self.timestamp}] {self.level} - {self.message}"
