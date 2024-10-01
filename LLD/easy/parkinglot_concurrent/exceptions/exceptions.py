"""
This file is responsible for storing our custom exception which we will
be using in our while app
"""


class InvalidVehicleTypeException(Exception):
    pass


class UnavailableSpotException(Exception):
    pass


class AvailableSpotException(Exception):
    pass


class VehicleNoExitException(Exception):
    pass


class FloorAlreadyPresentException(Exception):
    pass


class InvalidFloorException(Exception):
    pass
