from typing import Dict, List
import threading
import uuid
from entities.user import User
from entities.movie import Movie
from entities.theater import Theatre
from entities.booking import Booking
from enums.booking_status import BookingStatus


class TicketBookingService:
    _instance = None

    def __init__(self):
        if TicketBookingService._instance is not None:
            raise Exception("This is a singleton class!")
        else:
            TicketBookingService._instance = self
            self.__users: Dict[str, User] = {}
            self.__movies: Dict[str, Movie] = {}
            self.__theatres: Dict[str, Theatre] = {}
            self.__bookings: Dict[str, Booking] = {}
            self.__booking_lock = threading.Lock()

    @staticmethod
    def get_instance():
        if TicketBookingService._instance is None:
            return TicketBookingService()
        else:
            return TicketBookingService._instance

    @property
    def users(self):
        return self.__users

    @property
    def movies(self):
        return self.__movies

    @property
    def theatres(self):
        return self.__theatres

    @property
    def bookings(self):
        return self.__bookings

    def add_movie(self, movie: Movie):
        self.__movies[movie.movie_id] = movie
        print(f"Movie {movie.title} added to the system")

    def add_theatre(self, theatre: Theatre):
        self.__theatres[theatre.theatre_id] = theatre
        print(f"Theater {theatre.name} added to the system")

    def add_user(self, user: User):
        self.__users[user.user_id] = user
        print(f"User {user.name} registered")

    def cancel_booking(self, booking_id: str):
        booking = self.__bookings.get(booking_id)
        if booking and booking.status == BookingStatus.CONFIRMED:
            booking.cancel_booking()
        else:
            print(f"Booking {booking_id} cannot be cancelled")

    def create_booking(self, user_id: str, show_id: str, seat_ids: List[str]):
        user = self.__users[user_id]

        # find the show
        show = None
        for theatre in self.__theatres.values():
            for theatre_show in theatre.shows:
                if theatre_show.show_id == show_id:
                    show = theatre_show
                    break
            if show:
                break

        if not show:
            raise Exception("Show not found")

        # book the seats
        with self.__booking_lock:
            try:
                show.book_seats(seat_ids=seat_ids)
                seats = [show.seats[seat_id] for seat_id in seat_ids]
                booking_id = str(uuid.uuid4())
                booking = Booking(
                    booking_id=booking_id, user=user, show=show, seats=seats
                )
                booking.confirm_booking()
                self.__bookings[booking_id] = booking
                return booking

            except Exception as booking_exception:
                print(f"Booking failed: {booking_exception}")
                raise booking_exception
