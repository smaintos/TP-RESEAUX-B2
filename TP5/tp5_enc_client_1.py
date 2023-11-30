import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('172.16.40.8', 13337))
s.send('Hello'.encode())

# On reçoit la string Hello
data = s.recv(1024)

# Récupération d'une expression arithmétique de l'utilisateur
expression = input("Entrez une expression arithmétique simple (ex. 3 + 3): ")

# Validation de l'expression
try:
    x, operator, y = map(str.strip, expression.split())
    x = int(x)
    y = int(y)

    if 0 <= x < 4294967295 and 0 <= y < 4294967295:
        # Envoie de l'expression au serveur
        s.send(expression.encode())

        # Réception et affichage du résultat
        s_data = s.recv(1024)
        print(s_data.decode())
    else:
        print("Les nombres doivent être inférieurs à 4294967295.")
except (ValueError, IndexError):
    print("Expression invalide. Veuillez entrer une expression arithmétique simple.")

s.close()
