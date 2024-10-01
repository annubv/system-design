from entities.vehicle import Vehicle
from enums.vehicle_type import VehicleType


class Bike(Vehicle):
    def __init__(self, vehicle_number: str):
        super().__init__(vehicle_number=vehicle_number, vehicle_type=VehicleType.BIKE)
