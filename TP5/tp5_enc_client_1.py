import socket
from re import compile

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('10.2.2.3', 13337))

# Récupération d'une string utilisateur
calc = input("Calcul à envoyer: ")

calc_pattern = compile('^(\+|-)?([0-9]){1,10} (\+|-|\*) (\+|-)?([0-9]){1,10}$')

if not calc_pattern.match(calc):
    raise TypeError("Veuillez saisir un calcul valide (addition, soustraction ou multiplication) : choisir des nombres entiers compris inférieurs à 4294967295")

nums = calc.split(" ")

if int(nums[0]) >= 4294967295 or int(nums[2]) >= 4294967295:
    print("Les nombres saisis doivent être inférieurs à 4294967295")
    exit(0)
    
n1, op, n2 = nums[0], nums[1], nums[2]

n1_len, op_len, n2_len = len(n1), len(op), len(n2)

hdr = n1_len.to_bytes(4, byteorder='big') + n2_len.to_bytes(4, byteorder='big') + op_len.to_bytes(4, byteorder='big')

seq = hdr + calc.replace(" ", "").encode()
print(seq)

# On envoie
s.send(seq)

# Réception et affichage du résultat
s_data = s.recv(1024)
print(s_data.decode())
s.close()
exit(0)
