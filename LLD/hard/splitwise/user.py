from typing import Dict


class User:
    def __init__(self, user_id: str, name: str, email: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.balances: Dict[str, float] = dict()

    def get_user_id(self) -> str:
        return self.user_id

    def get_name(self) -> str:
        return self.name

    def get_email(self) -> str:
        return self.email

    def get_balances(self) -> Dict[str, float]:
        return self.balances