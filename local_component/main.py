import paho.mqtt.client as mqtt
from mqtt_service import on_connect, on_message, on_subscribe, send_aggregated_data
import time

MQTT_BROKER_HOST = "mqtt.eclipseprojects.io"
MQTT_BROKER_PORT = 1883


mqtt_client = mqtt.Client(client_id="local-component")

mqtt_client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)



mqtt_client.on_message = on_message
mqtt_client.on_connect = on_connect
mqtt_client.on_subscribe = on_subscribe

while True:
    mqtt_client.loop_start()
    send_aggregated_data(mqtt_client)
    time.sleep(10)
