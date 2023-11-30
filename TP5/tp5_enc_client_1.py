import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('10.2.2.3', 13337))

# Récupération d'une string utilisateur
calc = input("Calcul à envoyer: ")

if not (calc.count('+') == 1 and calc.count('-') <= 1 and calc.count('*') <= 1):
    raise TypeError("Veuillez saisir un seul opérateur (+, - ou *) dans le calcul.")

nums = calc.split(" ")

if not all(num.lstrip('-').isdigit() for num in nums):
    raise TypeError("Veuillez saisir des nombres entiers.")

if int(nums[0]) >= 4294967295 or int(nums[2]) >= 4294967295:
    print("Les nombres saisis doivent être inférieurs à 4294967295")
    exit(0)
    
n1, op, n2 = nums[0], nums[1], nums[2]

n1_len, op_len, n2_len = len(n1), len(op), len(n2)

header = n1_len.to_bytes(4, byteorder='big') + n2_len.to_bytes(4, byteorder='big') + op_len.to_bytes(4, byteorder='big')

seq = header + calc.replace(" ", "").encode()
print(seq)

# On envoie
s.send(seq)

# Réception et affichage du résultat
s_data = s.recv(1024)
print(s_data.decode())
s.close()
exit(0)
