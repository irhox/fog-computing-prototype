import paho.mqtt.client as mqtt

from cloud_component.mqtt_broker import on_connect, on_message


def main():
    client = mqtt.Client("cloud-component")
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("mqtt.eclipseprojects.io", 1883, 60)

    client.loop_forever()


if __name__ == "__main__":
    main()
