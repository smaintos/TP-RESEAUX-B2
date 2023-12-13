import asyncio

CLIENTS = {}

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')

    if addr in CLIENTS:
        print(f"Client déjà connecté : {addr}")
        return

    try:
        # Attente du premier message du client contenant le pseudo
        data = await reader.read(1024)
        if not data or not data.startswith(b"Hello|"):
            print(f"Message invalide de {addr}. Déconnexion.")
            return

        # Isoler le pseudo du message "Hello|<PSEUDO>"
        pseudo = data.decode().split("|")[1].strip()

        # Stocker les informations du client dans le dictionnaire
        CLIENTS[addr] = {"r": reader, "w": writer, "pseudo": pseudo}

        # Annoncer l'arrivée du nouveau client à tous les clients
        announce_message = f"Annonce : {pseudo} a rejoint la chatroom"
        for client_addr, client_info in CLIENTS.items():
            if client_addr != addr:
                client_info["w"].write(announce_message.encode())
                await client_info["w"].drain()

        print(f"Nouveau client connecté : {addr}, pseudo : {pseudo}")

        # Attendre et redistribuer les messages du client
        while True:
            data = await reader.read(1024)
            if not data:
                break

            sender_info = CLIENTS[addr]["pseudo"]
            message = data.decode()
            formatted_message = f"{sender_info}: {message}"

            for client_addr, client_info in CLIENTS.items():
                if client_addr != addr:
                    client_info["w"].write(formatted_message.encode())
                    await client_info["w"].drain()

            print(f"Message redistribué à tous les clients : {formatted_message}")

    except asyncio.CancelledError:
        pass

    finally:
        # Gérer la déconnexion du client
        del CLIENTS[addr]
        print(f"Client déconnecté : {addr}")

async def main():
    server = await asyncio.start_server(
        handle_client, '10.33.76.197', 8888
    )

    addr = server.sockets[0].getsockname()
    print(f'Serveur en attente de connexions sur {addr}')

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
