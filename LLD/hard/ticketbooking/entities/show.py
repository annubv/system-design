import threading
from typing import Dict, List
from entities.movie import Movie
from entities.seat import Seat

from enums.seat_status import SeatStatus


class Show:
    def __init__(
        self,
        show_id: str,
        theatre,
        movie: Movie,
        start_time: str,
        end_time: str,
        seats: Dict[str, Seat],
    ):
        self.__show_id = show_id
        self.__theatre = theatre
        self.__movie = movie
        self.__start_time = start_time
        self.__end_time = end_time
        self.__seats: Dict[str, Seat] = seats
        self.__seats_lock = threading.Lock()

    @property
    def show_id(self):
        return self.__show_id

    @property
    def theatre(self):
        return self.__theatre

    @property
    def movie(self) -> Movie:
        return self.__movie

    @property
    def start_time(self) -> str:
        return self.__start_time

    @property
    def end_time(self) -> str:
        return self.__end_time

    @property
    def seats(self) -> Dict[str, Seat]:
        return self.__seats

    def get_available_seats(self):
        return [
            seat
            for seat in self.__seats.values()
            if seat.status == SeatStatus.AVAILABLE
        ]

    def book_seats(self, seat_ids: List[str]):
        with self.__seats_lock:
            for seat_id in seat_ids:
                if self.__seats[seat_id].status != SeatStatus.AVAILABLE:
                    raise Exception(f"Seat {seat_id} is not available")

            for seat_id in seat_ids:
                self.__seats[seat_id].status = SeatStatus.BOOKED
                print(f"Seat {seat_id} booked in Show {self.show_id}")

    def add_seats(self, seats: List[Seat]):
        for seat in seats:
            self.__seats[seat.seat_id] = seat
