from typing import Dict, List
from user import User
from expense import Expense
from equal_split import EqualSplit
from percent_split import PercentSplit
from transaction import Transaction
from group import Group


class SplitwiseService:
    _instance = None
    _transaction_count = 0
    _transaction_prefix = "TXN"

    def __init__(self):
        if SplitwiseService._instance is not None:
            raise Exception("This is a singleton")
        else:
            SplitwiseService._instance = self
            self.users: Dict[str, User] = {}
            self.groups: Dict[str, Group] = {}
            self.transactions: List[Transaction] = []

    @staticmethod
    def get_instance():
        if SplitwiseService._instance is None:
            SplitwiseService()
        return SplitwiseService._instance

    def add_user(self, user: User):
        self.users[user.get_user_id()] = user

    def add_group(self, group: Group):
        self.groups[group.get_group_id()] = group

    def add_expense(self, group_id: str, expense: Expense):
        """
        Add expense to the group
        Split the expense bw users (update the amounts)
        Update user balances
        """

        if group_id in self.groups:
            group: Group = self.groups[group_id]
            group.add_expense(expense=expense)
            self._split_expense(expense)
            self._update_user_balance(expense)

    def _split_expense(self, expense: Expense):
        splits = expense.get_splits()
        total_amount = expense.get_amount()
        eq_amount = total_amount / len(splits)

        for split in splits:
            if isinstance(split, EqualSplit):
                split.set_amount(eq_amount)
            elif isinstance(split, PercentSplit):
                perc = split.get_percent()
                split_amount = total_amount * perc / 100.0
                split.set_amount(amount=split_amount)

        return None

    def _update_user_balance(self, expense: Expense):
        paid_by = expense.get_paid_by()
        paid_by_id = paid_by.get_user_id()
        splits = expense.get_splits()

        for split in splits:
            user = split.get_user()
            user_id = user.get_user_id()
            split_amount = split.get_amount()

            if user_id != paid_by_id:
                self._update_balance(paid_by, user, split_amount)
                self._update_balance(user, paid_by, -split_amount)

    def _update_balance(self, user1: User, user2: User, amount: float):
        user_id2 = user2.get_user_id()
        user1.get_balances()[user_id2] = (
            user1.get_balances().get(user_id2) or 0 + amount
        )

    def settle_balances(self, user_id1: str, user_id2):
        """
        Add a transaction
        Update the balance bw the users
        """
        user1: User = self.users[user_id1]
        user2: User = self.users[user_id2]

        if user1 and user2:
            balance = user1.get_balances().get(user_id2) or 0

            if balance > 0:
                self._add_transaction(sender=user2, receiver=user1, amount=balance)
            elif balance < 0:
                self._add_transaction(sender=user1, receiver=user2, amount=-balance)

            user1.get_balances()[user_id2] = 0
            user2.get_balances()[user_id1] = 0

    def _add_transaction(self, sender: User, receiver: User, amount: float):
        transaction = Transaction(
            transaction_id=self._create_transaction_id(),
            sender=sender,
            receiver=receiver,
            amount=amount,
        )
        self.transactions.append(transaction)

    def _create_transaction_id(self):
        self._transaction_count += 1
        return f"{self._transaction_prefix}+{self._transaction_count}"
