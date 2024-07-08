import jsonpickle
from cloud_component.sensor_data_dbmanager import insert_sensor_data
from cloud_component.sensor_data import SensorData


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
        client.subscribe("power-station/data")
    else:
        print(f"Connection failed with code {rc}")


def on_message(client, userdata, msg):
    print(f"Received message from topic {msg.topic}")
    payload = msg.payload.decode()
    # print(f"Payload: {payload}")

    if msg.topic == "power-station/data":
        aggregated_data = jsonpickle.decode(payload)
        for data in aggregated_data:
            # print("Aggregated data received from local component:{}\n".format(data))
            sensor_data = SensorData(
                id=data['id'],
                average_fuel_level=data['average_fuel_level'],
                average_power_level=data['average_power_level'],
                start_fuel_timestamp=data['start_fuel_timestamp'],
                end_fuel_timestamp=data['end_fuel_timestamp'],
                start_power_timestamp=data['start_power_timestamp'],
                end_power_timestamp=data['end_power_timestamp'],
                status=data['status']
            )
            insert_sensor_data(sensor_data)
