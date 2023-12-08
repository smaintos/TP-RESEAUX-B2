import aiohttp
import aiofiles
import os
import sys
import asyncio


async def get_content(url):
    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.text()

async def write_content(content, file):
    try:
        async with aiofiles.open(file, 'w', encoding='utf-8') as aiofiles.open:
            await aiofiles.open.write(content)

        print(f"Good : {file}")

    except IOError as e:
        print(f"Un peu moins good : {e}")
        sys.exit(1)

async def main():
    if len(sys.argv) != 2:
        print("Usage: python web_sync.py <URL>")
        sys.exit(1)

    url = sys.argv[1]

    os.makedirs("./tmp/web_page", exist_ok=True)

    file = os.path.join("./tmp/web_page", "downloaded_page.html")

    content = await get_content(url)
    await write_content(content, file)


if __name__ == "__main__":
    asyncio.run(main())

