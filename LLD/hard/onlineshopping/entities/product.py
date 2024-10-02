from exceptions.exceptions import ProductQtyException
import threading


class Product:
    def __init__(self, product_id: str, name: str, quantity: int, price: float):
        self._product_id = product_id
        self._name = name
        self._quantity = quantity
        self._price = price
        self.lock = threading.Lock()

    @property
    def product_id(self):
        return self._product_id

    @property
    def name(self):
        return self._name

    @property
    def quantity(self):
        return self._quantity

    @property
    def price(self):
        return self._price

    def is_available(self, requested_quantity: int) -> bool:
        return self._quantity >= requested_quantity

    def update_quantity(self, quantity: int):
        self._quantity += quantity

    def reduce_quantity(self, quantity: int):
        if not self.is_available(quantity):
            raise ProductQtyException(f"Product {self.name} is out of stock")
        self._quantity -= quantity
