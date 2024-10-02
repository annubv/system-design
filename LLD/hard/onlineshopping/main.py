import threading
from abc import ABC, abstractmethod
from typing import List, Dict

# User Class
class User:
    def __init__(self, user_id: str, name: str):
        self.user_id = user_id
        self.name = name
        self.order_history: List[Order] = []

    def view_order_history(self):
        return self.order_history

# Product Class
class Product:
    def __init__(self, product_id: str, name: str, price: float, quantity: int):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.lock = threading.Lock()  # Lock for product quantity

    def check_availability(self, requested_quantity: int) -> bool:
        return self.quantity >= requested_quantity

    def reduce_quantity(self, requested_quantity: int):
        if self.check_availability(requested_quantity):
            self.quantity -= requested_quantity
        else:
            raise Exception(f"Not enough stock for product {self.name}")

# Shopping Cart Class
class ShoppingCart:
    def __init__(self):
        self.items: Dict[Product, int] = {}  # product -> quantity

    def add_item(self, product: Product, quantity: int):
        if product in self.items:
            self.items[product] += quantity
        else:
            self.items[product] = quantity

    def remove_item(self, product: Product):
        if product in self.items:
            del self.items[product]

# OrderStatus Enum
class OrderStatus:
    PENDING = "Pending"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"

# OrderItem Class
class OrderItem:
    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity

# Order Class
class Order:
    def __init__(self, user: User, items: List[OrderItem]):
        self.user = user
        self.items = items
        self.status = OrderStatus.PENDING

    def calculate_total(self):
        return sum(item.product.price * item.quantity for item in self.items)

    def update_status(self, status: str):
        self.status = status

# Payment Interface
class Payment(ABC):
    @abstractmethod
    def process_payment(self, amount: float):
        pass

class CreditCardPayment(Payment):
    def process_payment(self, amount: float):
        print(f"Processing credit card payment for amount: {amount}")

class PayPalPayment(Payment):
    def process_payment(self, amount: float):
        print(f"Processing PayPal payment for amount: {amount}")

# Online Shopping Service
class OnlineShoppingService:
    def __init__(self):
        self.products: Dict[str, Product] = {}  # product_id -> Product
        self.users: Dict[str, User] = {}  # user_id -> User

    def add_product(self, product: Product):
        self.products[product.product_id] = product

    def add_user(self, user: User):
        self.users[user.user_id] = user

    def place_order(self, user_id: str, shopping_cart: ShoppingCart, payment: Payment):
        user = self.users.get(user_id)
        if not user:
            raise Exception("User not found")

        order_items = []
        for product, quantity in shopping_cart.items.items():
            # Locking product quantity to prevent race condition
            with product.lock:
                if product.check_availability(quantity):
                    product.reduce_quantity(quantity)
                    order_items.append(OrderItem(product, quantity))
                else:
                    raise Exception(f"Product {product.name} is out of stock")

        order = Order(user=user, items=order_items)
        user.order_history.append(order)
        total_amount = order.calculate_total()
        payment.process_payment(total_amount)
        print(f"Order placed successfully for user {user.name}")

# Demo Code
def main():
    shopping_service = OnlineShoppingService()

    # Add products
    product1 = Product(product_id="P1", name="Laptop", price=1000, quantity=10)
    product2 = Product(product_id="P2", name="Phone", price=500, quantity=10)

    shopping_service.add_product(product1)
    shopping_service.add_product(product2)

    # Add users
    user1 = User(user_id="U1", name="Alice")
    user2 = User(user_id="U2", name="Bob")

    shopping_service.add_user(user1)
    shopping_service.add_user(user2)

    # Shopping carts for users
    cart1 = ShoppingCart()
    cart2 = ShoppingCart()

    cart1.add_item(product1, 10)  # Alice adds 1 laptop
    cart2.add_item(product1, 10)  # Bob adds 2 laptops

    # Run orders concurrently
    def place_order_for_user(shopping_service, user_id, cart, payment):
        try:
            shopping_service.place_order(user_id, cart, payment)
        except Exception as e:
            print(e)

    thread1 = threading.Thread(target=place_order_for_user, args=(shopping_service, "U1", cart1, CreditCardPayment()))
    thread2 = threading.Thread(target=place_order_for_user, args=(shopping_service, "U2", cart2, PayPalPayment()))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

if __name__ == "__main__":
    main()