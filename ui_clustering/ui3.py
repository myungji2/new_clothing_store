from PyQt5.QtWidgets import *
from PyQt5 import uic
import pickle
from clustering_func import smilar_images
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QSlider, QDial, QPushButton
import ui4
from PyQt5.QtGui import *
window3 = uic.loadUiType("ui3.ui")[0]  # 두 번째창 ui

class window_3(QDialog, QWidget, window3):
    def __init__(self):
        super(window_3, self).__init__()
        self.initUI()
        self.showMaximized()  # 두번째창 실행

    def initUI(self):
        self.setupUi(self)
        with open("./rgb.pkl", "rb") as fr:
            rgb = pickle.load(fr)
        self.pushButton.setStyleSheet('background-color:rgb({},{},{})'.format(rgb[0], rgb[1], rgb[2]))

        rgb=[[rgb[0],rgb[1],rgb[2]]]
        images = smilar_images(rgb)
        self.pushButton_2.setIcon(QIcon(images[0]))
        self.pushButton_3.setIcon(QIcon(images[1]))
        self.pushButton_4.setIcon(QIcon(images[2]))
        self.pushButton_5.setIcon(QIcon(images[3]))
        self.pushButton_6.setIcon(QIcon(images[4]))
        self.pushButton_7.setIcon(QIcon(images[5]))
        self.pushButton_8.setIcon(QIcon(images[6]))
        self.pushButton_9.setIcon(QIcon(images[7]))


        self.HOME.clicked.connect(self.Home)
        self.pushButton_2.clicked.connect(self.button2)
        self.pushButton_3.clicked.connect(self.button3)
        self.pushButton_4.clicked.connect(self.button4)
        self.pushButton_5.clicked.connect(self.button5)
        self.pushButton_6.clicked.connect(self.button6)
        self.pushButton_7.clicked.connect(self.button7)
        self.pushButton_8.clicked.connect(self.button8)
        self.pushButton_9.clicked.connect(self.button9)






    def button2(self):
        with open("./rgb.pkl", "rb") as fr:
            rgb = pickle.load(fr)
        rgb = [[rgb[0], rgb[1], rgb[2]]]
        print(rgb)
        images = smilar_images(rgb)
        where=['A', images[0]]
        with open('where.pkl', 'wb') as f:
            pickle.dump(where, f, protocol=pickle.HIGHEST_PROTOCOL)
        self.hide()  # 메인 윈도우 숨김
        self.second = ui4.window_4()
        self.second.exec()  # 두번째창 닫을때까지 기다림
        self.showMaximized()
    def button3(self):
        with open("./rgb.pkl", "rb") as fr:
            rgb = pickle.load(fr)

        rgb = [[rgb[0], rgb[1], rgb[2]]]
        print(rgb)
        images = smilar_images(rgb)
        where = ['A', images[1]]
        with open('where.pkl', 'wb') as f:
            pickle.dump(where, f, protocol=pickle.HIGHEST_PROTOCOL)
        self.hide()  # 메인 윈도우 숨김
        self.second = ui4.window_4()
        self.second.exec()  # 두번째창 닫을때까지 기다림
        self.showMaximized()
    def button4(self):
        with open("./rgb.pkl", "rb") as fr:
            rgb = pickle.load(fr)

        rgb = [[rgb[0], rgb[1], rgb[2]]]
        print(rgb)
        images = smilar_images(rgb)
        where = ['A', images[2]]
        with open('where.pkl', 'wb') as f:
            pickle.dump(where, f, protocol=pickle.HIGHEST_PROTOCOL)
        self.hide()  # 메인 윈도우 숨김
        self.second = ui4.window_4()
        self.second.exec()  # 두번째창 닫을때까지 기다림
        self.showMaximized()
    def button5(self):
        with open("./rgb.pkl", "rb") as fr:
            rgb = pickle.load(fr)

        rgb = [[rgb[0], rgb[1], rgb[2]]]
        print(rgb)
        images = smilar_images(rgb)
        where = ['A', images[3]]
        with open('where.pkl', 'wb') as f:
            pickle.dump(where, f, protocol=pickle.HIGHEST_PROTOCOL)
        self.hide()  # 메인 윈도우 숨김
        self.second = ui4.window_4()
        self.second.exec()  # 두번째창 닫을때까지 기다림
        self.showMaximized()
    def button6(self):
        with open("./rgb.pkl", "rb") as fr:
            rgb = pickle.load(fr)

        rgb = [[rgb[0], rgb[1], rgb[2]]]
        print(rgb)
        images = smilar_images(rgb)
        where = ['A', images[4]]
        with open('where.pkl', 'wb') as f:
            pickle.dump(where, f, protocol=pickle.HIGHEST_PROTOCOL)
        self.hide()  # 메인 윈도우 숨김
        self.second = ui4.window_4()
        self.second.exec()  # 두번째창 닫을때까지 기다림
        self.showMaximized()
    def button7(self):
        with open("./rgb.pkl", "rb") as fr:
            rgb = pickle.load(fr)

        rgb = [[rgb[0], rgb[1], rgb[2]]]
        print(rgb)
        images = smilar_images(rgb)
        where = ['A', images[5]]
        with open('where.pkl', 'wb') as f:
            pickle.dump(where, f, protocol=pickle.HIGHEST_PROTOCOL)
        self.hide()  # 메인 윈도우 숨김
        self.second = ui4.window_4()
        self.second.exec()  # 두번째창 닫을때까지 기다림
        self.showMaximized()
    def button8(self):
        with open("./rgb.pkl", "rb") as fr:
            rgb = pickle.load(fr)

        rgb = [[rgb[0], rgb[1], rgb[2]]]
        print(rgb)
        images = smilar_images(rgb)
        where = ['A', images[6]]
        with open('where.pkl', 'wb') as f:
            pickle.dump(where, f, protocol=pickle.HIGHEST_PROTOCOL)
        self.hide()  # 메인 윈도우 숨김
        self.second = ui4.window_4()
        self.second.exec()  # 두번째창 닫을때까지 기다림
        self.showMaximized()
    def button9(self):
        with open("./rgb.pkl", "rb") as fr:
            rgb = pickle.load(fr)

        rgb = [[rgb[0], rgb[1], rgb[2]]]
        print(rgb)
        images = smilar_images(rgb)
        where = ['A', images[7]]
        with open('where.pkl', 'wb') as f:
            pickle.dump(where, f, protocol=pickle.HIGHEST_PROTOCOL)
        self.hide()  # 메인 윈도우 숨김
        self.second = ui4.window_4()
        self.second.exec()  # 두번째창 닫을때까지 기다림
        self.showMaximized()



    def Home(self):
        self.close()  # 창 닫기