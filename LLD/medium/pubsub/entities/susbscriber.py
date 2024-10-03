import threading
from entities.topic import Topic


class Subscriber(threading.Thread):
    def __init__(self, name: str, topic: Topic):
        super().__init__()
        self._name = name
        self._topic: Topic = topic
        self._msg_offset = -1

    @property
    def name(self):
        return self._name

    @property
    def topic(self):
        return self._topic

    def run(self):
        while True:
            self.topic.message_event.wait()
            while self._msg_offset < self.topic.messages.qsize() - 1:
                self._msg_offset += 1
                msg, publisher = self.topic.messages.queue[self._msg_offset]
                print(
                    f"Subscriber {self.name} received message from {publisher.name}: {msg.content}"
                )
            # self.topic.message_event.clear()
