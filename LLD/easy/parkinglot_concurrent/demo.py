import random
import time

from entities.parking_lot import ParkingLot
from entities.entry_gate import EntryGate
from entities.exit_gate import ExitGate
from entities.bike import Bike
from entities.car import Car
from enums.vehicle_type import VehicleType


class ParkingDemo:

    @staticmethod
    def main():
        parking_lot = ParkingLot()

        # Adding floors with spots
        parking_lot.add_floor(floor_id=1, num_spots=10, vehicle_type=VehicleType.CAR)
        parking_lot.add_floor(floor_id=2, num_spots=10, vehicle_type=VehicleType.CAR)
        parking_lot.add_floor(floor_id=3, num_spots=10, vehicle_type=VehicleType.BIKE)

        # Adding gates to the parking lot
        entry_gates = [
            EntryGate(gate_id=f"Entry-{gate_idx}", parking_lot=parking_lot)
            for gate_idx in range(3)
        ]

        exit_gates = [
            ExitGate(gate_id=f"Exit-{i}", parking_lot=parking_lot) for i in range(3)
        ]

        # Start entry and exit gate threads
        all_gates = entry_gates + exit_gates
        for gate in all_gates:
            gate.start()

        # Creating vehicles
        cars = [Car(vehicle_number=f"VC-{i}") for i in range(5)]
        bikes = [Bike(vehicle_number=f"VB-{i}") for i in range(5)]
        vehicles = cars + bikes

        # Distribute vehicles to random entry gates
        for vehicle in vehicles:
            random.choice(entry_gates).add_vehicle(vehicle)

        time.sleep(1)
        print("\nWaiting some time to unpark the vehicles.....")

        time.sleep(5)
        # Add the same vehicles to exit gates for unparking
        for vehicle in vehicles:
            random.choice(exit_gates).add_vehicle(vehicle)

        # Join the threads
        for gate in all_gates:
            gate.join()


if __name__ == "__main__":
    ParkingDemo.main()
