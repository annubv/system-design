import threading
from services.online_shopping_service import OnlineShoppingService
from entities.user import User
from entities.product import Product
from entities.shopping_cart import ShoppingCart
from entities.cc_payment import CcPayment
from entities.upi_payment import UpiPayment


class OnlineShoppingDemo:
    def run():
        shopping_service = OnlineShoppingService()

        # Register Users
        user1 = User(user_id="alice", name="Alice")
        user2 = User(user_id="bob", name="Bob")
        shopping_service.register_user(user=user1)
        shopping_service.register_user(user=user2)

        # Add products
        product1 = Product(product_id="phone1", name="Phone 1", quantity=10, price=2000)
        product2 = Product(
            product_id="laptop1", name="Laptop 1", quantity=10, price=20000
        )
        shopping_service.add_product(product=product1)
        shopping_service.add_product(product=product2)

        # Add carts
        cart1 = ShoppingCart()
        cart1.add_item(product=product1, quantity=4)
        cart1.add_item(product=product2, quantity=1)

        cart2 = ShoppingCart()
        cart2.add_item(product=product1, quantity=3)
        cart2.add_item(product=product2, quantity=5)

        # Run orders concurrently
        def place_order_for_user(user_id, cart, payment):
            shopping_service.place_order(user_id, cart, payment)

        thread1 = threading.Thread(
            target=place_order_for_user,
            args=("alice", cart1, CcPayment()),
        )
        thread2 = threading.Thread(
            target=place_order_for_user,
            args=("bob", cart2, UpiPayment()),
        )

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

        # Get order history of alice
        print("Alice's Order History:")
        for order in user1.order_history:
            print("Order ID:", order.order_id)
            print("Total Amount: Rs.", order.total_amount)
            print("Status:", order.status)
            print("----------")


if __name__ == "__main__":
    OnlineShoppingDemo.run()
