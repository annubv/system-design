from typing import List
from vehicle_type import VehicleType
from vehicle import Vehicle
from parking_spot import ParkingSpot


class Level:
    def __init__(self, floor: int):
        self.floor = floor
        self.parking_spots: List[ParkingSpot] = []
        self.num_spots = 0

    def add_parking_spot(self, vehicle_type: VehicleType):
        self.num_spots += 1
        self.parking_spots.append(
            ParkingSpot(spot_number=self.num_spots, vehicle_type=vehicle_type)
        )

    def park_vehicle(self, vehicle: Vehicle) -> bool:
        for spot in self.parking_spots:
            if (
                spot.get_availability()
                and spot.get_vehicle_type() == vehicle.get_vehicle_type()
            ):
                spot.park_vehicle(vehicle=vehicle)
                return True
        return False

    def unpark_vehicle(self, vehicle: Vehicle) -> bool:
        for spot in self.parking_spots:
            if not spot.get_availability() and spot.get_parked_vehicle() == vehicle:
                spot.unpark_vehicle()
                return True
        return False

    def display_availability(self) -> None:
        print(f"Level {self.floor} availability")
        for spot in self.parking_spots:
            spot_availibilty = (
                "Available"
                if spot.get_availability()
                else f"Occupied by {spot.get_parked_vehicle().get_vehicle_number()}"
            )
            print(f"Spot {spot.get_spot_number()} is {spot_availibilty}")
        print("\n")
