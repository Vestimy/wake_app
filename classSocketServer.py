import threading, socketserver
import socket, time

from PyQt5 import QtWidgets,QtCore


class Server(QtCore.QThread):
    socketsignal = QtCore.pyqtSignal(str)
    def __init__(self, ip, port):
        QtCore.QThread.__init__(self)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.errors = True
        try:
            self.socket.bind((ip, port))
        except OSError as e:
            print(e)
            self.running = False
            self.errors = False
        self.ip = ip
        self.port = port
        self.running = True
        self.clients = []
        self.users = {"Vestimy":"1234"}
    def run(self):
        while self.running:
            try:
                data, addr = self.socket.recvfrom(1024)

                if addr not in self.clients:
                    self.clients.append(addr)
                    msgs = data.decode("utf-8")
                    msgs = msgs.split("::")
                    self.check(msgs, addr)
                else:
                    msgs = data.decode("utf-8")
                    msgs = msgs.split("::")
                    self.check(msgs, addr)

                print(self.clients)
                itsatime = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())

                print("[" + addr[0] + "]=[" + str(addr[1]) + "]=[" + itsatime + "]/", end="")
                print(data.decode("utf-8"))
                msg = data.decode("utf-8")
                for client in self.clients:
                    if addr != client:
                        self.socket.sendto(data, client)

                los = msg.find("::")
                if los > 0:
                    msg = msg.split("::")
                    print(msg)
                    self.command(msg[1])
                    if msg[1] == "play":
                        print("все работает!")
                    elif msg[1] == "stop":
                        print("Остонваливаем лебедку")
            except:
                print("\n[ Server Stopped ]")
                self.running = False
                self.stop()
    def check(self, value, addr):
        client = addr
        print(value)
        if value[0] == "login":
            for value[1] in self.users:
                if value[2] == self.users[value[1]]:
                    self.send_check(client)
    def send_check(self, addr):
        self.socket.sendto(("Логин сработал!").encode("utf-8"), addr)
    def stop(self):
        self.socket.close()

    def stops(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        addr = (self.ip, self.port)
        sock.connect(addr)
        sock.send(b'stop')
    def command(self, message):
        try:
            print("Сообщенеие: {}".format(message))
            # message = bytes.decode(message)
            print(message)
            if message == "keyForward":
                self.socketsignal.emit("keyForward")
            elif message == "keyBackward":
                self.socketsignal.emit("keyBackward")
            elif message == "keyStop":
                self.socketsignal.emit("keyStop")
            elif message == "keyHome":
                self.socketsignal.emit("keyHome")
            elif message == "keyStartTimer":
                self.socketsignal.emit("keyStartTimer")
            elif message == "keySpeedUp":
                self.socketsignal.emit("keySpeedUp")
            elif message == "keySpeedDown":
                self.socketsignal.emit("keySpeedDown")
            elif message == "keyRevers":
                self.socketsignal.emit("keyRevers")
            elif message == "keyStart":
                self.socketsignal.emit("keyStart")
            else:
                pass
        except Exception as e:
            print("Error: {}".format(e))
            # sock.close()
    # def hell(self):
    #     self.queue.helloo()
