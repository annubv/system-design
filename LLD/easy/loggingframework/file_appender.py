from log_message import LogMessage
from log_appender import LogAppender


class FileAppender(LogAppender):
    def __init__(self, file_location: str):
        self.file_location = file_location

    def append(self, log_message: LogMessage):
        with open(self.file_location, "a") as file:
            file.write(str(log_message) + "\n")
