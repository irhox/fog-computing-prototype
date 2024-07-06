from dataclasses import dataclass
import sqlite3


@dataclass
class SensorData:
    average_fuel_level: float
    average_power_level: float
    start_timestamp: str
    end_timestamp: str
    status: str


conn = sqlite3.connect('sensordata.db')

cursor = conn.cursor()

create_table_query = """
CREATE TABLE IF NOT EXISTS SensorData (
    average_fuel_level REAL,
    average_power_level REAL,
    start_timestamp TEXT,
    end_timestamp TEXT,
    status TEXT
);
"""

cursor.execute(create_table_query)

conn.commit()
conn.close()
