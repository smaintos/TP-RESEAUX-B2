import requests
import os
import sys

def get_content(url):
        response = requests.get(url)
        response.raise_for_status()  

        return response.text 


def write_content(content, file):
    try:
 
        with open(file, 'w', encoding='utf-8') as file:
            file.write(content)

        print(f"Contenu écrit avec succès dans {file}")

    except IOError as e:
        print(f"Erreur lors de l'écriture dans le fichier : {e}")
        sys.exit(1)

def main():

    if len(sys.argv) != 2:
        print("Usage: python web_sync.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    content = get_content(url)

    os.makedirs("/tmp/web_page", exist_ok=True)

    file = os.path.join("/tmp/web_page", "downloaded_page.html")

    write_content(content, file)

if __name__ == "__main__":
    main()
