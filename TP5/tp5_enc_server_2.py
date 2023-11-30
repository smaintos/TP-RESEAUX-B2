import socket
from math import ceil

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
        
        n1 = int.from_bytes(conn.recv(n1_len), byteorder='big')
        op = int.from_bytes(conn.recv(1), byteorder='big')
        n2 = int.from_bytes(conn.recv(n2_len), byteorder='big')
        
        if op == 0:
            op = "+"
        elif op == 1:
            op = "-"
        else:
            op = "*"

        calc = f"{n1} {op} {n2}"
        
        # Évaluation et envoi du résultat
        result: int = eval(calc)
        
        res_byte_len = ceil(result.bit_length()/8.0)
        
        hdr = res_byte_len.to_bytes(4, byteorder='big')
        
        if result < 0:
            hdr += int.to_bytes(1, 1, byteorder='big')
            result = abs(result)
        else:
            hdr += int.to_bytes(0, 1, byteorder='big')
        
        seq = hdr + result.to_bytes(res_byte_len, byteorder='big')
        
        conn.send(seq)
         
    except socket.error:
        print("Une erreur s'est produite.")
        break

conn.close()
