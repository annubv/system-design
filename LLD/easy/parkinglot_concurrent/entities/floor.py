from entities.parking_spot import ParkingSpot
from enums.vehicle_type import VehicleType


class Floor:
    def __init__(
        self, floor_id: int, num_spots: int, vehicle_type: VehicleType
    ) -> None:
        self.floor_id = floor_id
        self.vehicle_type = vehicle_type
        self.parking_spots = [
            ParkingSpot(
                spot_id=f"F{floor_id}-S{idx}",
                floor_id=floor_id,
                vehicle_type=vehicle_type,
            )
            for idx in range(1, num_spots + 1)
        ]

    def get_available_spot(self):
        for spot in self.parking_spots:
            if spot.get_is_available():
                return spot
        return None
