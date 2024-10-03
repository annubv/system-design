import threading
import queue
from typing import List
from entities.publisher import Publisher
from entities.message import Message


class Topic:
    def __init__(self, name: str):
        self._name = name
        self._subscribers: List = []
        self._messages = queue.Queue()
        self._message_event = threading.Event()
        self._subscriber_lock = threading.Lock()

    @property
    def name(self):
        return self._name

    @property
    def subscribers(self):
        return self._subscribers

    @property
    def messages(self):
        return self._messages

    @property
    def message_event(self):
        return self._message_event

    def subscribe(self, subscriber):
        with self._subscriber_lock:
            self._subscribers.append(subscriber)
        print(f"{subscriber.name} subscribed to the topic {self._name}")

    def unsubscribe(self, subscriber):
        with self._subscriber_lock:
            # Add value exception check here
            self._subscribers.remove(subscriber)
        print(f"{subscriber.name} unsubscribed to the topic")

    def publish(self, message: Message, publisher: Publisher):
        self._messages.put((message, publisher))
        print(
            f"Publisher {publisher.name} published message: {message.content} on topic {self._name}"
        )
        self._message_event.set()  # Notify subscribers
