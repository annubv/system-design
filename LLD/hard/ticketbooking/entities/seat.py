from enums.seat_status import SeatStatus
from enums.seat_type import SeatType


class Seat:
    def __init__(
        self, seat_id: str, row: int, column: int, seat_type: SeatType, price: float
    ):
        self.__seat_id = seat_id
        self.__row = row
        self.__column = column
        self.__seat_type = seat_type
        self.__price = price
        self.status: SeatStatus = SeatStatus.AVAILABLE

    @property
    def seat_id(self):
        return self.__seat_id

    @property
    def row(self):
        return self.__row

    @property
    def column(self):
        return self.__column

    @property
    def seat_type(self):
        return self.__seat_type

    @property
    def price(self):
        return self.__price

    def __str__(self):
        return f"Seat {self.__seat_id} ({self.__seat_type}) - {self.status}"
