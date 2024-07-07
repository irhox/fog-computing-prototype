import json

import paho.mqtt.client as mqtt
from mqtt_service import on_connect
from mqtt_service import on_message
from mqtt_service import on_subscribe
from mqtt_service import send_aggregated_data
import time


mqtt_client = mqtt.Client(client_id="local-component")

mqtt_client.connect("mqtt.eclipseprojects.io", 1883)



mqtt_client.on_message = on_message
mqtt_client.on_connect = on_connect
mqtt_client.on_subscribe = on_subscribe

while True:
    mqtt_client.loop_start()
    send_aggregated_data(mqtt_client)
    time.sleep(10)
