from entities.bank_account import BankAcount


class User:
    def __init__(self, name: str, upi_id: str, bank_account: BankAcount) -> None:
        self.__name = name
        self.__upi_id = upi_id
        self.__bank_account = bank_account

    @property
    def name(self):
        return self.__name

    @property
    def upi_id(self):
        return self.__upi_id

    @property
    def bank_account(self):
        return self.__bank_account
