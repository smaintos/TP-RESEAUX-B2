import argparse
import socket
import sys
import signal

def parse_arguments():
    parser = argparse.ArgumentParser(description='Description de votre programme.')
    parser.add_argument('-p', '--port', type=int, help='Spécifie le port à utiliser (par défaut: 13337)')
    return parser.parse_args()

def validate_port(port):
    if port is not None:
        if port < 0 or port > 65535:
            print("ERROR: Le port spécifié n'est pas un port possible (de 0 à 65535).")
            sys.exit(1)
        elif 0 <= port <= 1024:
            print("ERROR: Le port spécifié est un port privilégié. Spécifiez un port au dessus de 1024.")
            sys.exit(2)

# Validation du port
args = parse_arguments()
validate_port(args.port)

# Utilisation du port par défaut si -p n'est pas spécifié
port = args.port if args.port is not None else 13337

host = ''  # Laisse l'IP vide pour écouter sur toutes les interfaces
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)

while True:
    try:
        conn, addr = s.accept()
        print("Un client vient de se connecter et son IP est", addr)
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
    conn.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
