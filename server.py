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
packet_size = 1024


def broadcast(message):
    """Send message to all connected users"""
    time_now = time.strftime("%H.%M.%S", time.localtime())
    message_formatted = f"[{time_now}] {message.decode('utf-8')}"
    print(message_formatted)

    for client in clients:
        client.send(message_formatted.encode('utf-8'))


def listen_client(client, nickname):
    """Handle client messages, process commands, broadcast messages"""
    connected = True
    while connected:
        try:
            message = client.recv(packet_size)
            broadcast(message)
        except BrokenPipeError:
            nicknames.remove(nickname)
            clients.remove(client)
            broadcast(f"{nickname} exited from server".encode('utf-8'))
            connected = False


if __name__ == '__main__':
    while not server_shutdown:
        try:
            client, address = server.accept()
            nickname = client.recv(packet_size).decode('utf-8')
            if nickname not in nicknames:
                broadcast(f"Accepted new connection; address: {address}, username: {nickname} ".encode('utf-8'))
                nicknames.append(nickname)
                clients.append(client)
                client.send('Welcome to server!'.encode('utf-8'))
                thread = Thread(target=listen_client, args=(client, nickname,), daemon=True)
                thread.start()
            else:
                client.send('Client with that name is connected already.Disconnecting.'.encode('utf-8'))
        except KeyboardInterrupt:
            server_shutdown = True
            broadcast('Server shut down!'.encode('utf-8'))
