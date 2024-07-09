import logging
import jsonpickle
from sensor_data_dbmanager import insert_sensor_data
from sensor_data import SensorData

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MQTT_TOPIC_DATA = "power-station/data"
MQTT_TOPIC_STATUS_UPDATE = "power-station/data/status-update"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected successfully")
        client.subscribe(MQTT_TOPIC_DATA)
    else:
        logger.error(f"Connection failed with code {rc}")


def on_subscribe(client, userdata, mid, granted_qos):
    pass


def handle_sensor_data(client, data):
    try:
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
        result = insert_sensor_data(sensor_data)
        if result:
            sensor_id, updated_status = result
            if not updated_status:
                status_message = jsonpickle.encode({'id': sensor_id})
            else:
                status_message = jsonpickle.encode({'id': sensor_id, 'status': updated_status})
            client.publish(MQTT_TOPIC_STATUS_UPDATE, status_message)
    except Exception as e:
        logger.error(f"Error processing data: {e}")


def on_message(client, userdata, msg):
    logger.info(f"Received message from topic {msg.topic}")
    payload = msg.payload.decode()

    if msg.topic == MQTT_TOPIC_DATA:
        try:
            aggregated_data = jsonpickle.decode(payload)
            for data in aggregated_data:
                handle_sensor_data(client, data)
        except jsonpickle.JSONDecodeError as e:
            logger.error(f"JSONDecodeError: {e}. Payload: {payload}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
