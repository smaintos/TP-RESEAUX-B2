import socket
from re import compile
from math import ceil

def sendcalc(socket, calculation):
    # Validation de la saisie utilisateur
    calcpattern = compile('^(\+)?([0-9]){1,10} (\+|-|\*) (\+)?([0-9]){1,10}$')

    if not calcpattern.match(calculation):
        raise TypeError("Veuillez saisir un calcul valide (addition, soustraction ou multiplication) : choisir des nombres entiers compris entre 0 et 4294967294")

    array = calculation.split(" ")

    if int(array[0]) >= 4294967295 or int(array[2]) >= 4294967295:
        print("Les nombres saisis doivent être compris entre 0 et 4294967294")
        exit(0)

    first_nb, operand, second_nb = int(array[0]), array[1], int(array[2])

    first_nb_len, second_nb_len = ceil(first_nb.bit_length() / 8.0), ceil(second_nb.bit_length() / 8.0)

    if first_nb == 0:
        first_nb_len = 1
    if second_nb == 0:
        second_nb_len = 1

    operand = array[1]

    if operand == "+":
        operand = 0
    elif operand == "-":
        operand = 1
    else:
        operand = 2

    header = first_nb_len.to_bytes(4, byteorder='big') + second_nb_len.to_bytes(4, byteorder='big')

    byte_calculation = first_nb.to_bytes(first_nb_len, byteorder='big') + operand.to_bytes(1, byteorder='big') + second_nb.to_bytes(second_nb_len, byteorder='big')

    sequence = header + byte_calculation

    # On envoie
    socket.send(sequence)

def sendresult(socket):
    # Réception et affichage du résultat
    res_byte_len = int.from_bytes(socket.recv(4), byteorder='big')

    is_negative = int.from_bytes(socket.recv(1), byteorder='big') == 1

    res = int.from_bytes(socket.recv(res_byte_len), byteorder='big')

    if is_negative:
        res = -abs(res)

    return res

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('10.2.2.3', 13337))

    # Récupération d'une string utilisateur
    calculation = input("Calcul à envoyer: ")

    sendcalc(s, calculation)

    result = sendresult(s)

    print(f"Le résultat du calcul {calculation} est : {result}")

    s.close()
    exit(0)

if __name__ == "__main__":
    main()
