from dataclasses import dataclass

@dataclass
class PowerData:
    power_in_volts: float
    timestamp: str

    def __init__(self, power_in_volts: float, timestamp: str):
        self.power_in_volts = power_in_volts
        self.timestamp = timestamp