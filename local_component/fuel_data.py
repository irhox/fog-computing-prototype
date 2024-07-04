from dataclasses import dataclass

@dataclass
class FuelData:
    fuel_level: float
    timestamp: str

    def __init__(self, fuel_level: float, timestamp: str):
        self.fuel_level = fuel_level
        self.timestamp = timestamp