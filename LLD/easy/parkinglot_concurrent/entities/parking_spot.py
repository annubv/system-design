from entities.vehicle import Vehicle
from enums.vehicle_type import VehicleType
from exceptions.exceptions import (
    InvalidVehicleTypeException,
    UnavailableSpotException,
    AvailableSpotException,
)


class ParkingSpot:
    def __init__(self, spot_id: int, floor_id: int, vehicle_type: VehicleType):
        self.spot_id = spot_id
        self.is_available = True  # by default there is no vehicle parked here
        self.vehicle_number = None
        self.floor_id = floor_id
        self.vehicle_type = vehicle_type

    def get_spot_id(self):
        # We typically don't need getters and setters in python
        # Making this one for future code extensibility
        return self.spot_id

    def get_is_available(self):
        return self.is_available

    def park_vehicle(self, vehicle: Vehicle):
        if vehicle.vehicle_type != self.vehicle_type:
            raise InvalidVehicleTypeException("Invalid vehicle type for the required spot")

        if not self.is_available:
            raise UnavailableSpotException("Parking spot is pre occupied")

        self.vehicle_number = vehicle.get_vehicle_number()
        self.is_available = False
        print(f"Spot {self.spot_id} parked with vehicle {self.vehicle_number}")

    def remove_vehicle(self):
        if self.is_available:
            raise AvailableSpotException("Parking spot is already available")

        removed_vehicle = self.vehicle_number
        self.vehicle_number = None
        self.is_available = True
        print(f"Vehicle {removed_vehicle} unparked from spot {self.spot_id}")
