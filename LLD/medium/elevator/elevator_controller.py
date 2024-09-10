from threading import Thread
from typing import List

from elevator import Elevator
from request import Request


class ElevatorController:
    def __init__(self, num_elevators: int, capacity: int):
        self.elevators: List[Elevator] = []
        for i in range(num_elevators):
            elevator = Elevator(id=i + 1, capacity=capacity)
            self.elevators.append(elevator)
            Thread(target=elevator.run).start()

    def request_elevator(self, source_floor: int, destination_floor: int):
        elevator = self.find_optimal_elevator(source_floor=source_floor)
        request = Request(source_floor=source_floor, destination_floor=destination_floor)
        elevator.add_request(request=request)

    def find_optimal_elevator(self, source_floor: int) -> Elevator:
        min_distance = float('inf')
        optimal_elevator = None

        for elevator in self.elevators:
            current_floor = elevator.current_floor
            distance = abs(source_floor - current_floor)
            if distance < min_distance:
                min_distance = distance
                optimal_elevator = elevator

        return optimal_elevator
