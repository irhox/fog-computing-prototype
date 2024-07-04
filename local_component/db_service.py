from fuel_data import FuelData
from aggregated_data import AggregatedData
from power_data import PowerData

def create_fuel_data(cursor, fuel_data: FuelData):
    cursor.execute("INSERT INTO public.fuel_data(fuel_level) VALUES (%s);", fuel_data.fuel_level)
    print("Fuel data is successfully created.")

def create_power_data(cursor, power_data: PowerData):
    cursor.execute("INSERT INTO public.power_data(power_in_volts) VALUES (%s);", power_data.power_in_volts)
    print("Power data is successfully created.")

def save_aggregated_data(cursor, aggregated_data: AggregatedData):
    aggregated_data.status = "CREATED"
    cursor.execute("INSERT INTO public.aggregated_data(average_fuel_level, average_power_level, start_fuel_timestamp, end_fuel_timestamp, start_power_timestamp, end_power_timestamp, status) "
                   "VALUES(%s, %s, %s, %s, %s, %s, %s);",
                   (aggregated_data.average_fuel_level,
                    aggregated_data.average_power_level,
                    aggregated_data.start_fuel_timestamp,
                    aggregated_data.end_fuel_timestamp,
                    aggregated_data.start_power_timestamp,
                    aggregated_data.end_power_timestamp,
                    aggregated_data.status
                    )
                   )
    print("Saved aggregated data to db.")


