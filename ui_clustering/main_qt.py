import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import ui2
import test
import test2

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("ui1.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        #버튼에 기능을 연결하는 코드
        self.btn_1.clicked.connect(self.button_Second)
        self.btn_2.clicked.connect(self.button_two)

    def button_Second(self):
        self.hide() #메인 윈도우 숨김
        self.second = ui2.secondwindow()
        self.second.exec() # 두번째창 닫을때까지 기다림
        self.showMaximized()  #두번째창 닫으면 다시 첫 번째 창 보여 짐
    def button_two(self):
        self.second=test.SecondWindow()
        self.second.show()
if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.showMaximized()
    app.exec_()