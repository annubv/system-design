import threading
from services.ticket_booking_service import TicketBookingService
from entities.movie import Movie
from entities.theater import Theatre
from entities.show import Show
from entities.seat import Seat
from entities.user import User
from enums.seat_type import SeatType


class MovieTicketBookingDemo:
    @staticmethod
    def run_demo():
        system = TicketBookingService()

        # Add Movies
        movie1 = Movie("M1", "Inception", "A mind-bending thriller", 150)
        movie2 = Movie("M2", "Interstellar", "A space exploration epic", 180)
        system.add_movie(movie1)
        system.add_movie(movie2)

        # Add Theaters
        theater1 = Theatre("T1", "PVR Cinemas", "Downtown", [])
        theater2 = Theatre("T2", "Cinepolis", "Uptown", [])
        system.add_theatre(theater1)
        system.add_theatre(theater2)

        # Add Shows
        show1 = Show("S1", movie1, theater1, "10:00 AM", "12:30 PM", {})
        show2 = Show("S2", movie2, theater2, "01:00 PM", "04:00 PM", {})
        theater1.add_show(show1)
        theater2.add_show(show2)

        # Add Seats to Shows
        seats = []
        for row in range(1, 6):
            for col in range(1, 11):
                seat_id = f"R{row}C{col}"
                seat_type = SeatType.NORMAL if row > 2 else SeatType.PREMIUM
                price = 100.0 if seat_type == SeatType.NORMAL else 150.0
                seat = Seat(
                    seat_id=seat_id,
                    row=row,
                    column=col,
                    seat_type=seat_type,
                    price=price,
                )

                seats.append(seat)

        show1.add_seats(seats)
        show2.add_seats(seats.copy())

        # Add Users
        user1 = User("U1", "Alice", "alice@example.com")
        user2 = User("U2", "Bob", "bob@example.com")
        system.add_user(user1)
        system.add_user(user2)

        # Function to simulate booking tickets
        def book_tickets(user_id, show_id, seat_ids):
            try:
                booking = system.create_booking(user_id, show_id, seat_ids)
                print(f"Booking successful: {booking.booking_id} for User {user_id}")
            except Exception as e:
                print(e)
                print(f"Booking failed for User {user_id}: {e}")

        # Simulate concurrent bookings
        seat_selection1 = ["R1C1", "R1C2", "R1C3"]
        seat_selection2 = ["R1C2", "R1C3", "R1C4"]

        thread1 = threading.Thread(
            target=book_tickets, args=("U1", "S1", seat_selection1)
        )
        thread2 = threading.Thread(
            target=book_tickets, args=("U2", "S1", seat_selection2)
        )

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

        # Display final seating arrangement
        print("\nFinal Seat Status:")
        for seat in show1.seats.values():
            print(seat)


# Run the demo
if __name__ == "__main__":
    MovieTicketBookingDemo.run_demo()
