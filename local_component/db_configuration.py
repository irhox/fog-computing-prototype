import psycopg
import os
from dotenv import load_dotenv

load_dotenv()
connection = psycopg.connect(
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT')
)

cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS public.fuel_data ( "
               "fuel_level NUMERIC NOT NULL,"
               "timestamp TIMESTAMP NOT NULL DEFAULT now() "
               ");")

cursor.execute("CREATE TABLE IF NOT EXISTS public.power_data ( "
               "power_in_volts NUMERIC, "
               "timestamp TIMESTAMP NOT NULL DEFAULT now() "
               ");")

cursor.execute("CREATE TABLE IF NOT EXISTS public.aggregated_data ( "
               "id VARCHAR(255) PRIMARY KEY,"
               "average_fuel_level NUMERIC, "
               "average_power_level NUMERIC, "
               "start_fuel_timestamp TIMESTAMP, "
               "end_fuel_timestamp TIMESTAMP, "
               "start_power_timestamp TIMESTAMP, "
               "end_power_timestamp TIMESTAMP, "
               "status VARCHAR(255) NOT NULL " # CREATED, SENT
               ");")
cursor.close()

connection.commit()
connection.close()