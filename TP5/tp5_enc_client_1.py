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

def main():
    host = "172.16.40.8"
    port = 13337

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:
        expression = input("Entrez une expression arithmétique simple (ex. 3 + 3): ")

        if is_valid_expression(expression):
            # Envoyer l'expression au serveur
            client_socket.send(expression.encode())
        else:
            print("Expression invalide. Veuillez entrer une expression arithmétique simple.")

    client_socket.close()

if __name__ == "__main__":
    main()
