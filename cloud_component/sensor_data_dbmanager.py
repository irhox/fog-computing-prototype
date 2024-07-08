import sqlite3
from cloud_component.sensor_data import SensorData
from datetime import datetime


def insert_sensor_data(sensor_data: SensorData):
    try:
        conn = sqlite3.connect('sensordata.db')
        cursor = conn.cursor()

        average_fuel_level = float(sensor_data.average_fuel_level)
        average_power_level = float(sensor_data.average_power_level)
        start_fuel_timestamp = sensor_data.start_fuel_timestamp.isoformat() if isinstance(
            sensor_data.start_fuel_timestamp, datetime) else sensor_data.start_fuel_timestamp
        end_fuel_timestamp = sensor_data.end_fuel_timestamp.isoformat() if isinstance(sensor_data.end_fuel_timestamp,
                                                                                      datetime) else sensor_data.end_fuel_timestamp
        start_power_timestamp = sensor_data.start_power_timestamp.isoformat() if isinstance(
            sensor_data.start_power_timestamp, datetime) else sensor_data.start_power_timestamp
        end_power_timestamp = sensor_data.end_power_timestamp.isoformat() if isinstance(sensor_data.end_power_timestamp,
                                                                                        datetime) else sensor_data.end_power_timestamp

        insert_query = """
        INSERT INTO SensorData (id, average_fuel_level, average_power_level, start_fuel_timestamp, end_fuel_timestamp, start_power_timestamp, end_power_timestamp, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(insert_query, (sensor_data.id, average_fuel_level, average_power_level,
                                      start_fuel_timestamp, end_fuel_timestamp,
                                      start_power_timestamp, end_power_timestamp,
                                      sensor_data.status))

        conn.commit()
        conn.close()
        print("Data inserted successfully.")
    except Exception as e:
        print(f"Error inserting data into database: {e}")
