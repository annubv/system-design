from entities.parking_lot import ParkingLot
from entities.gate import Gate
from enums.gate_type import GateType


class EntryGate(Gate):
    def __init__(self, gate_id: str, parking_lot: ParkingLot):
        super().__init__(gate_id, parking_lot, gate_type=GateType.ENTRY)

    def run(self):
        while True:
            with self.condition:
                while not self.vehicle_queue:
                    self.condition.wait()

                vehicle = self.vehicle_queue.pop()

            print(f"Vehicle {vehicle.vehicle_number} entering gate {self.gate_id}")
            self.parking_lot.park_vehicle(vehicle=vehicle)
