
import cv2
import threading
import sys
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QEvent, QObject
import time
from PyQt5.QtWidgets import QMainWindow, QPushButton

running = False
class SecondWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.showMaximized()

    def initUI(self):
        self.setGeometry(200, 200, 640, 480)
        self.setWindowTitle('Second Window')

        self.camera_button = QPushButton('Start Camera', self)
        self.camera_button.setGeometry(100, 100, 150, 30)
        self.camera_button.clicked.connect(self.startCamera)

    def startCamera(self):
        self.camera_instance = Camera()
        # self.camera_instance.start()
        #
        # print("사진을 찍습니다")
        # # 이미지 캡처 및 저장
        # self.camera_instance.capture_image()
        #
        # self.camera_instance.release()  # 웹캠 해제
        # self.close()  # 현재 창 닫기
class Camera():
    def run(self):
        global running
        cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.label.resize(int(width), int(height))
        start= time.time()

        while running:
            ret, img = cap.read()
            if ret:
                end = time.time()
                print(end-start)
                if end-start>10:
                    cv2.imwrite('a.jpg',img)
                    break
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                cv2.putText(img, "The picture will be taken in 10 seconds", (int(width/2)-200, 90), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0))
                cv2.rectangle(img, (int((width-192)/2),int((height-256)/2)), (int(width-(width-192)/2),int(height-(height-256)/2)), (0, 255, 0), 3)
                h,w,c = img.shape
                qImg = QtGui.QImage(img.data, w, h, w*c, QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap.fromImage(qImg)
                pixmap = pixmap.scaledToWidth(int(w*1.5))
                pixmap = pixmap.scaledToHeight(int(h*1.5))
                self.label.setPixmap(pixmap)
            else:
                QtWidgets.QMessageBox.about(self.win, "Error", "Cannot read frame.")
                print("cannot read frame.")
                break
        cap.release()
        print("Thread end.")
        # self.app.aboutToQuit.connect(self.onExit)
        # sys.exit(self.app.exec_())
    def stop(self):
        global running
        running = False
        print("stoped..")
    def start(self):
        global running
        running = True
        print(running)
        th = threading.Thread(target=self.run)
        th.start()
        print("started..")
    def onExit(self):
        print("exit")
        self.stop()
    def __init__(self):
        super().__init__()

        self.app = QtWidgets.QApplication([])
        self.win = QtWidgets.QWidget()
        self.vbox = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel()
        btn_start = QtWidgets.QPushButton("Camera On")

        btn_stop = QtWidgets.QPushButton("Camera Off")
        self.vbox.addWidget(self.label)
        self.vbox.addWidget(btn_start)

        self.vbox.addWidget(btn_stop)
        self.win.setLayout(self.vbox)
        self.win.show()

        btn_start.clicked.connect(self.start)

        btn_stop.clicked.connect(self.stop)
            # self.app.aboutToQuit.connect(self.onExit)
            # sys.exit(self.app.exec_())







