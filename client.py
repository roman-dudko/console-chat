import socket
import os
from threading import Thread

server = input("Enter server (press Enter to use default): ") or "127.0.1.1"
port = int(input("Enter port (press Enter to use default): ") or "7777")
nickname = input("Enter nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server, port))
os.system('cls' if os.name == 'nt' else 'clear')

shutdown = False


def listen_server():
    client.send(nickname.encode('utf-8'))
    while True:
        received_message = client.recv(1024).decode('utf-8')
        if received_message:
            print(received_message)


if __name__ == '__main__':
    listen_thread = Thread(target=listen_server, daemon=True)
    listen_thread.start()

    while not shutdown:
        try:
            send_message = '{}: {}'.format(nickname, input(''))
            print('\033[F\033[K', end="")  # clear last line with entered message
            client.send(send_message.encode('utf-8'))
        except KeyboardInterrupt:
            shutdown = True
            client.send(f"{nickname} exited from server".encode('utf-8'))
        except BrokenPipeError:
            shutdown = True
            print("Server is not available!")

    client.close()
