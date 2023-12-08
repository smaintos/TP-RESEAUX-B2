import socket

def main():
    server_address = ('10.33.76.197', 8888)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(server_address)
        print(f"Connecté au serveur {server_address}")

        message = "Hello"
        client_socket.sendall(message.encode())

        data = client_socket.recv(1024)
        response = data.decode()

        print(f"Réponse du serveur : {response}")

if __name__ == "__main__":
    main()
