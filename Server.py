import socket
from User import User
from threading import Thread


class Server:
    packet_size = 1024
    users = []

    def __init__(self, port):
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def broadcast(self, message):
        print(message.decode('utf-8'))
        for user in self.users:
            user.post_message(message)

    def cmd_whois(self):
        return str([u.nickname for u in self.users])


    def listen_user(self, user):
        connected = True
        while connected:
            message = user.sock.recv(self.packet_size)
            # If Command
            command = message.decode('utf-8').split(':')[1]
            if command.startswith(' /'):
                cmd = 'cmd_' + command[2:]
                if hasattr(self, cmd):
                    cmd = getattr(self,cmd)
                    user.post_message(cmd().encode('utf-8'))
                else:
                    self.broadcast('Unknown сommand')
                continue
            if message:
                self.broadcast(message)
            else:
                self.users.remove(user)
                self.broadcast(f"{user.nickname} exited from server".encode('utf-8'))
                connected = False

    def accept_connections(self):
        server_shutdown = False
        while not server_shutdown:
            try:
                sock, address = self.server.accept()
                accepted = False
                while not accepted:
                    data = sock.recv(self.packet_size).decode('utf-8')
                    if any(user.nickname == data for user in self.users):
                        sock.send("This name is not available!".encode('utf-8'))
                    else:
                        nickname = data
                        accepted = True
                user = User(sock, address, nickname)
                self.users.append(user)
                thread = Thread(target=self.listen_user, args=(user,), daemon=True)
                thread.start()
            except KeyboardInterrupt:
                server_shutdown = True
                self.broadcast('Server shut down!'.encode('utf-8'))

    def run(self):
        self.server.bind((self.host, self.port))
        self.server.listen()
        print(f"Listening for connections at {self.host}:{self.port}...")
        self.accept_connections()
