from user import User


class Transaction:
    def __init__(
        self, transaction_id: str, sender: User, receiver: User, amount: float
    ):
        self.transaction_id = transaction_id
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def get_transaction_id(self):
        self.transaction_id

    def get_sender(self):
        self.sender

    def get_receiver(self):
        self.receiver

    def get_amount(self):
        self.amount
