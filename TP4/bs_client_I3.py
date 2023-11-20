import socket
import sys

# On définit la destination de la connexion
host = '172.16.40.8'  # IP du serveur
port = 13337               # Port choisir par le serveur

# Création de l'objet socket de type TCP (SOCK_STREAM)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connexion au serveur
s.connect((host, port))
# note : la double parenthèse n'est pas une erreur : on envoie un tuple à la fonction connect()

print(f'Connecté avec succès au serveur {host} sur le port {port}')

# Envoi de data bidon
input_data = input("Que veut tu envoyé au serveur : ")
if type(input_data) is str & input_data == "waf" | input_data == "meo":
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