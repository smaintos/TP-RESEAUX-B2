import socket
import sys
import signal

# On choisit une IP et un port où on va écouter
host = '172.16.40.8' # string vide signifie, dans ce conetxte, toutes les IPs de la machine
port = 13337 # port choisi arbitrairement

# On crée un objet socket
# SOCK_STREAM c'est pour créer un socket TCP (pas UDP donc)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# On demande à notre programme de se bind sur notre port
s.bind((host, port))  

# Place le programme en mode écoute derrière le port auquel il s'est bind
s.listen(1)


# Petite boucle infinie (bah oui c'est un serveur)
# A chaque itération la boucle reçoit des données et les traite
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
        print("Error Occured.")
        break

def signal_handler(sig, frame):
    conn.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)