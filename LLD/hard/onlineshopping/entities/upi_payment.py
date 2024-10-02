from entities.payment import Payment


class UpiPayment(Payment):
    def process_payment(self, amount: float):
        print(f"Processing UPI payment for amount: {amount}")
