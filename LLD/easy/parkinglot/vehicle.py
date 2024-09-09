from abc import ABC

from vehicle_type import VehicleType


class Vehicle(ABC):
    def __init__(self, vehicle_number: str, vehicle_type: VehicleType):
        self.vehicle_number = vehicle_number
        self.vehilce_type = vehicle_type

    def get_vehicle_number(self):
        return self.vehicle_number

    def get_vehicle_type(self):
        return self.vehilce_type
