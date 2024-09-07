from typing import List
from user import User
from expense import Expense


class Group:
    def __init__(self, group_id: str, group_name: str):
        self.group_id = group_id
        self.group_name = group_name
        self.members: List[User] = []
        self.expenses: List[Expense] = []

    def add_user(self, user: User):
        self.members.append(user)

    def add_expense(self, expense):
        self.expenses.append(expense)

    def get_group_id(self) -> str:
        return self.group_id

    def get_group_name(self) -> str:
        return self.group_name

    def get_members(self) -> List[User]:
        return self.members

    def get_expenses(self) -> List[Expense]:
        return self.expenses
