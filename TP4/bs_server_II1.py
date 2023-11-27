import socket
import argparse
import sys
import signal

conn = None  # Définir la variable conn en dehors du bloc try

def print_help():
    print("Usage: python3 bs_server_II1.py [OPTION] [ARGUMENT]\n\n"
          "\t-a, --help \t\t Affiche l'aide\n"
          "\t-p, --port \t\t Spécifie le port sur lequel le serveur va écouter\n\n")
    sys.exit(0)

def handle_port_argument(port):
    if 0 <= port <= 65535:
        if 0 <= port <= 1024:
            raise ValueError("ERROR Le port spécifié est un port privilégié. Spécifiez un port au dessus de 1024.")
            sys.exit(2)
        else:
            return port
    else:
        raise ValueError("ERROR Le port spécifié n'est pas un port possible (de 0 à 65535).")
        sys.exit(1)

def main():
    global conn  # Utiliser la variable globale conn

    parser = argparse.ArgumentParser(description="Serveur bidon avec quelques réponses spéciales.")
    parser.add_argument("-p", "--port", type=int, help="Spécifie le port sur lequel le serveur va écouter.")
    parser.add_argument("-a", "--help", action="store_true", help="Affiche l'aide.")  # Modifier le raccourci -h en -a

    args = parser.parse_args()

    if args.help:
        print_help()

    # On choisit une IP et un port où on va écouter
    host = ''  # string vide signifie, dans ce contexte, toutes les IPs de la machine

    if args.port is not None:
        port = handle_port_argument(args.port)
    else:
        port = 13337  # port choisi arbitrairement

    # On crée un objet socket
    # SOCK_STREAM c'est pour créer un socket TCP (pas UDP donc)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # On demande à notre programme de se bind sur notre port
    s.bind((host, port))

    # Place le programme en mode écoute derrière le port auquel il s'est bind
    s.listen(1)

    # Petite boucle infinie (bah oui c'est un serveur)
    # À chaque itération la boucle reçoit des données et les traite
    while True:
        try:
            conn, addr = s.accept()
            print("Un client vient de se co et son IP c'est", addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break

                if b'meo' in data:
                    conn.send(b'Meo a toi confrere.')
                elif b'waf' in data:
                    conn.send(b'Ptdr t ki ?')
                else:
                    conn.send(b'Mes respects humble humain.')

        except socket.error:
            print("Error Occurred.")
            break

def signal_handler(sig, frame):
    if conn:
        conn.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == "__main__":
    main()
