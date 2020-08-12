import socket, json
import threading
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
        data = json.loads(data)
        if 'access_token' in data:
            return data['access_token']
        else:
            return data['errors']

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
        msg = json.loads(msg.decode())
        if 'access_token' in msg:
            self.msg['access_token'] = msg.get('access_token')
            self.msg.pop("authentication")
            self.fff = False

            print(msg)
        else:
            print(msg)
            print(msg.pop('errors'))

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
    while client.fff:
        login = input('Введите логин: ')
        password = input('Введите пароль: ')
        try:
            client.msg.pop()
        except:
            pass

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
