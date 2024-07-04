from dataclasses import dataclass
@dataclass
class AggregatedData:
    average_fuel_level: float
    average_power_level: float
    start_fuel_timestamp: str
    end_fuel_timestamp: str
    start_power_timestamp: str
    end_power_timestamp: str
    status: str

    def __init__(
            self,
            average_fuel_level: float,
            average_power_level: float,
            start_fuel_timestamp: str,
            end_fuel_timestamp: str,
            start_power_timestamp: str,
            end_power_timestamp: str,
            status: str
    ):
        self.average_fuel_level = average_fuel_level
        self.average_power_level = average_power_level
        self.start_fuel_timestamp = start_fuel_timestamp
        self.end_fuel_timestamp = end_fuel_timestamp
        self.start_power_timestamp = start_power_timestamp
        self.end_power_timestamp = end_power_timestamp
        self.status = status
