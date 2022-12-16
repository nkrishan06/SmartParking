
class ParkingSlot():
    """
    A simple data class to map represent the parking slot/sensor

    state: 0 free parking slot, 1 occupied parking slot. By default, is marked as free (0).
    """
    def __init__(self, rpi_pin: int, id: int, state: int = 0):
        self.rpi_pin = rpi_pin
        self.id = id
        self.state = state