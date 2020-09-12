import socket
from threading import Thread
import time

host = socket.gethostbyname(socket.gethostname())
port = 7777

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
print(f"Listening for connections on {host}:{port}...")

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
        if message:
            time_now = time.strftime("%H.%M.%S", time.localtime())
            message_formatted = f"[{time_now}] {message.decode('utf-8')}"
            print(message_formatted)
            broadcast(message_formatted.encode('utf-8'))


def start_server():
    """Handle clients on separate threads"""
    while True:
        client, address = server.accept()
        nickname = client.recv(1024).decode('utf-8')
        time_now = time.strftime("%H.%M.%S", time.localtime())
        print(f"[{time_now}] Accepted new connection from {address}, username: {nickname} ")
        nicknames.append(nickname)
        clients.append(client)
        client.send('Welcome to server!'.encode('utf-8'))
        thread = Thread(target=listen_client, args=(client,))
        thread.start()


start_server()
