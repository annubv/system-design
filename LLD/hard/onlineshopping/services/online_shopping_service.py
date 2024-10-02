import uuid
from typing import Dict, List
from entities.payment import Payment
from entities.user import User
from entities.order import Order
from entities.product import Product
from entities.order_item import OrderItem
from entities.shopping_cart import ShoppingCart

from exceptions.exceptions import (
    DuplicateUserException,
    DuplicateProductException,
    InvalidUserException,
    ProductQtyException,
)


class OnlineShoppingService:
    _instance = None

    def __init__(self):
        if OnlineShoppingService._instance is not None:
            raise Exception("This is a singleton class!")
        else:
            OnlineShoppingService._instance = self
            self.users: Dict[str, User] = {}
            self.orders: Dict[str, Order] = {}
            self.products: Dict[str, Product] = {}

    @staticmethod
    def get_instance():
        if OnlineShoppingService._instance is None:
            return OnlineShoppingService()
        else:
            return OnlineShoppingService._instance

    def register_user(self, user: User):
        user_id = user.user_id
        if user_id in self.users:
            raise DuplicateUserException("User with the same id already exists")

        self.users[user_id] = user
        print(f"User {user_id} registered successfully")

    def get_user(self, user_id: str) -> User:
        if user_id in self.users:
            return self.users[user_id]
        else:
            print("User with the given id does not exists")

    def add_product(self, product: Product):
        product_id = product.product_id
        if product_id in self.products:
            raise DuplicateProductException(
                "Product with the given product id already exists"
            )
        self.products[product_id] = product

    def get_product(self, product_id: str) -> Product:
        if product_id in self.products:
            return self.products[product_id]
        else:
            print("Product with the given id does not exists")

    def search_product(self, keyword: str) -> List[Product]:
        # we can move this to a separate service and apply better techniques using trie
        return [
            product
            for product in self.products.values()
            if keyword.lower() in product.name.lower()
        ]

    def get_order(self, order_id: str) -> Order:
        if order_id in self.orders:
            return self.orders[order_id]
        else:
            print("Order with the given id does not exists")

    def _generate_order_id(self) -> str:
        return "ORDER" + str(uuid.uuid4()).split("-")[0].upper()

    def _calculate_total_amount(self, items: List[OrderItem]) -> float:
        return sum(item.product.price * item.quantity for item in items)

    def place_order(self, user_id: str, cart: ShoppingCart, payment: Payment) -> None:
        if user_id not in self.users:
            raise InvalidUserException("User ID not found")
        user = self.users[user_id]

        locked_products: List[Product] = []
        added_products: Dict[str, int] = {}

        try:
            # Phase 1 -> Lock all the produts
            cart_items = cart.get_items()
            for item in cart_items:
                product = item.product
                product.lock.acquire()
                locked_products.append(product)

                if not product.is_available(item.quantity):
                    raise ProductQtyException(f"Product {product.name} is out of stock")

            # Phase 2 -> Reduce Qtys
            for item in cart_items:
                product = item.product
                added_products[product.product_id] = product.quantity
                product.reduce_quantity(item.quantity)

            # Create order and process payment
            order_id = self._generate_order_id()
            order = Order(order_id=order_id, user=user, items=cart_items)
            total_amount = order.calculate_total_amount()
            user.order_history.append(order)
            self.orders[order_id] = order

            payment.process_payment(total_amount)
            print(f"Order placed successfully for user {user.name}")

        except Exception as order_exception:
            for product in locked_products:
                if product.product_id in added_products:
                    product.quantity = added_products[product.product_id]
            print(f"Order failed: {order_exception}")

        finally:
            # Release all the locks
            for product in locked_products:
                product.lock.release()
