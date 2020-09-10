import socket
from threading import Thread

host = socket.gethostbyname(socket.gethostname())
port = 7777

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
print(f"[ Listening for connections on {host}:{port}... ]")

clients = []
nicknames = []


def broadcast(message):
    """Send message to all connected users"""
    for client in clients:
        client.send(message)


def listen_client(client):
    """Handle client messages, process commands, broadcast messages"""
    while True:
        message = client.recv(1024)
        broadcast(message)


def start_server():
    """Handle clients on separate threads"""
    while True:
        client, address = server.accept()
        nickname = client.recv(1024).decode('utf-8')
        print(f"[ Accepted new connection from {address}, username: {nickname} ]")
        nicknames.append(nickname)
        clients.append(client)
        client.send('Welcome to server!'.encode('utf-8'))
        thread = Thread(target=listen_client, args=(client,))
        thread.start()


start_server()
