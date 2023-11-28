import socket
import struct

# Fonction pour envoyer une chaîne en tant qu'entier
def send_string_as_int(sock, data):
    # Convertit la longueur de la chaîne en entier non signé 4 octets
    length = len(data)
    length_pack = struct.pack("!I", length)

    # Envoie la longueur
    sock.send(length_pack)

    # Envoie les données
    sock.send(data.encode())

# Fonction pour recevoir une chaîne en tant qu'entier
def recv_string_as_int(sock):
    # Reçoit la longueur de la chaîne en entier non signé 4 octets
    length_pack = sock.recv(4)
    length = struct.unpack("!I", length_pack)[0]

    # Reçoit les données
    data = sock.recv(length)

    return data.decode()

# Connexion au serveur
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('172.16.40.8', 13337))

# Envoie la première chaîne (Hello)
send_string_as_int(s, 'Hello')

# Reçoit la réponse (string Hello)
data = recv_string_as_int(s)

# Récupération de l'expression arithmétique de l'utilisateur
expression = input("Expression arithmétique à envoyer: ")

# Vérification de la validité de l'expression
# ... (vous devez ajouter votre propre logique de validation ici)

# on encode l'expression explicitement en UTF-8 pour récupérer un tableau de bytes
encoded_expression = expression.encode('utf-8')

# on calcule sa taille, en nombre d'octets
expression_len = len(encoded_expression)

# on encode ce nombre d'octets sur une taille fixe de 4 octets
header = expression_len.to_bytes(4, byteorder='big')

# on peut concaténer ce header avec l'expression, avant d'envoyer sur le réseau
payload = header + encoded_expression

# on peut envoyer ça sur le réseau
s.send(payload)

# Séquence de fin (par exemple, un octet 0)
end_sequence = b'\x00'
s.send(end_sequence)

# Réception et affichage du résultat
s_data = recv_string_as_int(s)
print(s_data)

# Fermeture de la connexion
s.close()
