import sqlite3
from cloud_component.sensor_data import SensorData


def insert_sensor_data(sensor_data: SensorData):
    conn = sqlite3.connect('sensordata.db')
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO SensorData (id, average_fuel_level, average_power_level, start_fuel_timestamp, end_fuel_timestamp, start_power_timestamp, end_power_timestamp, status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """

    cursor.execute(insert_query, (sensor_data.id, sensor_data.average_fuel_level, sensor_data.average_power_level,
                                  sensor_data.start_fuel_timestamp, sensor_data.end_fuel_timestamp,
                                  sensor_data.start_power_timestamp, sensor_data.end_power_timestamp,
                                  sensor_data.status))

    conn.commit()
    conn.close()
