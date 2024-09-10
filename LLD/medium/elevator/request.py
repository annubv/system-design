class Request:
    def __init__(self, source_floor: int, destination_floor: int) -> None:
        self.source_floor = source_floor
        self.destination_floor = destination_floor

    def get_source_floor(self) -> int:
        return self.source_floor

    def get_destination_floor(self) -> int:
        return self.destination_floor
