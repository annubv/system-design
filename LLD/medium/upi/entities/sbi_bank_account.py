from entities.bank_account import BankAcount


class SbiBankAccount(BankAcount):
    def __init__(self, account_number: str, balance: float):
        super().__init__(account_number, balance, "SBI Bank")
