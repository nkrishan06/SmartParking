
class ParkingSlot():
    """
    A simple data class to map represent the parking slot/sensor

    state: 1 free parking slot, 0 occupied parking slot
    """
    def __init__(self, rpi_pin: int, id: int, state: int = 1):
        self.rpi_pin = rpi_pin
        self.id = id
        self.state = state