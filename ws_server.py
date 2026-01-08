import websockets
import asyncio

connected_clients = set()

async def handle_client(websocket):
    connected_clients.add(websocket)
    print(f"client connected")
    try:
        async for message in websocket:
            for client in connected_clients:
                if client != websocket:
                    await client.send(message)
    except websocket.exceptions.ConnectionClosed:
        pass
    finally:
        connected_clients.remove(websocket)

async def main():
    server = await websockets.serve(handle_client, 'localhost', 5000)
    await server.wait_closed()
    print("Server Closed")

if __name__ == "__main__":
    asyncio.run(main())

    

