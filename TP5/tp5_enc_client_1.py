import socket

def is_valid_expression(expr):
    # Vérifie si l'expression est une opération arithmétique simple
    valid_operators = ['+', '-', '*']
    parts = expr.split()

    if len(parts) != 3:
        return False

    try:
        x = int(parts[0])
        y = int(parts[2])
    except ValueError:
        return False

    if parts[1] not in valid_operators:
        return False

    return True

def send_with_header(sock, message):
    # Envoie un message avec un en-tête annonçant la taille du message
    message_size = len(message)
    header = str(message_size).encode()
    sock.sendall(header + message.encode() + '<clafin>'.encode())


def main():
    host = "172.16.40.8"  # Remplace avec l'adresse IP du serveur
    port = 13337

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:
        expression = input("Entrez une expression arithmétique simple (ex. 3 + 3): ")

        if is_valid_expression(expression):
            # Envoyer l'expression au serveur avec un en-tête de taille
            send_with_header(client_socket, expression)

            # Recevoir et imprimer la réponse du serveur
            response = client_socket.recv(1024)
            print(f"Réponse du serveur : {response.decode()}")
        else:
            print("Expression invalide. Veuillez entrer une expression arithmétique simple.")

    client_socket.close()

if __name__ == "__main__":
    main()
