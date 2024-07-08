import sqlite3

from cloud_component.sensor_data import SensorData


def insert_sensor_data(sensor_data: SensorData):
    conn = sqlite3.connect('sensordata.db')
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO SensorData (average_fuel_level, average_power_level, start_timestamp, end_timestamp, status)
    VALUES (?, ?, ?, ?, ?)
    """

    cursor.execute(insert_query, (sensor_data.average_fuel_level, sensor_data.average_power_level,
                                  sensor_data.start_timestamp, sensor_data.end_timestamp, sensor_data.status))

    conn.commit()
    conn.close()
