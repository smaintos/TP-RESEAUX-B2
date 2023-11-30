import socket

def receive_with_header(sock):
    # Reçoit un message avec un en-tête annonçant la taille du message
    header = sock.recv(1024)
    message_size = int(header.decode())
    message = sock.recv(message_size).decode()
    return message

def send_with_header(sock, message):
    # Envoie un message avec un en-tête annonçant la taille du message
    message_size = len(message)
    header = str(message_size).encode()
    sock.sendall(header + message.encode() + '<clafin>'.encode())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('172.16.40.8', 13337))
s.listen(1)
conn, addr = s.accept()

while True:
    try:
        # On reçoit le calcul du client avec un en-tête de taille
        data = receive_with_header(conn)
        if not data:
            break
        print(f"Calcul reçu du client : {data}")

        # Evaluation et envoi du résultat
        try:
            res = eval(data)
            send_with_header(conn, str(res))
        except Exception as e:
            print(f"Erreur lors de l'évaluation du calcul : {e}")
            send_with_header(conn, "Erreur")

    except socket.error:
        print("Error Occurred.")
        break

conn.close()
