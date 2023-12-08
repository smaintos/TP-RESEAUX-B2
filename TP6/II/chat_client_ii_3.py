import asyncio
from aioconsole import ainput  # Assurez-vous d'installer le module aioconsole

async def user_input(writer):
    while True:
        user_message = await ainput()
        writer.write(user_message.encode())
        await writer.drain()

async def receive_messages(reader):
    while True:
        data = await reader.read(1024)
        if not data:
            break
        message = data.decode()
        print(f"Message reçu du serveur : {message}")

async def main():
    try:
        reader, writer = await asyncio.open_connection(host="10.33.76.197", port=8888)
        print("Vous êtes connecter au serveur , envoyé un message :")

        input_task = asyncio.create_task(user_input(writer))
        receive_task = asyncio.create_task(receive_messages(reader))

        await asyncio.gather(input_task, receive_task)

    except KeyboardInterrupt:
        print("Client interrompu.")

if __name__ == "__main__":
    asyncio.run(main())
