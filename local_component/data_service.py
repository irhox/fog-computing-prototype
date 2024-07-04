import numpy as np

from fuel_data import FuelData
from aggregated_data import AggregatedData
from power_data import PowerData


def create_aggregated_data(cursor):
    cursor.execute("SELECT * FROM public.fuel_data")
    fuel_data_array = cursor.fetchall()
    cursor.execute("SELECT * FROM public.power_data")
    power_data_array = cursor.fetchall()

    average_fuel_level = np.mean([d.fuel_level for d in fuel_data_array])
    average_power_level = np.mean([d.power_in_volts for d in power_data_array])

    start_fuel_timestamp = min(fuel_data_array, key=lambda x: x.timestamp).timestamp
    end_fuel_timestamp = max(fuel_data_array, key=lambda x: x.timestamp).timestamp

    start_power_timestamp = min(power_data_array, key=lambda x: x.timestamp).timestamp
    end_power_timestamp = max(power_data_array, key=lambda x: x.timestamp).timestamp

    aggregated_data = AggregatedData(
        average_fuel_level, average_power_level,
        start_fuel_timestamp, end_fuel_timestamp,
        start_power_timestamp, end_power_timestamp,
        "CREATED")
    return aggregated_data