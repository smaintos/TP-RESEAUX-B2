import asyncio
import websockets

async def handle_client(websocket, path):
    try:
        while True:
            client_message = await websocket.recv()
            print(f"Serveur a reçu: {client_message}")

            response_message = f"Hello client ! Received \"{client_message}\""
            await websocket.send(response_message)
            print(f"Serveur a envoyé: {response_message}")

    except websockets.exceptions.ConnectionClosedOK:
        print("La connexion avec le client a été fermée.")

start_server = websockets.serve(handle_client, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
