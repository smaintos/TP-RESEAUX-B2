import asyncio

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Client connecté : {addr}")

    data = await reader.read(100)
    message = data.decode()

    print(f"Message du client : {message}")

    response = f"Hello {addr[0]}:{addr[1]}"
    writer.write(response.encode())
    await writer.drain()

    print(f"Message de bienvenue envoyé à {addr}")

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
