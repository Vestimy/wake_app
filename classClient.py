import socket, json
import threading
from classDb import session
from classModels import Users
import rsa
import time


class ClientSocket:
    def __init__(self, ip, port=1802):
        self.runs = True
        self.check = None
        self.pubkey = None
        self.registred = None
        self.sock = self.sock_init(ip, port)
        self.msg = {}
        (self.pubkeys, self.privatekey) = rsa.newkeys(1024)
        self.fff = True


    def sock_init(self, ip, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        return sock

    def potok(self):
        self.potok = threading.Thread(target=self.run, daemon=True)
        self.potok.start()
        return self.potok

    def read_msg(self):
        data = self.sock.recv(1024)
        print(data)
        # print(data)
        data = json.loads(data)
        # print(data)
        if 'access_token' in data:
            return data['access_token']
        else:
            return data['errors']


    # def rsa_load(self, data):


    # def run(self):
    #
    #     print('Potok запущен')
    #     try:
    #         while self.runs:
    #             try:
    #                 data = self.sock.recv(4096)
    #
    #             except Exception:
    #                 print('Поток остановлен')
    #                 self.sock.close()
    #                 break
    #             else:
    #                 if self.pubkey is None:
    #                     pubkey = rsa.PublicKey.load_pkcs1(data)
    #                     self.pubkey = pubkey
    #                 else:
    #                     # self.msg_encrypt(data)
    #                     print(data)
    #                 print(data)
    #                 # data = self.sock.recv(4096)
    #                 # data = data.decode()
    #                 # self.reads_json(data)
    #             # print(data.decode())
    #             # self.msg_encrypt(data)
    #     except:
    #         print('Ошибка в цикле')
    #         self.runs = False
    def run(self):
        while self.runs:
            data = self.sock.recv(4096)
            if data == b'':
                break
            if self.pubkey is None:
                pubkey = rsa.PublicKey.load_pkcs1(data)
                self.pubkey = pubkey
            else:
                self.msg_encrypt(data)

    def msg_encrypt(self, msg):
        self.reads_json(rsa.decrypt(msg, self.privatekey))

    def reads_json(self, msg):
        # msg = rsa.encrypt()
        msg = json.loads(msg.decode())
        if 'access_token' in msg:
            self.msg['access_token'] = msg.get('access_token')
            self.msg.pop("authentication")
            self.fff = False

            print(msg)
        else:
            print(msg)
            print(msg.get('errors'))



    def send_msg(self, msg):
        if self.pubkey is None:
            raise Exception('Ошибка нет ключа')
        msg = msg.encode()
        try:
            self.sock.send(rsa.encrypt(msg, self.pubkey))
        except BrokenPipeError as e:
            print(e)

    def rsa_msg(self):
        self.sock.send(self.pubkeys.save_pkcs1())
    def quit(self):
        self.sock.close()


if __name__ == '__main__':
    client = ClientSocket('localhost', 1802)
    potok = client.potok()
    client.rsa_msg()


    # msgs = json.dumps(msg)
    # client.send_msg(msgs)
    # if 'access_token' in msgs:
    #     msg['access_token'] = client.read_msg()
    # else:
    #     msg['errors'] = client.read_msg()

    # print(msg)
    while client.fff:
        login = input('Введите логин: ')
        password = input('Введите пароль: ')

        client.msg['authentication'] = {
                'login': login,
                'password': password
            }

        client.send_msg(json.dumps(client.msg))

        time.sleep(1)

    while True:
        commanda = input('Введите разде')
        comm = input('Введите командку')

        client.msg[commanda] = comm
        client.send_msg(json.dumps(client.msg))

        print(client.msg)

        client.msg.pop(commanda)
# while T????????rue:
#     try:
#         msg = input("Введите сообщение: ")
#         if msg != '':
#             client.send_msg(msg)
#     except KeyboardInterrupt:
# break
