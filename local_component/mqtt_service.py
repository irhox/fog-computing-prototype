from db_manager import DatabaseManager
from aggregated_data import AggregatedData
from fuel_data import FuelData
from power_data import PowerData
import jsonpickle


MQTT_DATA_PUB_TOPIC = "power-station/data"
MQTT_FUEL_DATA_SUB_TOPIC = "fuel"
MQTT_POWER_DATA_SUB_TOPIC = "power"
MQTT_DATA_CLOUD_SUB_TOPIC = "power-station/data/status-update"

def on_message(client, userdata, msg):

    if msg.topic == MQTT_FUEL_DATA_SUB_TOPIC or msg.topic == MQTT_POWER_DATA_SUB_TOPIC:
        sensor_message_handler(msg.topic, msg.payload)

    elif msg.topic == MQTT_DATA_CLOUD_SUB_TOPIC:
        cloud_message_handler(msg.topic, msg.payload)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK Returned code=", rc)
        client.subscribe(MQTT_POWER_DATA_SUB_TOPIC)
        client.subscribe(MQTT_FUEL_DATA_SUB_TOPIC)
        client.subscribe(MQTT_DATA_CLOUD_SUB_TOPIC)
    else:
        print("Bad connection Returned code=", rc)

def on_subscribe(client, userdata, mid, granted_qos):
    pass


def sensor_message_handler(topic, payload):
    dbObj = DatabaseManager()
    payload_str = str(payload.decode())
    print("TOPIC: ", topic, " PAYLOAD: ", payload_str)
    processed_data = payload_str.split(':', 1)[1]
    processed_data = processed_data.replace('}', '')
    processed_data = float(processed_data)

    if topic == MQTT_POWER_DATA_SUB_TOPIC:
        dbObj.add_power_record(processed_data)
        print("Power data is successfully created.")

    elif topic == MQTT_FUEL_DATA_SUB_TOPIC:
        dbObj.add_fuel_record(processed_data)
        print("Fuel Data is successfully created.")

    del dbObj

def cloud_message_handler(topic, payload):
    dbObj = DatabaseManager()
    if topic == MQTT_DATA_CLOUD_SUB_TOPIC:
        payload_json = jsonpickle.decode(payload)
        dbObj.cur.execute("DELETE FROM public.aggregated_data WHERE id LIKE %(id)s", {"id": payload_json["id"]})
        dbObj.conn.commit()
        print("Deleted data with id: ", payload_json["id"], " after success message from cloud component")

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
            client.publish(MQTT_DATA_PUB_TOPIC, jsonpickle.encode(not_sent_aggregated_data))

    if len(fuel_data_array) != 0 and len(power_data_array) != 0:
        fuel_data_array = [FuelData(data) for data in fuel_data_array]
        power_data_array = [PowerData(data) for data in power_data_array]

        new_aggregated_data = AggregatedData(fuel_data_array, power_data_array, "CREATED")
        not_sent_aggregated_data.append(new_aggregated_data.__dict__)
        client.publish(MQTT_DATA_PUB_TOPIC, jsonpickle.encode(not_sent_aggregated_data))

        dbObj.add_aggregated_data_record(new_aggregated_data)
        dbObj.cur.execute("DELETE FROM public.fuel_data WHERE timestamp <= %s", (new_aggregated_data.end_fuel_timestamp,))
        dbObj.cur.execute("DELETE FROM public.power_data WHERE timestamp <= %s", (new_aggregated_data.end_power_timestamp,))
        dbObj.conn.commit()
    del dbObj




