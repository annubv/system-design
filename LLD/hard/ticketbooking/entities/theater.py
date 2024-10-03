from typing import List
from entities.show import Show


class Theatre:
    def __init__(self, theatre_id: str, name: str, location: str, shows: List[Show]):
        self.__theatre_id = theatre_id
        self.__name = name
        self.__location = location
        self.__shows: List[Show] = shows

    @property
    def theatre_id(self) -> str:
        return self.__theatre_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def location(self) -> str:
        return self.__location

    @property
    def shows(self) -> List[Show]:
        return self.__shows

    def add_show(self, show):
        self.__shows.append(show)
        print(f"Show {show.show_id} added to Theater {self.name}")
