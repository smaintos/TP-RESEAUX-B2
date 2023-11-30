import socket
from math import ceil

def hitcalc(socket):
    # On reçoit le calcul du client
    first_nb_len = int.from_bytes(socket.recv(4), byteorder='big')

    if not first_nb_len:
        return None

    second_nb_len = int.from_bytes(socket.recv(4), byteorder='big')

    first_nb = int.from_bytes(socket.recv(first_nb_len), byteorder='big')
    operand = int.from_bytes(socket.recv(1), byteorder='big')
    second_nb = int.from_bytes(socket.recv(second_nb_len), byteorder='big')

    if operand == 0:
        operand = "+"
    elif operand == 1:
        operand = "-"
    else:
        operand = "*"

    calculation = f"{first_nb} {operand} {second_nb}"
    return calculation

def hitresult(socket, result):
    # Envoie du résultat au client
    res_byte_len = ceil(result.bit_length() / 8.0)

    header = res_byte_len.to_bytes(4, byteorder='big')

    if result < 0:
        header += int.to_bytes(1, 1, byteorder='big')
        result = abs(result)
    else:
        header += int.to_bytes(0, 1, byteorder='big')

    sequence = header + result.to_bytes(res_byte_len, byteorder='big')

    socket.send(sequence)

def main():
    port = 13337
    ip_addr = '10.2.2.3'

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip_addr, port))

    print(f"Server started at port {port}")

    s.listen(1)

    while True:
        conn, addr = s.accept()
        print(f"Client {addr[0]} is connected")

        try:
            calculation = hitcalc(conn)

            if calculation is None:
                continue

            print(f"Calculation received from client: {calculation}")

            # Evaluation et envoi du résultat
            result = eval(calculation)
            hitresult(conn, result)

        except socket.error:
            print("Error Occurred.")
            break

    conn.close()

if __name__ == "__main__":
    main()
