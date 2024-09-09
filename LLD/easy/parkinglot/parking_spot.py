from typing import Optional
from vehicle_type import VehicleType
from vehicle import Vehicle


class ParkingSpot:
    def __init__(self, spot_number: int, vehicle_type: VehicleType):
        self.spot_number = spot_number
        self.vehicle_type = vehicle_type
        self.parked_vehicle: Optional[Vehicle] = None

    def get_availability(self) -> bool:
        return self.parked_vehicle is None

    def get_parked_vehicle(self) -> Vehicle:
        return self.parked_vehicle

    def get_spot_number(self) -> int:
        return self.spot_number

    def get_vehicle_type(self) -> VehicleType:
        return self.vehicle_type

    def park_vehicle(self, vehicle: Vehicle) -> None:
        if (
            self.get_availability()
            and self.get_vehicle_type() == vehicle.get_vehicle_type()
        ):
            self.parked_vehicle = vehicle
        else:
            raise ValueError("Invalid vehicle type or spot already filled")

    def unpark_vehicle(self) -> None:
        self.parked_vehicle = None
