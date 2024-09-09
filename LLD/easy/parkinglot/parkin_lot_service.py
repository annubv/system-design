from typing import List
from level import Level
from vehicle import Vehicle


class ParkingLotService:
    _instance = None

    def __init__(self):
        if self._instance is not None:
            raise Exception("This is a singletion class")
        else:
            ParkingLotService._instance = self
            self.levels: List[Level] = []

    @staticmethod
    def get_instance():
        if ParkingLotService._instance is None:
            return ParkingLotService()
        else:
            return ParkingLotService._instance

    def add_level(self, level: Level) -> None:
        self.levels.append(level)

    def park_vehicle(self, vehicle: Vehicle) -> bool:
        for level in self.levels:
            if level.park_vehicle(vehicle=vehicle):
                return True
        return False

    def unpark_vehicle(self, vehhicle: Vehicle) -> bool:
        for level in self.levels:
            if level.unpark_vehicle(vehicle=vehhicle):
                return True
        return False

    def display_availability(self) -> None:
        for level in self.levels:
            level.display_availability()

    def get_levels(self) -> List[Level]:
        return self.levels
