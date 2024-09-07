from abc import ABC, abstractmethod
from user import User


class Split(ABC):
    def __init__(self, user: User):
        self.user = user
        self.amount = 0.0

    def set_amount(self, amount: float) -> float:
        self.amount = amount

    @abstractmethod
    def get_amount(self) -> float:
        pass
    
    def get_user(self) -> User:
        return self.user
