import aiohttp
import aiofiles
import asyncio
from sys import argv
import os
import time 

start_prog = time.time()
async def url_content(url: str, session: aiohttp.ClientSession):
    try:
        async with session.get(url, ssl=False) as response:
            if response.status == 200:
                content = await response.text()
                return content
            else:
                print(f"Échec de la requête : {response.status}")
                return None
    except Exception as e:
        print(f"Erreur lors de la requête : {e}")
        return None


async def save_file(content, file_path):
    try:
        async with aiofiles.open(file_path, "w") as web_page_file:
            await web_page_file.write(content)
    except Exception as e:
        print(f"Pas good : {e}")

async def create_directory(directory):
    try:
        os.makedirs(directory, exist_ok=True)
    except Exception as e:
        print(f"Pas good : {e}")

async def readurl_file(url_file_path):
    try:
        with open(url_file_path, "r") as url_file:
            urls = [line.strip() for line in url_file]
            return urls
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier d'URLs : {e}")
        return None

async def main():
    if len(argv) != 2:
        print("Usage : python3 web_sync_multiple.py <url_file_path>")
        exit(0)
        
    url_file_path = argv[1]
    
    urls = await readurl_file(url_file_path)
    
    if urls is not None:
        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in urls:
                content = await url_content(url, session)
                if content is not None:
                    url_without_protocol = url.replace('http://', '').replace('https://', '')
                    directory_path = f"./tmp/web_{url_without_protocol}"
                    file_path = os.path.join(directory_path, "downloaded_page.html")

                    tasks.append(create_directory(directory_path))
                    tasks.append(save_file(content, file_path))

            await asyncio.gather(*tasks)
end_prog = time.time()

if __name__ == "__main__":
    asyncio.run(main())

    print (f"Temps d'exécution : {end_prog - start_prog} secondes")

