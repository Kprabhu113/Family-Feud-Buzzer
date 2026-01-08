import websockets
import asyncio

async def chat():
    async with websockets.connect('ws://localhost:5000') as websocket:
        while True:
            message = input("Enter message: ")
            await websocket.send(message)
            response = await websocket.recv()
            print(f"Received: {response}")

if __name__ == "__main__":
    asyncio.run(chat())