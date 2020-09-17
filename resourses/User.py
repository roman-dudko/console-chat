class User:

    def __init__(self, sock, address, nickname):
        self.sock = sock
        self.address = address
        self.nickname = nickname
        self.connected = True
        self.pc_select = ''

    def post_message(self, message):
        self.sock.send(message)

    def get_message(self, packet_size):
        return self.sock.recv(packet_size)
