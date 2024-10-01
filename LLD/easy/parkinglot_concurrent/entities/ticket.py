import time
from entities.vehicle import Vehicle
from entities.parking_spot import ParkingSpot
from exceptions.exceptions import VehicleNoExitException


class Ticket:
    def __init__(
        self,
        ticket_id: str,
        vehicle: Vehicle,
        spot: ParkingSpot,
        entry_time=time.time(),
    ) -> None:
        self.ticket_id = ticket_id
        self.vehicle = vehicle
        self.spot = spot
        self.entry_time = entry_time
        self.exit_time = None
        self.amount = 10  # Setting 10 as default amt, which will be our mininum amt
        self.is_paid = False
        # for more accurate senarios, we will be needing to store billing details

    def calculate_bill(self):
        if not self.exit_time:
            raise VehicleNoExitException("Vehicle hasn't made the exit yet")

        time_spent = (self.exit_time - self.entry_time) // 3600
        self.amount = max(self.amount, round(time_spent * 10))

        # can extend this to another service to have more complex logic on the basis
        # of vehicle type, weekend, etc.

    def mark_as_paid(self):
        self.is_paid = True
