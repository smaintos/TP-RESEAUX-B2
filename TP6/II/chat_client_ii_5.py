import asyncio
from aioconsole import ainput

async def get_user_pseudo():
    # Fonction pour obtenir le pseudo de l'utilisateur
    return await ainput("Choisissez votre pseudo : ")

async def send_pseudo(writer, pseudo):
    # Fonction pour envoyer le pseudo au serveur
    greeting = f"Hello|{pseudo}"
    writer.write(greeting.encode())
    await writer.drain()

async def user_input(writer, pseudo):
    # Fonction pour gérer la saisie utilisateur
    while True:
        user_message = await ainput(" -> ")
        formatted_message = f"{user_message}"
        writer.write(formatted_message.encode())
        await writer.drain()

async def receive_messages(reader):
    # Fonction pour recevoir et afficher les messages du serveur
    while True:
        data = await reader.read(1024)
        if not data:
            break
        message = data.decode()
        print(message)

async def main():
    try:
        # Obtenir le pseudo de l'utilisateur
        user_pseudo = await get_user_pseudo()

        # Créer une connexion au serveur
        reader, writer = await asyncio.open_connection(host="10.33.76.197", port=8888)
        print(f"Vous êtes connecté au serveur en tant que {user_pseudo}.")

        # Envoyer le pseudo au serveur
        await send_pseudo(writer, user_pseudo)

        # Lancer les tâches asynchrones en parallèle
        input_task = asyncio.create_task(user_input(writer, user_pseudo))
        receive_task = asyncio.create_task(receive_messages(reader))

        await asyncio.gather(input_task, receive_task)

    except KeyboardInterrupt:
        print("Client interrompu.")

if __name__ == "__main__":
    asyncio.run(main())
