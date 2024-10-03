class Publisher:
    def __init__(self, name, topic_name):
        self._name = name
        self._topic_name = topic_name

    @property
    def name(self):
        return self._name

    @property
    def topic_name(self):
        return self._topic_name
