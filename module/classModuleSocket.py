import socket
from select import select
from PyQt5.QtCore import QThread, pyqtSignal


class Server(QThread):
    socketsignal = pyqtSignal(str)

    def __init__(self, ip, port=1802):
        QThread.__init__(self)
        self.reads = ("registers", "registered", "commands", "chat", "getparams")
        self.to_monitor = []
        self.sock_client = []

        self.admin = {'login': 'admin', 'passw': 'admin'}

        self.server = self.server_init(ip, port)

        self.to_monitor.append(self.server)
        self.runs = True

    def server_init(self, ip, port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((ip, port))
        server_socket.listen()
        return server_socket

    def accept_connection(self, server_socket):
        client_socket, addr = server_socket.accept()
        self.to_monitor.append(client_socket)
        print("Connected ", addr)

    def read_message(self, client_socket):
        try:
            request = client_socket.recv(4096)
            if request:
                request = request.decode("utf-8")
                self.read_msg(request, client_socket)
            else:
                self.remove_socket(client_socket)

        except OSError:
            self.to_monitor.remove(client_socket)
            self.sock_client.remove(client_socket)

    def remove_socket(self, client_socket):
        client_socket.send(b'')
        self.to_monitor.remove(client_socket)
        client_socket.close()

    def read_msg(self, msg, client_socket):
        msg = msg.split('$')
        request = msg.pop()
        if request == self.reads[1] and client_socket in self.sock_client:
            self.parse_string(msg, client_socket)
        else:
            if request == self.reads[0] and client_socket not in self.sock_client:
                self.register_client(msg, client_socket)
            else:

                self.remove_socket(client_socket)
                print('пытаются взломать')

    def register_client(self, msg, client_socket):
        admin, passw = msg
        if admin == self.admin.get('login') and passw == self.admin.get("passw"):
            self.sock_client.append(client_socket)
            client_socket.send(self.reads[1].encode())
            print("Логин прошел")
        else:
            print("Не прошел")
            self.remove_socket(client_socket)

    def parse_string(self, msg, client_socket):
        request = msg.pop()
        if request == self.reads[2]:
            self.command_request(msg)
        elif request == self.reads[3]:
            self.send_chat(msg, client_socket)

    def send_chat(self, msg, client_socket):
        for sock in self.sock_client:
            print('Chats')
            if sock != client_socket:
                sock.send(msg.pop().encode())

    def check_msg(self, msg):
        msg = msg.split('$')
        print(len(msg))
        if len(msg) >= 5:
            print(msg)
            reg, login, passw = msg[0], msg[2], msg[4]
            print(reg, login, passw)

    def run(self):
        while self.runs:
            try:
                ready_to_read, _, _ = select(self.to_monitor, [], [])  # read, write, errors
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(e)

            for sock in ready_to_read:
                if sock is self.server:
                    self.accept_connection(sock)
                else:
                    self.read_message(sock)

    def command_request(self, msg):
        self.command(msg.pop())

    def command(self, command):
        commands = (
            "keyForward", "keyBackward", "keyStop", "keyHome", "keyStartTimer", "keySpeedUp", "keySpeedDown",
            "keyRevers",
            "keyStart")
        if command in commands:
            print("Команда : {}".format(command))
            self.socketsignal.emit(command)
        else:
            print("Такой команды нет")


if __name__ == '__main__':
    sock = Server('localhost')
    sock.run()
