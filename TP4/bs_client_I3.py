import socket
import sys
import re

# On définit la destination de la connexion
host = '172.16.40.8'  # IP du serveur
port = 13337               # Port choisi par le serveur

# Création de l'objet socket de type TCP (SOCK_STREAM)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connexion au serveur
s.connect((host, port))
# note : la double parenthèse n'est pas une erreur : on envoie un tuple à la fonction connect()

print(f'Connecté avec succès au serveur {host} sur le port {port}')

# Envoi de data bidon
input_data = input("Que veut tu envoyer au serveur : ")

# Vérifier que l'entrée est une chaîne de caractères
if not isinstance(input_data, str):
    raise TypeError("Erreur : envoie du texte t'abuse ")

# Vérifier que la chaîne contient soit "waf" soit "meo"
if not re.match(r'^(waf|meo)$', input_data):
    raise ValueError("Erreur : nannnnnnnn bro soit waf soit meo")

try:
    s.sendall(input_data.encode())
except Exception as e:
    print("Erreur lors de l'envoi des données")
    print(e)

# On reçoit 1024 bytes qui contiennent peut-être une réponse du serveur
data = s.recv(1024)

# On libère le socket TCP
s.close()

print(repr(data))

sys.exit(0)