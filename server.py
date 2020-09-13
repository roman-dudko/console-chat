import socket
from threading import Thread
import time

host = socket.gethostbyname(socket.gethostname())
port = 7777

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
print(f"Listening for connections at {host}:{port}...")

clients = []
nicknames = []
server_shutdown = False


def broadcast(message):
    """Send message to all connected users"""
    for client in clients:
        client.send(message)


def listen_client(client, nickname):
    """Handle client messages, process commands, broadcast messages"""
    connected = True
    while connected:
        message = client.recv(1024)

        if message.decode('utf-8') == f"{nickname} exited from server":
            nicknames.remove(nickname)
            clients.remove(client)
            print(message.decode('utf-8'))
            connected = False
        time_now = time.strftime("%H.%M.%S", time.localtime())
        message_formatted = f"[{time_now}] {message.decode('utf-8')}"
        print(message_formatted)
        broadcast(message_formatted.encode('utf-8'))


if __name__ == '__main__':
    while not server_shutdown:
        try:
            client, address = server.accept()
            nickname = client.recv(1024).decode('utf-8')
            time_now = time.strftime("%H.%M.%S", time.localtime())
            print(f"[{time_now}] Accepted new connection from {address}, username: {nickname} ")
            nicknames.append(nickname)
            clients.append(client)
            client.send('Welcome to server!'.encode('utf-8'))
            thread = Thread(target=listen_client, args=(client, nickname,), daemon=True)
            thread.start()
        except KeyboardInterrupt:
            server_shutdown = True
            print('Server shut down!')
            broadcast('Server shut down!'.encode('utf-8'))
