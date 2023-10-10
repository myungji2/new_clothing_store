import cv2
import threading
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
import time
running = False
def run():
    global running
    cap = cv2.VideoCapture(0)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    label.resize(int(width), int(height))
    start= time.time()
    while running:
        ret, img = cap.read()
        if ret:
            end = time.time()
            if end-start>1000:
                cv2.imwrite('a.png',img)
                break
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            cv2.putText(img, "10 seconds ", (int(width/2)-200, 90), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0))
            cv2.rectangle(img, (int((width-192)/2),int((height-256)/2)), (int(width-(width-192)/2),int(height-(height-256)/2)), (0, 255, 0), 3)
            h,w,c = img.shape
            qImg = QtGui.QImage(img.data, w, h, w*c, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(qImg)
            pixmap = pixmap.scaledToWidth(int(w*1.5))
            pixmap = pixmap.scaledToHeight(int(h*1.5))
            label.setPixmap(pixmap)
        else:
            QtWidgets.QMessageBox.about(win, "Error", "Cannot read frame.")
            print("cannot read frame.")
            break
    cap.release()
    print("Thread end.")
def stop():
    global running
    running = False
    print("stoped..")
def start():
    global running
    running = True
    th = threading.Thread(target=run)
    th.start()
    print("started..")
def onExit():
    print("exit")
    stop()
app = QtWidgets.QApplication([])
win = QtWidgets.QWidget()
vbox = QtWidgets.QVBoxLayout()
label = QtWidgets.QLabel()
btn_start = QtWidgets.QPushButton("Camera On")
btn_stop = QtWidgets.QPushButton("Camera Off")
vbox.addWidget(label)
vbox.addWidget(btn_start)
vbox.addWidget(btn_stop)
win.setLayout(vbox)
win.show()
btn_start.clicked.connect(start)
btn_stop.clicked.connect(stop)
app.aboutToQuit.connect(onExit)
sys.exit(app.exec_())







