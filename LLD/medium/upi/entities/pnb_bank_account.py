from entities.bank_account import BankAcount


class PnbBankAccount(BankAcount):
    def __init__(self, account_number: str, balance: float):
        super().__init__(account_number, balance, "PNB Bank")
