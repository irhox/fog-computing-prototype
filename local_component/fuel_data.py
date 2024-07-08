from dataclasses import dataclass

@dataclass
class FuelData:
    fuel_level: float
    timestamp: str

    def __init__(self, fuel_data: []):
        self.fuel_level = fuel_data[0]
        self.timestamp = fuel_data[1]