from entities.payment import Payment


class CcPayment(Payment):
    def process_payment(self, amount: float):
        print(f"Processing credit card payment for amount: {amount}")
