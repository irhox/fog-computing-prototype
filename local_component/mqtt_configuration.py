from db_service import DatabaseManager

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




