from abc import ABC
import threading


class BankAcount(ABC):

    def __init__(self, account_number: str, balance: float, bank_name: str):
        self.__acount_number = account_number
        self.__balance = balance
        self.__bank_name = bank_name
        self.__lock = threading.Lock()

    @property
    def account_number(self):
        return self.__acount_number

    @property
    def balance(self):
        return self.__balance

    @property
    def bank_name(self):
        return self.__bank_name

    def credit(self, amount: float):
        with self.__lock:
            self.__balance += amount
            print(f"{self.__acount_number} received {amount}")

    def debit(self, amount: float):
        with self.__lock:
            if self.__balance >= amount:
                self.__balance -= amount
                return True
            return False
