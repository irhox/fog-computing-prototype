import asyncio
import websockets
import json

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
