import socket
import struct

def recv_expression(sock):
    # Lit l'en-tête pour déterminer la taille du message
    header = sock.recv(4)
    expression_len = struct.unpack("!I", header)[0]

    # Lit les octets suivants pour obtenir l'expression
    expression = sock.recv(expression_len)

    # Vérifie la séquence de fin
    end_sequence = sock.recv(1)
    if end_sequence != b'\x00':
        raise ValueError("Séquence de fin incorrecte")

    return expression.decode('utf-8')

# Création de la socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('172.16.40.8', 13337))  
server_socket.listen(1)
conn, addr = server_socket.accept()

while True:
    try:
        # On reçoit la string Hello du client
        data = conn.recv(1024)
        if not data: break
        print(f"Données reçues du client : {data}")

        conn.send("Hello".encode())

        # On reçoit l'expression arithmétique du client
        expression = recv_expression(conn)

        # Affiche la taille du message
        print(f"Taille du message : {len(expression)} octets")

        # Affiche l'expression
        print(f"Expression reçue : {expression}")

        # Evaluation et envoi du résultat
        res = eval(expression)
        conn.send(str(res).encode())
         
    except socket.error:
        print("Error Occured.")
        break

# Fermeture de la connexion
conn.close()
