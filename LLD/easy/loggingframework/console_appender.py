from log_appender import LogAppender
from log_message import LogMessage


class ConsoleAppender(LogAppender):

    def append(self, log_message: LogMessage):
        print(log_message)
