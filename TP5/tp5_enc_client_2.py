import socket
from re import compile
from math import ceil

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('10.2.2.3', 13337))

# Récupération d'une string utilisateur
calc = input("Calcul à envoyer: ")

calc_pattern = compile('^(\+)?([0-9]){1,10} (\+|-|\*) (\+)?([0-9]){1,10}$')

if not calc_pattern.match(calc):
    raise TypeError("Veuillez saisir un calcul valide (addition, soustraction ou multiplication) : choisir des nombres entiers compris entre 0 et 4294967294")

nums = calc.split(" ")

if int(nums[0]) >= 4294967295 or int(nums[2]) >= 4294967295:
    print("Les nombres saisis doivent être compris entre 0 et 4294967294")
    exit(0)
    
n1, op, n2 = int(nums[0]), nums[1], int(nums[2])

n1_len, n2_len = ceil(n1.bit_length()/8.0), ceil(n2.bit_length()/8.0)
print(n1_len, n2_len)

if n1 == 0:
    n1_len = 1
if n2 == 0:
    n2_len = 1

op = nums[1]

if op == "+":
    op = 0
elif op == "-":
    op = 1
else:
    op = 2

hdr = n1_len.to_bytes(4, byteorder='big') + n2_len.to_bytes(4, byteorder='big')

byte_calculation = n1.to_bytes(n1_len, byteorder='big') + op.to_bytes(1, byteorder='big') + n2.to_bytes(n2_len, byteorder='big')

seq = hdr + byte_calculation

# On envoie
s.send(seq)

# Réception et affichage du résultat
res_byte_len = int.from_bytes(s.recv(4), byteorder='big')

is_negative = True if int.from_bytes(s.recv(1), byteorder='big') == 1 else False

res = int.from_bytes(s.recv(res_byte_len), byteorder='big')
if is_negative:
    res = -abs(res)

print(f"Le résultat du calcul {calc} est : {res}")

s.close()
exit(0)
