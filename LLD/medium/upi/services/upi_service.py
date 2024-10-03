import threading
from typing import Dict
from entities.user import User
from entities.bank_account import BankAcount


class UpiService:
    _instance = None

    def __init__(self):
        if UpiService._instance is not None:
            raise Exception("This is a singletion class")
        else:
            UpiService._instance = self
            self.__users: Dict[str, User] = {}
            self.__user_lock = threading.Lock()  # lock for user registration

    @staticmethod
    def get_instance():
        if UpiService._instance is None:
            return UpiService()
        else:
            return UpiService._instance

    @property
    def users(self):
        return self.__users

    def register_user(self, user: User):
        with self.__user_lock:
            upi_id = user.upi_id
            if upi_id in self.__users:
                print(f"UPI ID {upi_id} is already registered.")
            else:
                self.__users[upi_id] = user
                print(
                    f"User {user.name} registered with UPI ID: {upi_id} and balance: {user.bank_account.balance}"
                )

    def transfer_money(self, sender_upi_id: str, receiver_upi_id: str, amount: float):
        if sender_upi_id not in self.__users:
            print("Invalid sender upi id")
            return

        if receiver_upi_id not in self.__users:
            print("Invalid receiver upi id")
            return

        if sender_upi_id == receiver_upi_id:
            print("You cannot send money to yourself")
            return

        sender = self.__users[sender_upi_id]
        receiver = self.__users[receiver_upi_id]

        if sender.bank_account.debit(amount=amount):
            print(f"Debited {amount} from {sender.name}'s account.")
            receiver.bank_account.credit(amount)
            print(f"Credited {amount} to {receiver.name}'s account.")
        else:
            print(f"Transfer failed: Insufficient balance in {sender.name}'s account.")
