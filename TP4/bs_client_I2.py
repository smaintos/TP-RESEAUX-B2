import socket
import sys

while True:
    # On définit la destination de la connexion
    host = '172.16.40.8'  # IP du serveur
    port = 13337  # Port choisir par le serveur

    # Création de l'objet socket de type TCP (SOCK_STREAM)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connexion au serveur
        s.connect((host, port))
        # note : la double parenthèse n'est pas une erreur : on envoie un tuple à la fonction connect()

        print(f'Connecté avec succès au serveur {host} sur le port {port}')

        # Envoi de data bidon
        input_data = input("Que veux-tu envoyer au serveur ('exit' pour quitter) : ")

        if input_data.lower() == 'exit':
            break  # Quitter la boucle si l'utilisateur entre 'exit'

        s.sendall(input_data.encode())

        # On reçoit 1024 bytes qui contiennent peut-être une réponse du serveur
        data = s.recv(1024)

        print(repr(data))

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

    finally:
        # On libère le socket TCP
        s.close()
