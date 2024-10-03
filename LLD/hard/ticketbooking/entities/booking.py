from typing import List
from entities.user import User
from entities.seat import Seat
from entities.show import Show
from enums.booking_status import BookingStatus
from enums.seat_status import SeatStatus


class Booking:
    def __init__(self, booking_id: str, user: User, show: Show, seats: List[Seat]):
        self.__booking_id = booking_id
        self.__user = user
        self.__show = show
        self.__seats = seats
        self.__total_price = sum(seat.price for seat in seats)
        self.__status = BookingStatus.PENDING

    @property
    def booking_id(self):
        return self.__booking_id

    @property
    def user(self):
        return self.__user

    @property
    def show(self):
        return self.__show

    @property
    def seats(self):
        return self.__seats

    @property
    def total_price(self):
        return self.__total_price

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status: BookingStatus):
        self._status = status

    def confirm_booking(self):
        self.status = BookingStatus.CONFIRMED
        print(f"Booking {self.__booking_id} confirmed for User {self.__user.name}")

    def cancel_booking(self):
        self.status = BookingStatus.CANCELLED
        for seat in self.seats:
            seat.status = SeatStatus.AVAILABLE
        print(f"Booking {self.booking_id} cancelled for User {self.user.name}")
