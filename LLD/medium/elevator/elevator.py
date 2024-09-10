import time
from threading import Lock, Condition
from typing import List
from direction import Direction
from request import Request


class Elevator:
    def __init__(self, id: int, capacity: int):
        self.id = id
        self.capacity = capacity
        self.current_floor = 1
        self.direction = Direction.UP
        self.requests: List[Request] = []
        self.lock = Lock()
        self.condition = Condition(self.lock)

    def add_request(self, request: Request) -> None:
        with self.lock:
            if len(self.requests) < self.capacity:
                self.requests.append(request)
                print(
                    f"Elevator {self.id} added request: from {request.get_source_floor()} to {request.get_destination_floor()}"
                )
                self.condition.notify_all()

    def get_next_request(self) -> Request:
        with self.lock:
            while not self.requests:
                self.condition.wait()
            return self.requests.pop()

    def process_requests(self):
        while True:
            with self.lock:
                while self.requests:
                    request = self.get_next_request()
                    self.process_request(request)

                self.condition.wait()

    def process_request(self, request: Request):
        start_floor = request.get_source_floor()
        end_floor = request.get_destination_floor()

        if start_floor < end_floor:
            self.direction = Direction.UP
            for i in range(start_floor, end_floor + 1):
                self.current_floor = i
                print(f"Elevator {self.id} has reached floor {self.current_floor}")
                time.sleep(1)  # simulating elevator movement

        elif start_floor > end_floor:
            self.direction = Direction.DOWN
            for i in range(start_floor, end_floor - 1, -1):
                self.current_floor = i
                print(f"Elevator {self.id} has reached floor {self.current_floor}")
                time.sleep(1)  # simulating elevator movement

    def run(self):
        self.process_requests()
