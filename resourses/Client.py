import os
from threading import Thread
from resourses.Socket import Socket


class Client(Socket):

    def __listen_server(self):
        connected = True

        while connected:
            received_message = self.connection.recv(self.packet_size).decode('utf-8')
            if received_message:
                print(received_message)
            else:
                print("Server is not available!")
                connected = False

    def __connect(self):
        connected = False
        os.system("cls" if os.name == "nt" else "clear")

        while not connected:
            try:
                server = input("Enter server (press Enter to use default): ") or self.host
                port = int(input("Enter port (press Enter to use default): ") or self.port)
                self.connection.connect((server, port))
                connected = True
            except Exception as e:
                print(f"Not able to connect. Please try again. {e}")

        listen_thread = Thread(target=self.__listen_server, daemon=True)
        listen_thread.start()

    def run(self):
        self.__connect()
        shutdown = False

        while not shutdown:
            try:
                send_message = input("")
                print('\033[F\033[K', end="")  # clear last line with entered message
                self.connection.send(send_message.encode('utf-8'))
            except KeyboardInterrupt:
                shutdown = True
            except BrokenPipeError:
                shutdown = True
                print("Server is not available!")

        self.connection.close()
