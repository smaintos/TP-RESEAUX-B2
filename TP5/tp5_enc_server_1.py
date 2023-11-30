import socket

port = 13337
ip_addr = '10.2.2.3'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ip_addr, port))

print(f"Serveur démarré sur le port {port}")

s.listen(1)

while True:
    
    conn, addr = s.accept()
    
    print(f"Client {addr[0]} connecté")

    try:
        # On reçoit le calcul du client
        n1_len = int.from_bytes(conn.recv(4), byteorder='big')
        if not n1_len:
            continue
        n2_len = int.from_bytes(conn.recv(4), byteorder='big')
        op_len = int.from_bytes(conn.recv(4), byteorder='big')

        calc = f"{conn.recv(n1_len).decode()} {conn.recv(op_len).decode()} {conn.recv(n2_len).decode()}"
        
        # Évaluation et envoi du résultat
        result = eval(calc)
        conn.send(str(result).encode())
         
    except socket.error:
        print("Une erreur s'est produite.")
        break

conn.close()
