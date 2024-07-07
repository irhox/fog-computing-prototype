import paho.mqtt.client as mqtt
from mqtt_configuration import on_connect
from mqtt_configuration import on_message
from mqtt_configuration import on_subscribe


mqtt_client = mqtt.Client(client_id="local-component")

mqtt_client.connect("mqtt.eclipseprojects.io", 1883)



mqtt_client.on_message = on_message
mqtt_client.on_connect = on_connect
mqtt_client.on_subscribe = on_subscribe

mqtt_client.loop_forever()

