import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('172.16.40.8', 13337))
s.send('Hello'.encode())

# On reçoit la string Hello
data = s.recv(1024)

# Récupération d'une string utilisateur
msg = input("Calcul à envoyer: ")


# on encode le message explicitement en UTF-8 pour récup un tableau de bytes
encoded_msg = msg.encode('utf-8')

# on calcule sa taille, en nombre d'octets
msg_len = len(encoded_msg)

# on encode ce nombre d'octets sur une taille fixe de 4 octets
header = msg_len.to_bytes(4, byteorder='big')

# on peut concaténer ce header avec le message, avant d'envoyer sur le réseau
payload = header + encoded_msg


# On envoie
s.send(payload)

# Réception et affichage du résultat
s_data = s.recv(payload)
print(s_data.decode())
s.close()
