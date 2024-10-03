import threading

# BankAccount class with thread-safe debit and credit operations
class BankAccount:
    def __init__(self, balance: float):
        self.balance = balance
        self.lock = threading.Lock()  # Lock to ensure thread safety

    def debit(self, amount: float):
        with self.lock:
            if self.balance >= amount:
                self.balance -= amount
                return True
            else:
                return False

    def credit(self, amount: float):
        with self.lock:
            self.balance += amount

    def get_balance(self):
        return self.balance

# User class that has a UPI ID and associated BankAccount
class User:
    def __init__(self, name: str, upi_id: str, balance: float):
        self.name = name
        self.upi_id = upi_id
        self.bank_account = BankAccount(balance)

# UPI System to manage user registration and money transfers
class UPISystem:
    def __init__(self):
        self.users = {}
        self.users_lock = threading.Lock()  # Lock for user registration

    def register_user(self, name: str, upi_id: str, balance: float):
        with self.users_lock:
            if upi_id not in self.users:
                self.users[upi_id] = User(name, upi_id, balance)
                print(f"User {name} registered with UPI ID: {upi_id} and balance: {balance}")
            else:
                print(f"UPI ID {upi_id} is already registered.")

    def transfer_money(self, sender_upi_id: str, receiver_upi_id: str, amount: float):
        sender = self.users.get(sender_upi_id)
        receiver = self.users.get(receiver_upi_id)

        if not sender:
            print(f"Sender UPI ID {sender_upi_id} not found.")
            return
        if not receiver:
            print(f"Receiver UPI ID {receiver_upi_id} not found.")
            return

        # Lock only sender's account first for debit
        if sender.bank_account.debit(amount):
            print(f"Transfer successful: Debited {amount} from {sender.name}'s account.")

            # Lock receiver's account to credit the amount
            receiver.bank_account.credit(amount)
            print(f"Transfer successful: Credited {amount} to {receiver.name}'s account.")
        else:
            print(f"Transfer failed: Insufficient balance in {sender.name}'s account.")

# Demo function to show concurrent money transfers
def upi_demo():
    upi_system = UPISystem()

    # Registering users
    upi_system.register_user("Alice", "alice@upi", 1000)
    upi_system.register_user("Bob", "bob@upi", 500)
    upi_system.register_user("Charlie", "charlie@upi", 800)

    # Function to simulate money transfer
    def make_transfer(sender_upi, receiver_upi, amount):
        upi_system.transfer_money(sender_upi, receiver_upi, amount)

    # Creating multiple threads for simultaneous transfers
    thread1 = threading.Thread(target=make_transfer, args=("alice@upi", "bob@upi", 200))
    thread2 = threading.Thread(target=make_transfer, args=("bob@upi", "charlie@upi", 300))
    thread3 = threading.Thread(target=make_transfer, args=("charlie@upi", "alice@upi", 100))

    # Start all threads
    thread1.start()
    thread2.start()
    thread3.start()

    # Wait for all threads to complete
    thread1.join()
    thread2.join()
    thread3.join()

    # Final balances after transfers
    print(f"Final balance of Alice: {upi_system.users['alice@upi'].bank_account.get_balance()}")
    print(f"Final balance of Bob: {upi_system.users['bob@upi'].bank_account.get_balance()}")
    print(f"Final balance of Charlie: {upi_system.users['charlie@upi'].bank_account.get_balance()}")

# Running the demo
upi_demo()