import socket

def receive_with_header(sock):
    # Reçoit un message avec un en-tête annonçant la taille du message
    header = sock.recv(1024)
    message_size = int(header.decode())
    message = sock.recv(message_size).decode()
    # Reçoit la séquence de fin
    end_sequence = sock.recv(1024).decode()
    if end_sequence != '<clafin>':
        print("Séquence de fin incorrecte.")
        return None
    return message

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('172.16.40.8', 13337))
s.listen(1)
conn, addr = s.accept()

while True:
    try:
        # On reçoit le calcul du client avec un en-tête de taille
        data = receive_with_header(conn)
        if data is None:
            break
        print(f"Calcul reçu du client : {data}")

        # Evaluation et envoi du résultat
        res = eval(data)
        conn.sendall(str(res).encode())
    except socket.error:
        print("Error Occurred.")
        break

conn.close()
