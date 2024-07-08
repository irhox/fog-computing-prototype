import asyncio
import websockets
import json

from cloud_component.sensor_data import SensorData
from cloud_component.sensor_data_dbmanager import insert_sensor_data

clients = {}


async def handle_client(websocket, path):
    client_id = await websocket.recv()
    clients[client_id] = websocket
    print(f"Client {client_id} connected")

    try:
        async for message in websocket:
            data = json.loads(message)
            topic = data['topic']
            payload = data['payload']

            if topic == "power-station/data":
                aggregated_data_list = json.loads(payload)
                for aggregated_data in aggregated_data_list:
                    sensor_data = SensorData(
                        average_fuel_level=aggregated_data['average_fuel_level'],
                        average_power_level=aggregated_data['average_power_level'],
                        start_timestamp=aggregated_data['start_timestamp'],
                        end_timestamp=aggregated_data['end_timestamp'],
                        status=aggregated_data['status']
                    )
                    insert_sensor_data(sensor_data)
                    print(f"Inserted sensor data: {sensor_data}")

            # Broadcast the message to all clients
            for cid, ws in clients.items():
                if cid != client_id:
                    await ws.send(json.dumps({'topic': topic, 'payload': payload}))

    except websockets.ConnectionClosed:
        print(f"Client {client_id} disconnected")
        del clients[client_id]


async def main():
    async with websockets.serve(handle_client, "0.0.0.0", 1883):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
