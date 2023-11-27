import socket
import sys
import signal
import threading
import time
import logging
from logging.handlers import TimedRotatingFileHandler
import os

log_folder = '/var/log/bs_server'

if not os.path.exists(log_folder):
    os.makedirs(log_folder)

log_file_path = os.path.join(log_folder, 'bs_server.log')

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
log_handler = TimedRotatingFileHandler(log_file_path, when='midnight', interval=1, backupCount=7)
log_handler.setLevel(logging.INFO)
log_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logging.getLogger('').addHandler(log_handler)

conn = None  # Variable globale pour stocker la connexion
stop_server = False  # Variable globale pour indiquer l'arrêt du serveur

def parse_arguments():
    host = ''
    port = 13337

    if len(sys.argv) > 1:
        if sys.argv[1] == '-h' or sys.argv[1] == '--help':
            print("Usage : python3 bs_server_II1.py [OPTION] [ARGUMENT]\n\n\t-h, --help \t\t Affiche l'aide\n\t-p, --port \t\t Spécifie le port sur lequel le serveur va écouter\n\n")
            sys.exit(0)
        # On choisit une IP et un port où on va écouter
        if sys.argv[1] == '-p' or sys.argv[1] == '--port':
            if 0 <= int(sys.argv[2]) <= 65535:
                if 0 <= int(sys.argv[2]) <= 1024:
                    raise ValueError("ERROR Le port spécifié est un port privilégié. Spécifiez un port au-dessus de 1024.")
                    sys.exit(2)
                else:
                    port = int(sys.argv[2])
                    logging.info("Lancement du serveur")
                    logging.info(f"Le serveur tourne sur {host}:{port}")
            else:
                raise ValueError("ERROR Le port spécifié n'est pas un port possible (de 0 à 65535).")
                sys.exit(1)
        else:
            port = 13337  # port choisi arbitrairement

    return host, port

while not stop_server:
    try:
        conn, addr = s.accept()
        logging.info(f"Un client {addr[0]} s'est connecté.")
        while not stop_server:
            data = conn.recv(1024)
            if not data:
                break

            logging.info(f"Message reçu d'un client {addr[0]} : {data.decode('utf-8')}")

            if b'meo' in data:
                response = b'Meo a toi confrere.'
                conn.send(response)
                logging.info(f"Réponse envoyée au client {addr[0]} : {response.decode('utf-8')}")
            elif b'waf' in data:
                response = b'Ptdr t ki ?'
                conn.send(response)
                logging.info(f"Réponse envoyée au client {addr[0]} : {response.decode('utf-8')}")
            else:
                response = b'Mes respects humble humain.'
                conn.send(response)
                logging.info(f"Réponse envoyée au client {addr[0]} : {response.decode('utf-8')}")

    except KeyboardInterrupt:
        break  # Sortir de la boucle en cas d'interruption

conn.close()
logging.info("Arrêt du serveur.")


def check_no_clients():
    while not stop_server:
        time.sleep(60)
        logging.warning("Aucun client connecté depuis plus d'une minute.")

def signal_handler(sig, frame):
    global stop_server
    logging.info("Arrêt du serveur.")
    stop_server = True

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    server_thread = threading.Thread(target=run_server)
    server_thread.start()

    check_no_clients_thread = threading.Thread(target=check_no_clients)
    check_no_clients_thread.start()

    server_thread.join()
    check_no_clients_thread.join()