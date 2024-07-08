from db_manager import DatabaseManager
from aggregated_data import AggregatedData
from fuel_data import FuelData
from power_data import PowerData
import jsonpickle


def on_message(client, userdata, msg):
    payload = str(msg.payload.decode())
    print("TOPIC: ", msg.topic, " PAYLOAD: ", payload)
    processed_data = payload.split(':', 1)[1]
    processed_data = processed_data.replace('}', '')
    processed_data = float(processed_data)
    message_handler(msg.topic, processed_data)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK Returned code=", rc)
        client.subscribe("power")
        client.subscribe("fuel")
        client.subscribe("power-station/data")
    else:
        print("Bad connection Returned code=", rc)

def on_subscribe(client, userdata, mid, granted_qos):
    pass


def message_handler(topic, data:float):
    dbObj = DatabaseManager()

    if topic == "power":
        dbObj.add_power_record(data)
        print("Power data is successfully created.")

    elif topic == "fuel":
        dbObj.add_fuel_record(data)
        print("Fuel Data is successfully created.")

    del dbObj

def send_aggregated_data(client):
    dbObj = DatabaseManager()

    dbObj.cur.execute("SELECT * FROM public.fuel_data")
    fuel_data_array = dbObj.cur.fetchall()
    dbObj.cur.execute("SELECT * FROM public.power_data")
    power_data_array = dbObj.cur.fetchall()

    dbObj.cur.execute("SELECT * FROM public.aggregated_data WHERE status like 'CREATED'")
    not_sent_data = dbObj.cur.fetchall()
    not_sent_aggregated_data = []

    if len(not_sent_data) != 0:
        not_sent_aggregated_data = [AggregatedData(aggregated_data_array=data).__dict__ for data in not_sent_data]
        if len(fuel_data_array) == 0 and len(power_data_array) == 0:
            client.publish("power-station/data", jsonpickle.encode(not_sent_aggregated_data))

    if len(fuel_data_array) != 0 and len(power_data_array) != 0:
        fuel_data_array = [FuelData(data) for data in fuel_data_array]
        power_data_array = [PowerData(data) for data in power_data_array]

        new_aggregated_data = AggregatedData(fuel_data_array, power_data_array, "CREATED")
        not_sent_aggregated_data.append(new_aggregated_data.__dict__)
        client.publish("power-station/data", jsonpickle.encode(not_sent_aggregated_data))

        dbObj.add_aggregated_data_record(fuel_data_array, power_data_array, "CREATED")
        dbObj.cur.execute("DELETE FROM public.fuel_data WHERE timestamp <= %s", (new_aggregated_data.end_fuel_timestamp,))
        dbObj.cur.execute("DELETE FROM public.power_data WHERE timestamp <= %s", (new_aggregated_data.end_power_timestamp,))
        dbObj.conn.commit()
    del dbObj




