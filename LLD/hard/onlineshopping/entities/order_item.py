from entities.product import Product


class OrderItem:
    def __init__(self, product: Product, quantity: int):
        self._product = product
        self._quantity = quantity

    @property
    def product(self) -> Product:
        return self._product

    @property
    def quantity(self) -> int:
        return self._quantity

    def update_quantity(self, quantity) -> None:
        self._quantity = quantity
