import socket
from os.path import isfile, exists
import logging

logging.basicConfig(filename='serverlog', level=logging.INFO, format='%(asctime)s - %(message)s')

def check_file(file_name: str) -> bool:
    file_path = f"./contents/{file_name}"
    return exists(file_path) and isfile(file_path)

def read_content(file_name: str):
    file_path = f'./contents/{file_name}'
    with open(file_path, 'r') as file:
        html_content = file.read()
    http_response = 'HTTP/1.0 200 OK\n\n' + html_content
    return http_response

def start_server(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip, port))
    s.listen(1)

    print(f"Serveur démarré sur  http://{ip}:{port}")

    while True:
        conn, addr = s.accept()
        logging.info(f"Client {addr[0]} est connecté")

        try:
            client_request(conn)
        except socket.error:
            print("Error Occurred.")
            break

    s.close()

def client_request(conn):
    request = conn.recv(1024).decode('utf-8')

    if not request:
        return

    method, uri = prequest(request)
    logging.info(f"Donnée du client : {method} {uri}")

    if method == "GET":
        if uri == "/":
            response = "HTTP/1.0 200 OK\n\n<h1>Hello je suis un serveur HTTP</h1>"
            conn.send(response.encode('utf-8'))
            conn.close()
        else:
            file_name = uri[1:]
            http_response = None

            if check_file(file_name):
                http_response = read_content(file_name)
                logging.info(f"Envoie de {file_name} au client")
            else:
                http_response = "HTTP/1.0 404 Not Found\n\n"
                logging.info(f"{file_name} not found, sent 404 response to client")

            conn.send(http_response.encode('utf-8'))
            conn.close()

def prequest(request):
    request_elements = request.split(" ")
    return request_elements[0], request_elements[1]

if __name__ == "__main__":
    start_server('10.2.2.3', 8080)
