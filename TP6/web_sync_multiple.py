from sys import argv
import os
import requests

def url_content(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        content = response.content.decode()
        return content
    else:
        print(f"Échec de la requête : {response.status_code}")
        return None

def save_file(content, file_path):
    try:
        with open(file_path, "w") as web_page_file:
            web_page_file.write(content)
    except Exception as e:
        print(f"Pas good : {e}")

def create_directory(directory):
    try:
        os.makedirs(directory, exist_ok=True)
    except Exception as e:
        print(f"Pas good : {e}")

def readurl_file(url_file_path):
    try:
        with open(url_file_path, "r") as url_file:
            urls = [line.strip() for line in url_file]
            return urls
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier d'URLs : {e}")
        return None

def main():
    if len(argv) != 2:
        print("Usage : python3 web_sync_multiple.py <url_file_path>")
        exit(0)
        
    url_file_path = argv[1]
    
    urls = readurl_file(url_file_path)
    
    if urls is not None:
        for url in urls:
            content = url_content(url)
            if content is not None:
                url_without_protocol = url.replace('http://', '').replace('https://', '')
                directory_path = f"./tmp/web_{url_without_protocol}"
                file_path = os.path.join(directory_path, "downloaded_page.html")

                create_directory(directory_path)
                save_file(content, file_path)

if __name__ == "__main__":
    main()
