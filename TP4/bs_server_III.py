import socket
import sys
import signal
import threading
import time
import logging
from logging.handlers import TimedRotatingFileHandler
import os

clients_connected = False  # Variable globale pour suivre les clients connectés

def parse_arguments():
    host = ''
    port = 13337
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '-h' or sys.argv[1] == '--help':
            print("Usage : python3 bs_server_II1.py [OPTION] [ARGUMENT]\n\n\t-h, --help \t\t Affiche l'aide\n\t-p, --port \t\t Spécifie le port sur lequel le serveur va écouter\n\n")
            sys.exit(0)
        elif sys.argv[1] == '-p' or sys.argv[1] == '--port':
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

    return host, port

def run_server():
    global clients_connected  # Utilisation de la variable globale
    host, port = parse_arguments()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)

    logging.info("Le serveur est lancé.")
    clients_connected = True  # Mise à jour de la variable globale

    while True:
        try:
            conn, addr = s.accept()
            logging.info(f"Un client <{addr[0]}> s'est connecté.")
            while True:
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

    conn.close()
    logging.info("Arrêt du serveur.")

def check_no_clients():
    while True:
        time.sleep(60)
        if not clients_connected:
            logging.warning("Aucun client depuis plus d'une minute.")

threading.Thread(target=check_no_clients).start()

def signal_handler(sig, frame):
    logging.info("Arrêt du serveur.")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    run_server()