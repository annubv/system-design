from typing import Dict
from entities.topic import Topic
from entities.publisher import Publisher
from entities.susbscriber import Subscriber
from entities.message import Message


class PubSubService:
    _instance = None

    def __init__(self):
        if PubSubService._instance is not None:
            raise Exception("This is a singletion class")
        else:
            PubSubService._instance = self
            self._topics: Dict[str, Topic] = {}
            self._publishers: Dict[str, Publisher] = {}
            self._subscribers: Dict[str, Subscriber] = {}

    @staticmethod
    def get_instance():
        if PubSubService._instance is None:
            return PubSubService()
        else:
            return PubSubService._instance

    def create_topic(self, topic_name: str):
        new_topic = Topic(name=topic_name)
        self._topics[topic_name] = new_topic

    def register_publisher(self, publisher_name: str, topic_name: str):
        new_publisher = Publisher(name=publisher_name, topic_name=topic_name)
        self._publishers[publisher_name] = new_publisher

    def register_subscriber(self, topic_name: str, subscriber_name: str):
        if topic_name in self._topics:
            subscriber = Subscriber(
                name=subscriber_name, topic=self._topics[topic_name]
            )
            self._subscribers[f"S:{subscriber_name}-T:{topic_name}"] = subscriber_name
            self._topics[topic_name].subscribe(subscriber)
            subscriber.start()
        else:
            print("Topic does not exist")

    def publish(self, message: Message, publisher_name: str):
        if publisher_name in self._publishers:
            publisher = self._publishers[publisher_name]
            topic_name = publisher.topic_name
            topic = self._topics[topic_name]
            topic.publish(message=message, publisher=publisher)
        else:
            print("Topic does not exist")
