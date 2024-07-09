import paho.mqtt.client as mqtt

from mqtt_broker import on_connect, on_message
from sensor_data_dbconfig import create_sensor_data_table

MQTT_BROKER_HOST = "mqtt.eclipseprojects.io"
MQTT_BROKER_PORT = 1883


def main():
    create_sensor_data_table()
    client = mqtt.Client("cloud-component")
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)
    client.loop_forever()


if __name__ == "__main__":
    main()
