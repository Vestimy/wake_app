import threading
import socketserver
import time
from PyQt5.QtCore import QThread, pyqtSignal
import socket


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def setup(self):
        if self.server.queue.first_connect(self.request, self.request.recv(1024)):
            self.runs = True
        else:
            self.runs = False

    def handle(self):
        while self.runs:
            if self.server.queue.client_check(self.request):
                data = self.request.recv(1024)
                print(data)
                if data == b'':
                    self.runs = False
                    self.request.close()
                    break
                self.server.queue.add(data)
                self.server.queue.command(self.request, data)
                # self.server.queue.send_msg_chat(self.request, data)
            else:
                try:
                    data = self.request.recv(1024)
                    self.server.queue.send(self.request, data)
                    print(data)
                except:
                    self.runs = False
                    print("Соединение закрыто")


class Queue(QThread):
    socketsignal = pyqtSignal(str)

    def __init__(self, ip, port):
        QThread.__init__(self)
        self.server = ThreadedTCPServer((ip, port), ThreadedTCPRequestHandler)

        self.server.queue = self
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.users = {'Login': 'admin', 'pass': '1234'}
        self.messages = []
        self.client = []
        self.commands = ['keyForward', "keyBackward", "keyStop", "keyHome", "keyStartTimer", "keySpeedUp", "keySpeedUp",
                         "keySpeedDown", "keyRevers", "keyStart"]

    def check_test(self):
        for i in self.client:
            print(i)
            i.send("quit".encode())
            i.close
        self.stop_server()

    def start_server(self):
        self.server_thread.start()
        print("Server loop running in thread:", self.server_thread.name)

    def stop_server(self):
        self.server.shutdown()
        self.server.server_close()

    def add(self, message):
        self.messages.append(message)

    def first_connect(self, client, msg):
        if not client in self.client:
            if self.check_client(msg):
                self.client.append(client)
                return True
            else:
                return False

    def check_client(self, msg):
        print(msg)
        msg = self.decode_msg(msg)
        req, login, passw = msg
        if req == "req":

            if login == self.users.get('Login'):
                if passw == self.users.get('pass'):
                    print("Проверка прошла успешно")
                    return True
            print("ПРоверка не прошла")
            return False
        else:
            if comm == "comm":
                self.command()

    def command(self, client, msg):
        msg = self.decode_msg(msg)
        print(msg)
        msg = msg
        print(msg)
        if len(msg) >= 2:
            req, command = msg
            if req == 'comm':
                if command in self.commands:
                    self.socketsignal.emit(command)
                    self.send(client, command)
        else:
            self.client_exit(client)

    def client_check(self, client):
        if client in self.client:
            return True
        else:
            self.server.runs = False
            return False

    def client_exit(self, client):
        client.send(b'')
        client.close()
        self.client.remove(client)
        print("client remove")

    def decode_msg(self, msg):
        msg = msg.decode('utf8')
        msg = msg.split("$")
        return msg

    def send(self, client, msg):
        for i in self.client:
            if client != i:
                try:
                    i.send('Выполнена команда: {}'.format(msg).encode())
                except Exception as e:

                    print("Клиент удален")
                    i.close()
                    self.client.remove(i)
                    # print("Ошибка")

    def run(self):
        while True:
            try:
                time.sleep(1)
                if self.exists():
                    self.handle(self.get())
            except:
                self.server.runs = False
                self.stop_server()

                self.server.shutdown()
                self.server.server_close()

    def send_msg_chat(self, client, msg):
        for cl in self.client:
            if cl != client:
                try:
                    cl.send(msg)
                except:
                    self.client.remove(cl)

    def view(self):
        return self.messages

    def get(self):
        return self.messages.pop()

    def exists(self):
        return len(self.messages)

    def handle(self, message):
        """
        Prototype
        """
        pass


if __name__ == "__main__":
    app = Queue('', 8889)
    app.start_server()
    app.loop()
    app.stop_server()
