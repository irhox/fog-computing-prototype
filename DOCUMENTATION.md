# Fog Computing Group 6 Report

The prototype simulates the metering of a power system with **two virtual sensors**: voltage and fuel level. Both sensors generate and send their current state as JSON data every 2 seconds. These sensors are based on the following repository: [https://github.com/DamascenoRafael/mqtt-simulator](https://github.com/DamascenoRafael/mqtt-simulator).

To simulate real-world behavior, the fuel level fluctuates between 10% and 100%, imitating fuel consumption and refueling. The voltage fluctuates between 5,000 and 15,000 V:

```bash
[13:21:27] Data published on: fuel
Payload: {"fuel_level": 99.80091345239494}
[13:21:29] Data published on: fuel
Payload: {"fuel_level": 98.93859972584184}
[13:21:31] Data published on: fuel
Payload: {"fuel_level": 97.46911245986342}
```

Sensor behavior, including message frequency, value range, and step size, is configured in a JSON file:

```json
"PREFIX": "power",
"TIME_INTERVAL": 2,
"DATA": [
    {
        "NAME": "power_in_volts",
        "TYPE": "math_expression",
        "RETAIN_PROBABILITY": 0.1,
        "MATH_EXPRESSION": "10000 * (math.sin(x) + 1) / 2 + 5000",
        "INTERVAL_START": 0,
        "INTERVAL_END": 6.28319,
        "MIN_DELTA": 0.1,
        "MAX_DELTA": 0.2
    }
]
```

The sensors send data to a **local (fog) component**, which accumulates the measurements for 10 seconds. The local component then aggregates this data into a single entry by calculating the average fuel level and voltage during that period and recording the timestamps of the first and last received metrics. This process reduces the amount of stored data and decreases the load between the local and cloud nodes by reducing the number of sent messages by a factor of five.

An entry of the aggregated data consists of the following fields:

- id
- average_fuel_level
- average_power_level
- start_fuel_timestamp
- end_fuel_timestamp
- start_power_timestamp
- end_power_timestamp
- status

The `status` field indicates whether an entry was `CREATED`, `SENT` to the cloud, or `SAVED` on the cloud. This allows tracking which entries can be deleted after they are permanently saved on the cloud node. If the cloud component is disconnected, the messages are stored on the local component until the connection is reestablished. Upon receiving the success message from the cloud component that contains the unique id of the data that is saved in the cloud component, the local component deletes those entries in the database in order to not overload this component.

For the publish/subscribe client, we chose an open-source library from the Eclipse Foundation, Paho MQTT: [https://github.com/eclipse/paho.mqtt.python](https://github.com/eclipse/paho.mqtt.python). This library allows connecting to MQTT servers, publishing messages, and subscribing to topics. It is also efficient for devices with limited resources.

The local node publishes data to the topic `power-station/data`. For simplicity, messages are published through the public sandbox MQTT broker service [mqtt.eclipseprojects.io](http://mqtt.eclipseprojects.io). The cloud node subscribes to this topic and receives the messages. Once a message is saved to the database, its status is changed to `SAVED`. The ID of the saved message is then sent back to the local node through the `power-station/data/status-update` topic to confirm successful receipt and allow deletion from the local node.