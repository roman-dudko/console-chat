import socket
import threading
import os

server = input("Enter server (press Enter to use default): ") or "127.0.1.1"
port = int(input("Enter port (press Enter to use default): ") or "7777")
nickname = input("Enter nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.1.1', 7777))
os.system('cls' if os.name == 'nt' else 'clear')


def listen_server():
    client.send(nickname.encode('utf-8'))
    while True:
        message = client.recv(1024).decode('utf-8')
        print(message)


def send_msg():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        print('\033[F\033[K', end="")  # clear last line with entered message
        client.send(message.encode('utf-8'))


listen_thread = threading.Thread(target=listen_server)
listen_thread.start()

send_thread = threading.Thread(target=send_msg)
send_thread.start()
