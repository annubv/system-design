from abc import ABC
from enums.vehicle_type import VehicleType


class Vehicle(ABC):
    # marking as abstract class
    def __init__(self, vehicle_number: str, vehicle_type: VehicleType):
        self.vehicle_number = vehicle_number
        self.vehicle_type = vehicle_type

    def get_vehicle_number(self):
        return self.vehicle_number

    def get_vehicle_type(self):
        return self.vehicle_type
