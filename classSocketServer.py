# ----------------------------------------------------
# Program by Andrey Vestimy
#
#
# Version   Date    Info
# 1.0       2020    ----
#
# ----------------------------------------------------

import socket, json
from select import select
from PyQt5.QtCore import QThread, pyqtSignal
from classDb import session
from classModels import Users, Tokens
import rsa


class Server(QThread):
    socketsignal = pyqtSignal(str)
    namesigal = pyqtSignal(str)

    def __init__(self, ip, port=1802):
        QThread.__init__(self)
        self.server = self.server_init(ip, port)
        self.to_monitor = []
        self.sock_client = {}
        self.client_socket = {}
        self.tokens = {}
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
        (pubkey, privkey) = rsa.newkeys(1024)
        if not client_socket in self.client_socket:
            self.rsa_send(client_socket, pubkey, privkey)
        print("Connected ", addr)

    def rsa_send(self, client, pubkey, privkey):
        self.client_socket[client] = (pubkey, privkey)
        client.send(pubkey.save_pkcs1())

    def client_msg(self, client, msg):
        pubkey = rsa.PublicKey.load_pkcs1(self.sock_client.get(client))
        msg = rsa.encrypt(json.dumps(msg).encode(), pubkey)
        client.send(msg)

    def read_message(self, client_socket):
        try:
            request = client_socket.recv(4096)
            if not client_socket in self.sock_client:
                self.sock_client[client_socket] = request
            else:
                if request:
                    try:

                        request = rsa.decrypt(request, self.client_socket.get(client_socket)[1])

                        # print(request)
                        self.work_msg(client_socket, self.json_read_msg(request))
                    except Exception:

                        self.to_monitor.remove(client_socket)

                else:
                    self.to_monitor.remove(client_socket)

        except OSError:
            self.to_monitor.remove(client_socket)

    def json_read_msg(self, data):
        return json.loads(data.decode())

    def json_write_msg(self, data):
        return json.dumps(data)

    def work_msg(self, client, msg):
        if 'access_token' in msg:
            # print(self.tokens[client])
            if msg.get('access_token') == self.tokens[client].get('access_token'):
                self.answer_client(client, msg)
        else:
            self.autentification(client, msg)

    def answer_client(self, client, msg):
        if 'commands' in msg:
            self.commands(msg.get('commands'))

    def commands(self, commands):
        self.socketsignal.emit(commands)

    def autentification(self, client_socket, msg):
        login = msg['authentication'].get('login')
        password = msg['authentication'].get('password')
        if login is not None and password is not None:
            user = Users.authentificate(login, password)
            if user:
                self.signal_only_user(user.name)
                self.add_token(user)
                # print(user.login, user.password)
                msg = self.add_token(user)
                self.tokens[client_socket] = msg
                # print(self.tokens)
            else:
                msg = {
                    'errors': 'Неверный пароль'
                }
        else:
            msg = {
                'errors': 'Введите логин и пароль'
            }
        self.client_msg(client_socket, msg)
    def signal_only_user(self, name):
        self.namesigal.emit(name)

    def add_token(self, user):
        new_token = Tokens(id=user.id)
        session.add(new_token)
        session.commit()
        return {'access_token': new_token.token}

    def run(self):
        print('Сервер запущен')
        while self.runs:
            try:
                ready_to_read, _, _ = select(self.to_monitor, [], [])  # read, write, errors
            except KeyboardInterrupt:
                print('Сервер остановлен')
                break
            except Exception as e:
                print(e)
            for sock in ready_to_read:
                if sock is self.server:
                    self.accept_connection(sock)
                else:
                    self.read_message(sock)

    def stop_server(self):
        self.server.close()
        self.runs = False



if __name__ == '__main__':
    sock = Server('localhost')
    sock.run()
