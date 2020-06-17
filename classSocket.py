import sys, os, time, datetime, configparser, serial, glob
from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5 import QtWidgets,QtCore
from wake import Ui_Form  # импорт нашего сгенерированного файла
from login import Ui_Login_Form

from socket import *

class mySocket(QtCore.QThread):
    soketSignal = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        host = "192.168.0.105"
        port = 8889
        addr = (host, port)
        self.tcp_socket = socket(AF_INET, SOCK_STREAM)

        self.tcp_socket.bind(addr)
        self.tcp_socket.listen(10)
        self.running = True

    def run(self):
        while self.running:
            conn, addr = self.tcp_socket.accept()
            print("Client addr: ", addr)
            data = conn.recv(1024)
            if not data:
                break
            else:
                print(data)
                conn.send(b'Hello from server')
