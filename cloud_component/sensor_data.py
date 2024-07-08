from dataclasses import dataclass


@dataclass
class SensorData:
    id: str
    average_fuel_level: float
    average_power_level: float
    start_fuel_timestamp: str
    end_fuel_timestamp: str
    start_power_timestamp: str
    end_power_timestamp: str
    status: str
