import logging
from threading import Thread
from resourses.Socket import Socket
from resourses.User import User
from resourses.CommandsHandler import CommandsHandler


class Server(Socket):
    users: list = []
    logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO)

    def _broadcast(self, message):
        logging.info(message)
        for user in self.users:
            user.post_message(message)

    def _listen_user(self, user):
        try:

            while True:
                message = user.get_message(self.packet_size)
                if message.startswith('/'):
                    try:
                        getattr(CommandsHandler, message[1:])(user=user, obj=self)
                    except AttributeError:
                        user.post_message("Incorrect command")
                elif message:
                    self._broadcast(f"{user.nickname}: {message}")
                else:
                    raise BrokenPipeError("Connection lost")

        except BrokenPipeError:
            user.sock.close()
            self.users.remove(user)
            self._broadcast(f"{user.nickname} exited from server")

    def _accept_connections(self):
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
                        self._broadcast(f"{nick} connected to the server!")
                        sock.send(f"{nick}! Welcome to the server! Type /help to see commands".encode("utf-8"))
                        accepted = True

                user = User(sock, address, nick)
                self.users.append(user)
                thread = Thread(target=self._listen_user, args=(user,), daemon=True)
                thread.start()
            except KeyboardInterrupt:
                server_shutdown = True
                self._broadcast("Server shut down!")
                for user in self.users:
                    user.sock.close()
                self.connection.close()

    def run(self):
        started = False

        while not started:
            try:
                port = int(input("Enter port (press Enter to use default): ") or self.port)
                self.connection.bind((self.host, port))
                self.port = port
                started = True
            except PermissionError:
                logging.error("This port is already reserved.")
            except OverflowError:
                logging.error("Out of range. Port must be 0-65535.")

        self.connection.listen()
        logging.info(f"Listening for connections at {self.host}:{self.port}...")
        self._accept_connections()
