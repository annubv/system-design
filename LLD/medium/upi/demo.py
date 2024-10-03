import threading
from services.upi_service import UpiService
from entities.user import User
from entities.pnb_bank_account import PnbBankAccount
from entities.sbi_bank_account import SbiBankAccount


class UpiDemo:
    @staticmethod
    def run():
        upi_service = UpiService()

        user1 = User(
            name="Alexis",
            upi_id="alexis@upi1",
            bank_account=PnbBankAccount(account_number="P-1", balance=1000),
        )

        user2 = User(
            name="John",
            upi_id="john@upi2",
            bank_account=SbiBankAccount(account_number="S-1", balance=2000),
        )

        user3 = User(
            name="Charlie",
            upi_id="charlie@upi2",
            bank_account=PnbBankAccount(account_number="S-2", balance=2000),
        )

        upi_service.register_user(user=user1)
        upi_service.register_user(user=user2)
        upi_service.register_user(user=user3)

        def make_transfer(sender_upi, receiver_upi, amount):
            upi_service.transfer_money(sender_upi, receiver_upi, amount)

        thread1 = threading.Thread(
            target=make_transfer, args=("john@upi2", "charlie@upi2", 500)
        )
        thread2 = threading.Thread(
            target=make_transfer, args=("charlie@upi2", "alexis@upi1", 24000)
        )
        thread3 = threading.Thread(
            target=make_transfer, args=("alexis@upi1", "john@upi2", 450)
        )

        # Start all threads

        thread1.start()
        thread2.start()
        thread3.start()

        # Wait for all threads to complete
        thread1.join()
        thread2.join()
        thread3.join()

        # Final balances after transfers
        print(
            f"Alexis Balance: {upi_service.users['alexis@upi1'].bank_account.balance}"
        )
        print(f"John Balance: {upi_service.users['john@upi2'].bank_account.balance}")
        print(
            f"Charlie Balance: {upi_service.users['charlie@upi2'].bank_account.balance}"
        )


if __name__ == "__main__":
    UpiDemo.run()
