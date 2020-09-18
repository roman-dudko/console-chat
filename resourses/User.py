class User:

    def __init__(self, sock, address, nickname):
        self.sock = sock
        self.address = address
        self.nickname = nickname

    def post_message(self, message):
        self.sock.send(message.encode("utf-8"))

    def get_message(self, packet_size):
        return self.sock.recv(packet_size).decode("utf-8")
