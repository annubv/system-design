class Message:
    def __init__(self, content: str):
        self._content = content

    @property
    def content(self):
        return self._content
