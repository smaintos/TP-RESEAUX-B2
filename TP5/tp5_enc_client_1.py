import socket
import struct

def send_expression(sock, expression):
    # Encode l'expression en UTF-8
    encoded_expression = expression.encode('utf-8')

    # Calcule la taille de l'expression en octets
    expression_len = len(encoded_expression)

    # Crée l'en-tête avec la taille de l'expression
    header = struct.pack("!I", expression_len)

    # Envoie l'en-tête et l'expression
    sock.send(header + encoded_expression)

    # Envoie une séquence de fin (0)
    sock.send(b'\x00')

# Connexion au serveur
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('172.16.40.8', 13337))
s.send('Hello'.encode())

# On reçoit la string Hello
data = s.recv(1024)

# Récupération de l'expression arithmétique de l'utilisateur
expression = input("Expression arithmétique à envoyer: ")

# Envoie l'expression au serveur
send_expression(s, expression)

# Réception et affichage du résultat
s_data = s.recv(1024)
print(s_data.decode())

# Fermeture de la connexion
s.close()
