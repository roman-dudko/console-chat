from resourses.Socket import Socket
from threading import Thread
from resourses.User import User
from resourses.CommandsHandler import CommandsHandler


class Server(Socket):
    users = []

    def handle_commands(self, command, user):
        command = 'cmd_' + command[1:]
        if hasattr(self.cmdHandler, command):
            return getattr(self.cmdHandler, command)(user)
        else:
            return "\nincorrect command"

    def __broadcast(self, message):
        print(message)
        for user in self.users:
            user.post_message(message)

    def __listen_user(self, user):
        connected = True

        while connected:
            message = user.get_message(self.packet_size).decode("utf-8")
            if message.startswith('/'):
                user.post_message(message)
                response = self.handle_commands(message, user)
                user.post_message(response)
            elif message:
                self.__broadcast(f"{user.nickname}: {message}")
            else:
                self.users.remove(user)
                self.__broadcast(f"{user.nickname} exited from server")
                connected = False

    def __accept_connections(self):
        server_shutdown = False

        while not server_shutdown:
            try:
                sock, address = self.connection.accept()
                accepted = False
                nick = None
                sock.send("Connected. please select nickname:".encode("utf-8"))
                while not accepted:
                    nick = sock.recv(self.packet_size).decode("utf-8")
                    if any(user.nickname == nick for user in self.users):
                        sock.send("This name is not available! Please enter another one:".encode("utf-8"))
                    else:
                        self.__broadcast(f"{nick} connected to the server!")
                        sock.send(f"{nick}! Welcome to the server!".encode("utf-8"))
                        accepted = True

                user = User(sock, address, nick)
                self.users.append(user)
                thread = Thread(target=self.__listen_user, args=(user,), daemon=True)
                thread.start()
            except KeyboardInterrupt:
                server_shutdown = True
                self.__broadcast("Server shut down!")

    def run(self):
        started = False
        self.cmdHandler = CommandsHandler(self)
        while not started:
            try:
                port = int(input("Enter port (press Enter to use default): ") or self.port)
                self.connection.bind((self.host, port))
                self.port = port
                started = True
            except Exception as e:
                print(f"Please select another port. {e}")

        self.connection.listen()
        print(f"Listening for connections at {self.host}:{self.port}...")
        self.__accept_connections()
