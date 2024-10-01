from entities.parking_lot import ParkingLot
from entities.gate import Gate
from enums.gate_type import GateType
from enums.payment_type import PaymentType


class ExitGate(Gate):
    def __init__(self, gate_id: str, parking_lot: ParkingLot):
        super().__init__(gate_id, parking_lot, gate_type=GateType.EXIT)

    def run(self):
        while True:
            with self.condition:
                while not self.vehicle_queue:
                    self.condition.wait()

                vehicle = self.vehicle_queue.pop()

            print(f"Vehicle {vehicle.vehicle_number} exiting gate {self.gate_id}")
            self.parking_lot.unpark_vehicle(
                vehicle_number=vehicle.get_vehicle_number(),
                payment_type=PaymentType.ONLINE,
            )
