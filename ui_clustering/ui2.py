import sys
import pickle
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QSlider, QDial, QPushButton
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPalette
form_secondwindow = uic.loadUiType("ui0.ui")[0]  # 두 번째창 ui
import ui3

class secondwindow(QDialog, QWidget, form_secondwindow):
    def __init__(self):
        super(secondwindow, self).__init__()
        self.initUI()
        self.showMaximized()  # 두번째창 실행

    def initUI(self):
        self.setupUi(self)
        self.HOME.clicked.connect(self.Home)
        # self.horizontalSlider = QSlider(Qt.Horizontal, self)
        # self.horizontalSlider_2 = QSlider(Qt.Horizontal, self)
        # self.horizontalSlider_3 = QSlider(Qt.Horizontal, self)

        # label_4 = QLabel('0', self)
        # label_5 = QLabel('0', self)
        # label_6 = QLabel('0', self)

        self.horizontalSlider.valueChanged.connect(self.valuechange)
        self.horizontalSlider_2.valueChanged.connect(self.valuechange)
        self.horizontalSlider_3.valueChanged.connect(self.valuechange)
        self.pushButton_2.clicked.connect(self.button2Function)

    def valuechange(self):
        r = self.horizontalSlider.value()
        g = self.horizontalSlider_2.value()
        b = self.horizontalSlider_3.value()

        self.label_4.setText(str(r))
        self.label_5.setText(str(g))
        self.label_6.setText(str(b))
        self.label_4.adjustSize()
        self.label_5.adjustSize()
        self.label_6.adjustSize()
        self.label_4.repaint()
        self.label_5.repaint()
        self.label_6.repaint()
        self.pushButton.setStyleSheet('background-color:rgb({},{},{})'.format(r,g,b))

    def button2Function(self):

        r = self.horizontalSlider.value()
        g = self.horizontalSlider_2.value()
        b = self.horizontalSlider_3.value()
        rgb=[r,g,b]
        with open('rgb.pkl', 'wb') as f:
            pickle.dump(rgb, f, protocol=pickle.HIGHEST_PROTOCOL)
        self.hide()  # 메인 윈도우 숨김
        self.second = ui3.window_3()
        self.second.exec() # 두번째창 닫을때까지 기다림
        self.showMaximized()  #두번째창 닫으면 다시 첫 번째 창 보여 짐

    def Home(self):
        self.close()  # 창 닫기