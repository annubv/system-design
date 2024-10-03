from services.pubsub_service import PubSubService
from entities.message import Message


class PubSubDemo:

    @staticmethod
    def run():
        pubsub_service = PubSubService()

        pubsub_service.create_topic(topic_name="topic1")
        pubsub_service.create_topic(topic_name="topic2")

        pubsub_service.register_publisher(publisher_name="pub1", topic_name="topic1")
        pubsub_service.register_publisher(publisher_name="pub2", topic_name="topic2")

        pubsub_service.register_subscriber(topic_name="topic1", subscriber_name="sub1")
        pubsub_service.register_subscriber(topic_name="topic1", subscriber_name="sub2")
        pubsub_service.register_subscriber(topic_name="topic2", subscriber_name="sub1")

        msg = Message(content="Hello World")
        pubsub_service.publish(message=msg, publisher_name="pub1")

        msg2 = Message(content="Hello World 2")
        pubsub_service.publish(message=msg2, publisher_name="pub2")


if __name__ == "__main__":
    PubSubDemo.run()
