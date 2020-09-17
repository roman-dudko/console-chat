import random
from resourses.Socket import Socket
from threading import Thread
from resourses.User import User


class Server(Socket):
    users = []

    def __handle_commands(self, user, message):
        if message == "/help":
            user.post_message("List of available commands:\n"
                              "/whois - show list of online users\n"
                              "/count - dhow number of online users\n"
                              "/play - 'paper-rock-scissors game'".encode("utf-8"))
        if message == "/whois":
            user.post_message(f"Online users: {str([u.nickname for u in self.users])}".encode("utf-8"))
        elif message == "/count":
            user.post_message(f"Current online: {len(self.users)} users".encode("utf-8"))
        elif message == "/play":
            user.post_message(f"Let's play! To stop the game type 'stop'.".encode("utf-8"))
            option = ["scissors", "paper", "rock"]

            while True:
                user.post_message(f"\nPlease enter your choice: 'scissors', 'paper' or 'rock':".encode("utf-8"))
                user_select = user.get_message(self.packet_size).decode("utf-8")
                if user_select in ("scissors", "paper", "rock"):
                    pc_select = random.choice(option)
                    if pc_select == user_select:
                        user.post_message(f"We both select {pc_select}. Let's try again!".encode("utf-8"))
                    elif option[option.index(user_select) - 1] != pc_select:
                        user.post_message(f"Your {user_select} vs my {pc_select}. "
                                          f"You win! One more time?".encode("utf-8"))
                    else:
                        user.post_message(f"Your {user_select} vs my {pc_select}. "
                                          f"You lose! Better luck next time!".encode("utf-8"))
                elif user_select == "stop":
                    user.post_message(f"Well played! Have a good day!".encode("utf-8"))
                else:
                    user.post_message(f"Incorrect choice. You can stop game by typing 'stop'.\n".encode("utf-8"))
        else:
            user.post_message(f"Incorrect command".encode("utf-8"))

    def __broadcast(self, message):
        print(message.decode("utf-8"))
        for user in self.users:
            user.post_message(message)

    def __listen_user(self, user):
        connected = True

        while connected:
            message = user.get_message(self.packet_size).decode("utf-8")
            if message.startswith('/'):
                self.__handle_commands(user, message)
            elif message:
                self.__broadcast(f"{user.nickname}: {message}".encode("utf-8"))
            else:
                self.users.remove(user)
                self.__broadcast(f"{user.nickname} exited from server".encode("utf-8"))
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
                        self.__broadcast(f"{nick} connected to the server!".encode("utf-8"))
                        sock.send(f"{nick}! Welcome to the server! Type /help to see list of commands".encode("utf-8"))
                        accepted = True

                user = User(sock, address, nick)
                self.users.append(user)
                thread = Thread(target=self.__listen_user, args=(user,), daemon=True)
                thread.start()
            except KeyboardInterrupt:
                server_shutdown = True
                self.__broadcast("Server shut down!".encode("utf-8"))

    def run(self):
        started = False

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
