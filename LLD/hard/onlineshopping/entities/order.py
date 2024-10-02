from typing import List
from entities.order_item import OrderItem
from enums.order_status import OrderStatus


class Order:
    def __init__(
        self,
        order_id: str,
        user,
        items: List[OrderItem],
    ):
        self._order_id = order_id
        self._user = user
        self._items = items
        self._total_amount = 0
        self._status = OrderStatus.PENDING

    def calculate_total_amount(self):
        self._total_amount = sum(
            item.product.price * item.quantity for item in self._items
        )
        return self._total_amount

    @property
    def order_id(self):
        return self._order_id

    @property
    def user(self):
        return self._user

    @property
    def items(self):
        return self._items

    @property
    def total_amount(self):
        return self._total_amount

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status: OrderStatus):
        self._status = status
