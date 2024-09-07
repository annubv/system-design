from splitwise_service import SplitwiseService
from user import User
from group import Group
from expense import Expense
from equal_split import EqualSplit
from exact_split import ExactSplit
from percent_split import PercentSplit


class SplitwiseDemo:

    @staticmethod
    def run():
        splitwise_service = SplitwiseService.get_instance()

        # Add users
        user1 = User(user_id="user_id1", name="Anu", email="anu@email.com")
        user2 = User(user_id="user_id2", name="Alice", email="alice@email.com")
        user3 = User(user_id="user_id3", name="Kiryu", email="kiryu@email.com")

        splitwise_service.add_user(user=user1)
        splitwise_service.add_user(user=user2)
        splitwise_service.add_user(user=user3)

        # Add group
        group = Group(group_id="group_id", group_name="Dinner")
        group.add_user(user=user1)
        group.add_user(user=user2)
        group.add_user(user=user3)

        splitwise_service.add_group(group=group)

        # Expense
        expense = Expense(
            expense_id="expense_id1",
            paid_by=user1,
            amount=10000,
            description="Dinner @ CP",
        )

        split1 = EqualSplit(user=user1)
        split2 = ExactSplit(user=user2, amount=5000)
        split3 = PercentSplit(user=user3, percent=10.0)

        expense.add_split(split=split1)
        expense.add_split(split=split2)
        expense.add_split(split=split3)

        splitwise_service.add_expense(expense=expense, group_id="group_id")

        splitwise_service.settle_balances(user_id1="user_id1", user_id2="user_id2")

        for user in [user1, user2, user3]:
            user_balances = user.get_balances()
            print("-------")
            print(f"Balances of {user.get_name()}")

            for user_id2 in user_balances:
                user_2 = splitwise_service.users[user_id2]
                print(f"{user_2.get_name()} : {user_balances[user_id2]}")


if __name__ == "__main__":
    SplitwiseDemo.run()
