import socket
import sys
import signal
import threading
import time
import logging
from logging.handlers import TimedRotatingFileHandler
import os

clients_connected = False  # Variable globale pour suivre les clients connectés
stop_server = False  # Variable globale pour indiquer l'arrêt du serveur
conn = None  # Variable globale pour stocker la connexion

def parse_arguments():
    host = ''
    port = 13337

    if len(sys.argv) > 1:
        if sys.argv[1] == '-h' or sys.argv[1] == '--help':
            print("Usage : python3 bs_server_II1.py [OPTION] [ARGUMENT]\n\n\t-h, --help \t\t Affiche l'aide\n\t-p, --port \t\t Spécifie le port sur lequel le serveur va écouter\n\n")
            sys.exit(0)
        elif sys.argv[1] == '-p' or sys.argv[1] == '--port':
            port = validate_port_argument(sys.argv[2])

    return host, port

def validate_port_argument(port_argument):
    port = int(port_argument)
    if not 0 <= port <= 65535:
        raise ValueError("ERROR Le port spécifié n'est pas un port possible (de 0 à 65535).")
    if 0 <= port <= 1024:
        raise ValueError("ERROR Le port spécifié est un port privilégié. Spécifiez un port au-dessus de 1024.")
    return port

# Configuration du logging
log_folder = '/var/log/bs_server'
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

log_file_path = os.path.join(log_folder, 'bs_server.log')

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
log_handler = TimedRotatingFileHandler(log_file_path, when='midnight', interval=1, backupCount=7)
log_handler.setLevel(logging.INFO)
log_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logging.getLogger('').addHandler(log_handler)

def run_server(host, port):
    global clients_connected, stop_server, conn  # Utilisation de variables globales

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)

    logging.info("Le serveur est lancé.")
    clients_connected = True  # Mise à jour de la variable globale

    while not stop_server:
        try:
            conn, addr = s.accept()
            logging.info(f"Un client <{addr[0]}> s'est connecté.")
            while not stop_server:
                data = conn.recv(1024)
                if not data:
                    break

                logging.info(f"Message reçu d'un client <{addr[0]}> : {data.decode('utf-8')}")

                try:
                    result = str(eval(data.decode('utf-8')))
                    conn.send(result.encode('utf-8'))
                    logging.info(f"Résultat envoyé au client <{addr[0]}> : {result}")
                except Exception as e:
                    error_message = f"Erreur lors de l'évaluation de l'expression : {str(e)}"
                    conn.send(error_message.encode('utf-8'))
                    logging.error(error_message)

        except socket.error:
            logging.error("Erreur lors de la connexion.")
            clients_connected = False  # Mise à jour de la variable globale
            break

    if conn:
        conn.close()
    logging.info("Arrêt du serveur.")

def check_no_clients():
    while not stop_server:
        time.sleep(60)
        logging.warning("Aucun client connecté depuis plus d'une minute.")

def signal_handler(sig, frame):
    global stop_server, conn
    logging.info("Arrêt du serveur.")
    stop_server = True
    if conn:
        conn.close()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    host, port = parse_arguments()

    threading.Thread(target=check_no_clients).start()

    run_server(host, port)
