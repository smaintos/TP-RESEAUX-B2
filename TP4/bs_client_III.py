import socket
import sys
import re
import logging
import os

def parse_arguments():
    host = '172.16.40.8'  # IP du serveur par défaut
    port = 13337           # Port choisi par le serveur par défaut

    if len(sys.argv) > 1:
        if sys.argv[1] == '-h' or sys.argv[1] == '--help':
            print("Usage: python script.py [OPTION] [ARGUMENT]\n\n"
                  "\t-h, --help\t\tAffiche l'aide\n"
                  "\t-i, --ip\t\tSpécifie l'adresse IP du serveur\n"
                  "\t-p, --port\t\tSpécifie le port sur lequel le serveur écoute\n")
            sys.exit(0)
        if sys.argv[1] == '-i' or sys.argv[1] == '--ip':
            host = sys.argv[2]
        elif sys.argv[1] == '-p' or sys.argv[1] == '--port':
            port = int(sys.argv[2])

    return host, port

def check_operation(input_data):
    # Vérifie que l'entrée est une chaîne de caractères
    if not isinstance(input_data, str):
        return False

    # Vérifie que la chaîne correspond à une opération d'addition, soustraction ou multiplication
    if not re.match(r'^-?\d+\s*[\+\-\*]\s*-?\d+$', input_data):
        return False

    # Vérifie que les nombres dans l'opération sont entre -100000 et +100000
    numbers = re.findall(r'-?\d+', input_data)
    for num in numbers:
        if not (-100000 <= int(num) <= 100000):
            return False

    return True

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Emplacement du fichier de log du client
log_folder = '/var/log/bs_client/'

if not os.path.exists(log_folder):
    os.makedirs(log_folder)

log_file_path = os.path.join(log_folder, 'bs_client.log')

# Configuration du gestionnaire de fichiers pour les logs du client
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
logging.getLogger('').addHandler(file_handler)

# On définit la destination de la connexion
host, port = parse_arguments()

# Création de l'objet socket de type TCP (SOCK_STREAM)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connexion au serveur
    s.connect((host, port))
    # note : la double parenthèse n'est pas une erreur : on envoie un tuple à la fonction connect()

    logging.info(f"Connexion réussie à {host}:{port}.")

    # Demande au client de saisir une opération arithmétique
    input_data = input("C'est quoi ton calcul hun ? : ")

    # Vérification de l'expression arithmétique
    if not check_operation(input_data):
        raise ValueError("Erreur : Opération non valide. Saisissez une opération d'addition, soustraction ou multiplication "
                         "avec des nombres entiers entre -100000 et +100000.")

    s.sendall(input_data.encode())
    logging.info(f"Message envoyé au serveur {host}:{port} : {input_data}")

    # On reçoit 1024 bytes qui contiennent peut-être une réponse du serveur
    data = s.recv(1024)
    logging.info(f"Réponse reçue du serveur {host}:{port} : {repr(data)}")

except Exception as e:
    logging.error(f"Erreur : {e}")

finally:
    # On libère le socket TCP
    s.close()

# Sortie du script
sys.exit(0)
