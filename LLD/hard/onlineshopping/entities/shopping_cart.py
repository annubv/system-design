from typing import Dict, List
from entities.order_item import OrderItem
from entities.product import Product
from exceptions.exceptions import InvalidProductException


class ShoppingCart:
    def __init__(self) -> None:
        self._items: Dict[str, OrderItem] = {}

    def add_item(self, product: Product, quantity: int):
        product_id = product.product_id
        if product_id in self._items:
            item = self._items[product_id]
            item.update_quantity(quantity=item.quantity + quantity)
        else:
            new_item = OrderItem(product=product, quantity=quantity)
            self._items[product_id] = new_item

    def remove_item(self, product_id: str):
        if product_id not in self._items:
            raise InvalidProductException("Product not in cart")
        del self._items[product_id]

    def update_quantity(self, product_id: str, quantity: int):
        if product_id not in self._items:
            raise InvalidProductException("Product not in cart")

        if quantity == 0:
            self.remove_item(product_id=product_id)

        else:
            item = self._items[product_id]
            item.update_quantity(quantity=quantity)

    def get_items(self) -> List[OrderItem]:
        return list(self._items.values())

    def clear(self) -> None:
        self._items.clear()
