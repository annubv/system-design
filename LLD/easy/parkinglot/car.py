from vehicle import Vehicle
from vehicle_type import VehicleType


class Car(Vehicle):
    def __init__(self, vehicle_number: str):
        super().__init__(vehicle_number=vehicle_number, vehicle_type=VehicleType.CAR)
