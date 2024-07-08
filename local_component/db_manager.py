from aggregated_data import AggregatedData
import psycopg
import os
from dotenv import load_dotenv

# Database Manager Class
class DatabaseManager:

    def __init__(self):
        load_dotenv()
        self.conn = psycopg.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'))
        self.cur = self.conn.cursor()

    def add_power_record(self, arg:float):
        self.cur.execute("INSERT INTO public.power_data(power_in_volts) VALUES (%(volts)s);", {"volts": arg})
        self.conn.commit()

    def add_fuel_record(self, arg:float):
        self.cur.execute("INSERT INTO public.fuel_data(fuel_level) VALUES (%(fuel)s);", {"fuel": arg})
        self.conn.commit()

    def add_aggregated_data_record(self, fuel_data_array: [], power_data_array:[], status):
        aggregated_data = AggregatedData(fuel_data_array, power_data_array, status)
        self.cur.execute("INSERT INTO public.aggregated_data(id, average_fuel_level, average_power_level, start_fuel_timestamp, end_fuel_timestamp, start_power_timestamp, end_power_timestamp, status) "
        "VALUES(%(id)s, %(fuel)s, %(power)s, %(startf)s, %(endf)s, %(startp)s, %(endp)s, %(status)s);",
        {
            "id": aggregated_data.id,
            "fuel": aggregated_data.average_fuel_level,
            "power": aggregated_data.average_power_level,
            "startf": aggregated_data.start_fuel_timestamp,
            "endf": aggregated_data.end_fuel_timestamp,
            "startp": aggregated_data.start_power_timestamp,
            "endp": aggregated_data.end_power_timestamp,
            "status": aggregated_data.status
        })
        self.conn.commit()

    def __exit__(self):
        self.cur.close()
        self.conn.close()
