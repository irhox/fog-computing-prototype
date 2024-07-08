from dataclasses import dataclass
import numpy as np


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
            fuel_data_array=None,
            power_data_array=None,
            status="CREATED",
            aggregated_data_array=None
    ):
        if fuel_data_array is not None and power_data_array is not None:
            self.average_fuel_level = round(np.mean([d.fuel_level for d in fuel_data_array]), 2)
            self.average_power_level = round(np.mean([d.power_in_volts for d in power_data_array]), 2)

            self.start_fuel_timestamp = min(fuel_data_array, key=lambda x: x.timestamp).timestamp
            self.end_fuel_timestamp = max(fuel_data_array, key=lambda x: x.timestamp).timestamp

            self.start_power_timestamp = min(power_data_array, key=lambda x: x.timestamp).timestamp
            self.end_power_timestamp = max(power_data_array, key=lambda x: x.timestamp).timestamp
            self.status = status
        elif aggregated_data_array is not None:
            self.average_fuel_level = aggregated_data_array[0]
            self.average_power_level = aggregated_data_array[1]
            self.start_fuel_timestamp = aggregated_data_array[2]
            self.end_fuel_timestamp = aggregated_data_array[3]
            self.start_power_timestamp = aggregated_data_array[4]
            self.end_power_timestamp = aggregated_data_array[5]
            self.status = aggregated_data_array[6]

