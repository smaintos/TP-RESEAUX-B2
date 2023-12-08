import asyncio

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Client connecté : {addr}")

    try:
        while True:
            data = await reader.read(1024)
            message = data.decode()

            if not message:
                break

            print(f"Message reçu de {addr[0]}:{addr[1]} : {message}")

            response = "Chat Room en développement, mais repasse bientôt"
            writer.write(response.encode())
            await writer.drain()

    except asyncio.CancelledError:
        pass

    print(f"Client déconnecté : {addr}")
    writer.close()

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
