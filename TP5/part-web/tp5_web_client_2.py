import socket



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('10.2.2.3', 8080))

user_input = input()

s.send(user_input.encode('utf-8'))

print(s.recv(1024).decode('utf-8'))