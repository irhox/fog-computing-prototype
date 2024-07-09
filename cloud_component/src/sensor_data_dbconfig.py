import sqlite3


def create_sensor_data_table():
    conn = sqlite3.connect('sensordata.db')
    cursor = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS SensorData (
        id TEXT PRIMARY KEY,
        average_fuel_level REAL,
        average_power_level REAL,
        start_fuel_timestamp TEXT,
        end_fuel_timestamp TEXT,
        start_power_timestamp TEXT,
        end_power_timestamp TEXT,
        status TEXT
    );
    """

    cursor.execute(create_table_query)
    conn.commit()
    conn.close()
