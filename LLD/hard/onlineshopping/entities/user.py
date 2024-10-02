from typing import List


class User:
    def __init__(self, user_id: str, name: str):
        self._user_id = user_id
        self._name = name
        self._order_history: List = []

    @property
    def name(self):
        return self._name

    @property
    def user_id(self):
        return self._user_id

    @property
    def order_history(self):
        return self._order_history
