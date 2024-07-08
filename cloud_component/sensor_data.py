from dataclasses import dataclass


@dataclass
class SensorData:
    average_fuel_level: float
    average_power_level: float
    start_timestamp: str
    end_timestamp: str
    status: str
