import threading
from abc import ABC
from typing import List
from entities.vehicle import Vehicle
from entities.parking_lot import ParkingLot
from enums.gate_type import GateType
from enums.payment_type import PaymentType


class Gate(ABC, threading.Thread):
    def __init__(self, gate_id: str, parking_lot: ParkingLot, gate_type: GateType):
        threading.Thread.__init__(self)
        self.gate_id = gate_id
        self.parking_lot = parking_lot
        self.gate_type = gate_type
        self.vehicle_queue: List[Vehicle] = []
        self.condition = threading.Condition()

    def add_vehicle(self, vehicle: Vehicle):
        with self.condition:
            self.vehicle_queue.append(vehicle)
            self.condition.notify()  # Notify the thread that a new vehicle has arrived

    def run(self):
        pass
