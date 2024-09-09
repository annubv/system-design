from abc import ABC, abstractmethod
from log_message import LogMessage


class LogAppender(ABC):

    @abstractmethod
    def append(self, log_message: LogMessage):
        pass
