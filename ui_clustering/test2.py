import cv2
import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import time
from PyQt5.QtWidgets import QMainWindow, QPushButton
class SecondWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 640, 480)
        self.setWindowTitle('Second Window')

        self.camera_button = QPushButton('Start Camera', self)
        self.camera_button.setGeometry(100, 100, 150, 30)
        self.camera_button.clicked.connect(self.startCamera)

    def startCamera(self):
        self.camera_instance = Camera3()
        self.camera_instance.start()

        time.sleep(10)  # 10초 대기
        print("사진을 찍습니다")
        # 이미지 캡처 및 저장
        self.camera_instance.capture_image()

        self.camera_instance.release()  # 웹캠 해제
        self.close()  # 현재 창 닫기

class Camera3:
    def __init__(self):
        self.capture = None

    def start(self):
        self.capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.show_camera()

    def show_camera(self):
        while True:
            ret, frame = self.capture.read()
            if not ret:
                break

            cv2.imshow('Camera', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def capture_image(self):
        ret, frame = self.capture.read()
        if ret:
            cv2.imwrite('captured_image.jpg', frame)

    def release(self):
        self.capture.release()
        cv2.destroyAllWindows()
"""
class ImageViewer(QtWidgets.QWidget):
    # parent 가 없어도 단독으로 사용가능하게
    # super parent를 상속받음
    def __init__(self, parent=None):
        super(ImageViewer, self).__init__(parent)
        self.image = QtGui.QImage()
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)

    # 다시 위젯을 그려줌 여기서 웹캠 화면을 출력
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)

    # 웹캠 사이즈에 맞춰 조절
    def setImage(self, image):
        # 이미지가 안넘어오면 출력
        if image.isNull():
            print("Viewer Dropped frame!")

        self.image = image
        #size가 다르면 fixed
        #image 사이즈는 640 480 웹캠 크기
        if image.size() != self.size():
            self.setFixedSize(image.size())
        self.update()


class ShowVideo(QtCore.QObject):
    flag = 1 #이미지 경로를 각각 다르게 해주기위해
    # 캠화면 3개 출력
    VideoSignal1 = QtCore.pyqtSignal(QtGui.QImage)
    VideoSignal2 = QtCore.pyqtSignal(QtGui.QImage)
    VideoSignal3 = QtCore.pyqtSignal(QtGui.QImage)
    def __init__(self, parent=None):
        super(ShowVideo, self).__init__(parent)
        self.run_video = True
        self.camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    def startVideo(self):
        #run_video가 true인 동안 실행
        while self.run_video:
            #웹캠 영상 이미지 가져옴
            self.ret, self.image = self.camera.read()
            #웹캠 영상 이미지 크기 가져옴
            height, width = self.image.shape[:2]
            #rgb형태로 변환
            color_swapped_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            hsv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
            self.qt_image = QtGui.QImage(color_swapped_image.data,
                                    width,
                                    height,
                                    color_swapped_image.strides[0],
                                    QtGui.QImage.Format_RGB888)
            # self.qt_image1 = QtGui.QImage(gray_image.data,
            #                         width,
            #                         height,
            #                         gray_image.strides[0],
            #                         QtGui.QImage.Format_Grayscale8)
            # self.qt_image2 = QtGui.QImage(hsv_image.data,
            #                          width,
            #                          height,
            #                          hsv_image.strides[0],
            #                          QtGui.QImage.Format_RGB888)
            #각각의 화면에 웹캠 영상 이미지 내보냄
            self.VideoSignal1.emit(self.qt_image)
            # self.VideoSignal2.emit(self.qt_image1)
            # self.VideoSignal3.emit(self.qt_image2)

            #영상 이미지 갱신 간격
            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(25, loop.quit) #25 ms
            loop.exec_()

    def stopVideo(self):
        self.run_video = False
        self.ret, self.image = self.camera.read()

    def restartVideo(self):
        self.run_video = True
        self.startVideo()

    def savePicture(self, text):
        print("HERE :", text)
        if self.run_video == False:
            filename = './webcam_image_{}_{}.png'.format(text, self.flag)
            # filename1 = './webcam_grayimage_{}_{}.png'.format(text, self.flag)
            # filename2 = './webcam_hsvimage_{}_{}.png'.format(text, self.flag)
            self.qt_image.save(filename)
            # self.qt_image1.save(filename1)
            # self.qt_image2.save(filename2)
            self.flag = self.flag + 1

        self.run_video = True
        self.startVideo()

class camera3(QtWidgets.QApplication,ShowVideo,ImageViewer):
    if __name__ == '__main__':
        app = QtWidgets.QApplication(sys.argv)

        thread = QtCore.QThread()
        thread.start()
        vid = ShowVideo()
        vid.moveToThread(thread)

        image_viewer1 = ImageViewer()
        # image_viewer2 = ImageViewer()
        # image_viewer3 = ImageViewer()

        vid.VideoSignal1.connect(image_viewer1.setImage)
        # vid.VideoSignal2.connect(image_viewer2.setImage)
        # vid.VideoSignal3.connect(image_viewer3.setImage)

        push_button2 = QtWidgets.QPushButton('캡쳐')
        input_box = QtWidgets.QLineEdit('팀명')
        push_button3 = QtWidgets.QPushButton('저장')
        push_button4 = QtWidgets.QPushButton('취소')
        push_button2.clicked.connect(vid.stopVideo)
        push_button3.clicked.connect(lambda: vid.savePicture(input_box.text()))
        push_button4.clicked.connect(vid.restartVideo)

        layout = QtWidgets.QHBoxLayout()
        box01 = QtWidgets.QVBoxLayout()
        box02 = QtWidgets.QVBoxLayout()

        box01.addWidget(image_viewer1)
        # box01.addWidget(image_viewer2)
        box02.addWidget(push_button2)
        box02.addWidget(input_box)
        box02.addWidget(push_button3)
        box02.addWidget(push_button4)
        # box01 imageviewer2개 추가
        layout.addLayout(box01)
        # imageviewr1개 추가
        # layout.addWidget(image_viewer3)
        # button3개와 입력창 추가
        layout.addLayout(box02)
        layout_widget = QtWidgets.QWidget()

        layout_widget.setLayout(layout)

        main_window = QtWidgets.QMainWindow()
        main_window.setCentralWidget(layout_widget)
        main_window.show()
        # 바로 웹캠 영상 시작
        vid.startVideo()


        sys.exit(app.exec_())
        
"""
