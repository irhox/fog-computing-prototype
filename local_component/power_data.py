from dataclasses import dataclass

@dataclass
class PowerData:
    power_in_volts: float
    timestamp: str

    def __init__(self, power_data: []):
        self.power_in_volts = power_data[0]
        self.timestamp = power_data[1]