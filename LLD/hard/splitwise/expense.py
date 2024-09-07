from typing import List
from user import User
from split import Split


class Expense:
    def __init__(self, expense_id: str, paid_by: User, amount: float, description: str):
        self.expense_id = expense_id
        self.paid_by = paid_by
        self.description = description
        self.amount = amount
        self.splits: List[Split] = []

    def add_split(self, split: Split):
        self.splits.append(split)

    def get_expense_id(self):
        return self.expense_id

    def get_paid_by(self):
        return self.paid_by

    def get_description(self):
        return self.description

    def get_amount(self):
        return self.amount

    def get_splits(self):
        return self.splits
