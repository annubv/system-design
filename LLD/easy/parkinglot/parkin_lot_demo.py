from parkin_lot_service import ParkingLotService
from car import Car
from bike import Bike
from truck import Truck
from level import Level
from vehicle_type import VehicleType


class ParkingLotDemo:
    def run():
        parking_lot_service = ParkingLotService.get_instance()

        car1 = Car(vehicle_number="C-1234")
        car2 = Car(vehicle_number="C-1235")
        bike1 = Bike(vehicle_number="B-1236")
        truck1 = Truck(vehicle_number="T-1237")

        level1 = Level(floor=1)
        level2 = Level(floor=2)

        level1.add_parking_spot(vehicle_type=VehicleType.CAR)
        level1.add_parking_spot(vehicle_type=VehicleType.BIKE)
        level2.add_parking_spot(vehicle_type=VehicleType.BIKE)

        parking_lot_service.add_level(level=level1)
        parking_lot_service.add_level(level=level2)

        parking_lot_service.get_levels()[1].add_parking_spot(
            vehicle_type=VehicleType.TRUCK
        )

        parking_lot_service.park_vehicle(vehicle=car1)
        parking_lot_service.park_vehicle(vehicle=bike1)
        parking_lot_service.park_vehicle(vehicle=truck1)
        parking_lot_service.park_vehicle(vehicle=car2)

        parking_lot_service.display_availability()


if __name__ == "__main__":
    ParkingLotDemo.run()
