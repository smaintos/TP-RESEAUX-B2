import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('172.16.40.8', 13337))
s.listen(1)
conn, addr = s.accept()

while True:
    try:
        # On reçoit le calcul du client
        data = conn.recv(1024)
        if not data:
            break
        print(f"Calcul reçu du client : {data.decode()}")

        # Evaluation et envoi du résultat
        res = eval(data.decode())
        conn.send(str(res).encode())
    except socket.error:
        print("Error Occurred.")
        break

conn.close()
