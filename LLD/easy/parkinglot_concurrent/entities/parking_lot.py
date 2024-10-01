import threading
import time
from typing import Dict
from entities.floor import Floor
from entities.vehicle import Vehicle
from entities.ticket import Ticket
from entities.billing import Billing
from enums.vehicle_type import VehicleType
from exceptions.exceptions import (
    FloorAlreadyPresentException,
    InvalidFloorException,
    InvalidVehicleTypeException,
)


class ParkingLot:
    _instance = None

    def __init__(self) -> None:
        if ParkingLot._instance is not None:
            raise Exception("This is a singleton class")
        else:
            ParkingLot._instance = self
            self.floors: Dict[int, Floor] = {}  # storing all the floors here
            self.lock = threading.Lock()
            self.tickets: Dict[str, Ticket] = {}  # storing all the tickets here

    @staticmethod
    def get_instance():
        if ParkingLot._instance is None:
            return ParkingLot()
        else:
            return ParkingLot._instance

    def add_floor(self, floor_id: int, num_spots: int, vehicle_type: VehicleType):
        if floor_id in self.floors:
            raise FloorAlreadyPresentException(
                f"Floor with the given id: {floor_id} is already present"
            )

        new_floor = Floor(
            floor_id=floor_id, num_spots=num_spots, vehicle_type=vehicle_type
        )
        self.floors[floor_id] = new_floor
        print(f"Floor {floor_id} added to the parking lot")

    def park_vehicle(self, vehicle: Vehicle, floor_id=None):
        # Can move this whole logic in a separate repo
        # the user has option to specify the floor
        with self.lock:
            # adding lock here so that the spot can't be filled by 2 vehicles at the same time
            floor = None
            spot = None

            if floor_id:
                if floor_id not in self.floors:
                    raise InvalidFloorException(f"No floor with id {floor_id} found")

                floor = self.floors[floor_id]
                if floor.vehicle_type != vehicle.vehicle_type:
                    raise InvalidVehicleTypeException(
                        "Invalid vehicle type for the requested floor"
                    )
                spot = floor.get_available_spot()

            else:
                for floor_id in self.floors:
                    floor = self.floors[floor_id]
                    if floor.vehicle_type == vehicle.vehicle_type:
                        spot = floor.get_available_spot()
                        if spot:
                            break

            if not spot:
                print("No spot available to park")
                return

            spot.park_vehicle(vehicle=vehicle)

            # create a ticket for this
            ticket = Ticket(
                ticket_id=f"T-{vehicle.get_vehicle_number()}",
                vehicle=vehicle,
                spot=spot,
            )
            self.tickets[vehicle.vehicle_number] = ticket
            print(
                f"Vehicle {vehicle.get_vehicle_number()} parked on floor {floor.floor_id} at spot {spot.spot_id}"
            )

    def unpark_vehicle(self, vehicle_number: str, payment_type: VehicleType):
        with self.lock:
            if vehicle_number not in self.tickets:
                raise InvalidVehicleTypeException("Requested vehicle is not present")

            ticket = self.tickets[vehicle_number]
            ticket.exit_time = time.time()
            ticket.calculate_bill()
            Billing.process_payment(ticket=ticket, payment_type=payment_type)
            spot = ticket.spot
            spot.remove_vehicle()
            del self.tickets[vehicle_number]

            print(f"Vehicle {vehicle_number} has exited. Bill: Rs.{ticket.amount}")
