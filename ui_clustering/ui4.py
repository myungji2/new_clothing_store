from PyQt5.QtWidgets import *
from PyQt5 import uic
import pickle
from clustering_func import smilar_images
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QSlider, QDial, QPushButton

from PyQt5.QtGui import *
window4 = uic.loadUiType("ui4.ui")[0]  # 두 번째창 ui

import socket

SERVER_IP = '192.168.126.248'  # 서버의 IP 주소
PORT = 12345  # 서버와 동일한 포트 번호

class window_4(QDialog, QWidget, window4):
    def __init__(self):
        super(window_4, self).__init__()
        self.initUI()
        self.showMaximized()  # 두번째창 실행

    def initUI(self):
        self.setupUi(self)
        self.HOME.clicked.connect(self.Home)
        with open("./where.pkl", "rb") as fr:
            where = pickle.load(fr)
        self.pushbutton2.setIcon(QIcon(where[1]))
        if where[0]=='A':
            '''
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # 서버에 연결
            client_socket.connect((SERVER_IP, PORT))
            # 데이터 전송
            message = '3'
            client_socket.sendall(message.encode())
            # 데이터 수신 및 출력
            data = client_socket.recv(1024)
            print('수신한 데이터:', data.decode())

            # 연결 종료
            client_socket.close()
            '''
            self.label.setText("고르신 옷은 1번 옷걸이에 있습니다. \n옷을 입어보시려면 로봇을 따라가주세요.")
        elif where[0]=='B':
            '''
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # 서버에 연결
            client_socket.connect((SERVER_IP, PORT))
            # 데이터 전송
            message = '2'
            client_socket.sendall(message.encode())
            # 데이터 수신 및 출력
            data = client_socket.recv(1024)
            print('수신한 데이터:', data.decode())

            # 연결 종료
            client_socket.close()
            '''
            self.label.setText("고르신 옷은 2 옷걸이에 있습니다. \n옷을 입어보시려면 로봇을 따라가주세요.")
        elif where[0] == '3':
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # 서버에 연결
            client_socket.connect((SERVER_IP, PORT))
            # 데이터 전송
            message = '2'
            client_socket.sendall(message.encode())
            # 데이터 수신 및 출력
            data = client_socket.recv(1024)
            print('수신한 데이터:', data.decode())

            # 연결 종료
            client_socket.close()
            self.label.setText("고르신 옷은 3 옷걸이에 있습니다. \n옷을 입어보시려면 로봇을 따라가주세요.")

        else:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # 서버에 연결
            client_socket.connect((SERVER_IP, PORT))
            # 데이터 전송
            message = '4'
            client_socket.sendall(message.encode())
            # 데이터 수신 및 출력
            data = client_socket.recv(1024)
            print('수신한 데이터:', data.decode())

            # 연결 종료
            client_socket.close()
            self.label.setText("고르신 옷은 4 옷걸이에 있습니다. \n옷을 입어보시려면 로봇을 따라가주세요.")

    def Home(self):
        self.close()  # 창 닫기