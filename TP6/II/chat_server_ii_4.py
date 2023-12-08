import asyncio

CLIENTS = {}

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')

    if addr in CLIENTS:
        print(f"Client déjà connecté : {addr}")
        return

    CLIENTS[addr] = {"r": reader, "w": writer}
    print(f"Nouveau client connecté : {addr}")

    try:
        while True:
            data = await reader.read(1024)
            if not data:
                break

            sender_info = f"{addr[0]}:{addr[1]}"
            message = data.decode()
            formatted_message = f"{sender_info} a dit : {message}"

            for client_addr, client_info in CLIENTS.items():
                if client_addr != addr:
                    client_info["w"].write(formatted_message.encode())
                    await client_info["w"].drain()

            print(f"Message redistribué à tous les clients : {formatted_message}")

    except asyncio.CancelledError:
        pass

    finally:
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
