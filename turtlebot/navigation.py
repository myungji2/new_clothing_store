#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import PoseWithCovarianceStamped
from nav_msgs.msg import OccupancyGrid
from nav_msgs.msg import Odometry
import time
import os
import sys
import signal
# from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSizePolicy, QLabel, QFontDialog
# from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QFileDialog
# from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *
from std_srvs.srv import Empty, EmptyRequest

data = None
global select_menu
select_menu = None


# Callbacks definition


def socket_listener():
    global sub_from_out
    rospy.init_node('listener', anonymous=True)
    sub_from_out = rospy.wait_for_message("chatter", String)
    rospy.loginfo(rospy.get_caller_id() + "%s", sub_from_out.data)


def signal_handler(sig, frame):
    time.sleep(3)
    os.system('killall -9 python rosout')
    sys.exit(0)


def cost_map_clear():
    clear_costmaps_srv = rospy.ServiceProxy('/move_base/clear_costmaps', Empty)
    clear_costmaps_srv(EmptyRequest())
    rospy.loginfo("costmap clear")


def read_file():
    global lines
    file = open('new.txt', 'r')
    lines = file.readlines()
    file.close()


def callbackFunction(msg):
    global data
    data = msg
    a = data.pose.pose.position.x


def active_cb():
    # rospy.loginfo("Goal pose being processed")
    pass


def feedback_cb(feedback):
    # rospy.loginfo("Current location: "+str(feedback))
    pass


def done_cb(status, result):
    if status == 3:
        rospy.loginfo("Goal reached")
    if status == 2 or status == 8:
        rospy.loginfo("Goal cancelled")
    if status == 4:
        rospy.loginfo("Goal aborted")


def move_tur(where):
    global finished
    global navclient
    global lines
    navclient = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    navclient.wait_for_server()

    # Example of navigation goal
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()

    goal.target_pose.pose.position.x = float(lines[where * 8 - 7].strip('\n'))
    goal.target_pose.pose.position.y = float(lines[where * 8 - 6].strip('\n'))
    goal.target_pose.pose.position.z = float(lines[where * 8 - 5].strip('\n'))
    goal.target_pose.pose.orientation.x = float(lines[where * 8 - 4].strip('\n'))
    goal.target_pose.pose.orientation.y = float(lines[where * 8 - 3].strip('\n'))
    goal.target_pose.pose.orientation.z = float(lines[where * 8 - 2].strip('\n'))
    goal.target_pose.pose.orientation.w = float(lines[where * 8 - 1].strip('\n'))

    navclient.send_goal(goal, done_cb, active_cb, feedback_cb)
    finished = navclient.wait_for_result()


def init_pose():
    pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size=1)
    init_msg = PoseWithCovarianceStamped()
    init_msg.header.frame_id = "map"
    print("select init_pose on rviz>>>>>")
    sub = rospy.wait_for_message('initialpose', PoseWithCovarianceStamped)
    init_msg.pose.pose.position.x = sub.pose.pose.position.x
    init_msg.pose.pose.position.y = sub.pose.pose.position.y
    init_msg.pose.pose.orientation.x = sub.pose.pose.orientation.x
    init_msg.pose.pose.orientation.y = sub.pose.pose.orientation.y
    init_msg.pose.pose.orientation.z = sub.pose.pose.orientation.z
    init_msg.pose.pose.orientation.w = sub.pose.pose.orientation.w
    rospy.sleep(1)
    rospy.loginfo("setting initial pose")
    pub.publish(init_msg)
    rospy.loginfo("initial pose is set")
    cost_map_clear()


def navigation():
    global finished
    global navclient
    global data
    global lines
    init_pose()
    cost_map_clear()
    while (1):
        print("<<< start navigation >>>")
        sub_from_out = rospy.wait_for_message("chatter", String)
        rospy.loginfo(rospy.get_caller_id() + "%s", sub_from_out.data)
        cost_map_clear()
        where = int(sub_from_out.data)
        if where == -1:
            break
        else:
            move_tur(where)
        if not finished:
            print("경로 오류로 시작지점으로 돌아갑니다.")
            move_tur(1)
        else:
            while (1):

                if where == 1:
                    rospy.loginfo(navclient.get_result())
                    print("<<< finish navigation >>>")
                    break
                else:
                    print("3초후 돌아갑니다")
                    time.sleep(3)
                    move_tur(1)
                    if finished:
                        rospy.loginfo(navclient.get_result())
                        print("<<< return to home >>>")
                        break


def Add_goal(text):
    global finished
    global navclient
    # global data
    global lines
    data = None
    # init_pose()
    # rospy.Subscriber('initialpose', PoseWithCovarianceStamped,callbackFunction)
    print("select goal on rviz>>>>>")
    sub = rospy.wait_for_message('initialpose', PoseWithCovarianceStamped)

    file_1 = open('new.txt', 'a')

    contents1 = str(sub.pose.pose.position.x)
    contents2 = str(sub.pose.pose.position.y)
    contents3 = str(sub.pose.pose.position.z)
    contents4 = str(sub.pose.pose.orientation.x)
    contents5 = str(sub.pose.pose.orientation.y)
    contents6 = str(sub.pose.pose.orientation.z)
    contents7 = str(sub.pose.pose.orientation.w)
    file_1.write(text)
    file_1.write("\n")
    file_1.write(contents1)
    file_1.write("\n")
    file_1.write(contents2)
    file_1.write("\n")
    file_1.write(contents3)
    file_1.write("\n")
    file_1.write(contents4)
    file_1.write("\n")
    file_1.write(contents5)
    file_1.write("\n")
    file_1.write(contents6)
    file_1.write("\n")
    file_1.write(contents7)
    file_1.write("\n")

    file_1.close()
    sub = None
    # init_pose()
    read_file()


def Modify_goal():
    global finished
    global navclient
    global data
    global lines
    data = None
    lines_old = lines
    # init_pose()
    point_num = int(input("number of point want modify>>>"))
    print("select goal on rviz>>>>>")
    sub = rospy.wait_for_message('initialpose', PoseWithCovarianceStamped)

    content1 = str(sub.pose.pose.position.x)
    content2 = str(sub.pose.pose.position.y)
    content3 = str(sub.pose.pose.position.z)
    content4 = str(sub.pose.pose.orientation.x)
    content5 = str(sub.pose.pose.orientation.y)
    content6 = str(sub.pose.pose.orientation.z)
    content7 = str(sub.pose.pose.orientation.w)

    lines_old[point_num * 8 - 7] = content1
    lines_old[point_num * 8 - 6] = content2
    lines_old[point_num * 8 - 5] = content3
    lines_old[point_num * 8 - 4] = content4
    lines_old[point_num * 8 - 3] = content5
    lines_old[point_num * 8 - 2] = content6
    lines_old[point_num * 8 - 1] = content7
    finish = 7
    if (finish == 7):
        file_new = open('new.txt', 'w')
        for i in range(len(lines_old)):
            contents = lines_old[i]
            file_new.write(contents.strip('\n'))
            file_new.write("\n")
            finish = 0
    file_new.close()
    # init_pose()
    read_file()
    sub = None


def main(self):
    global finished
    global navclient
    global data
    global lines
    # init_pose()
    while (1):
        ab = 0
        abc = 0
        data = None
        if select_menu == -1:
            break
        elif select_menu == 1:
            navigation(self)
            break
        elif select_menu == 2:
            Add_goal(text)
            break
        elif select_menu == 3:
            Modify_goal()
            break


class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global select_menu
        self.setWindowTitle('MainWindow')
        self.resize(800, 480)
        self.center()
        btn = QPushButton('NAVIGATION', self)
        btn.move(50, 50)
        btn.resize(btn.sizeHint())
        btn.clicked.connect(self.btn_main_to_NAVIGATION)
        btn = QPushButton('ADD GOAL', self)
        btn.move(50, 100)
        btn.resize(btn.sizeHint())
        btn.clicked.connect(self.btn_main_to_ADD)
        btn = QPushButton('MODIFY GOAL', self)
        btn.move(50, 150)
        btn.resize(btn.sizeHint())
        btn.clicked.connect(self.btn_main_to_MODIFY)
        self.center()
        self.show()
        select_menu = 0

    def btn_main_to_NAVIGATION(self):
        global select_menu
        self.hide()
        select_menu = 1
        print("presh main_to_nav>>>>%d" % select_menu)
        # self.anotherwindow = MAIN()
        # self.resize(800,480)
        # self.center()         # 메인윈도우 숨김
        self.anotherwindow = NAVIGATION()
        self.resize(800, 480)
        self.center()
        self.anotherwindow.show()

    def btn_main_to_ADD(self):
        global select_menu
        self.hide()
        select_menu = 2
        # self.anotherwindow = MAIN()
        # self.resize(800,480)
        # self.center()         # 메인윈도우 숨김                   # 메인윈도우 숨김
        self.anotherwindow = ADD()
        self.resize(800, 480)
        self.center()
        self.anotherwindow.show()

    def btn_main_to_MODIFY(self):
        global select_menu
        self.hide()
        select_menu = 3
        # self.anotherwindow = MAIN()
        # self.resize(800,480)
        # self.center()         # 메인윈도우 숨김                   # 메인윈도우 숨김
        self.anotherwindow = MODIFY()
        self.resize(800, 480)
        self.center()
        self.anotherwindow.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class NAVIGATION(QWidget):
    def __init__(self):
        super(NAVIGATION, self).__init__()
        self.initUi()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUi(self):
        self.setWindowTitle('NAVIGATION')
        self.resize(800, 480)
        self.center()
        btn = QPushButton('NAVIGATION to main', self)
        btn.move(50, 50)
        btn.resize(btn.sizeHint())
        # sub = rospy.Subscriber('map', OccupancyGrid,self.map_callbackFunction)
        btn.clicked.connect(self.btn_second_to_main)
        self.show()

        self.worker = Worker_NAV()
        self.worker.start()

    def btn_second_to_main(self):
        self.stop
        global select_menu
        self.anotherwindow = MyApp()
        self.anotherwindow.show()
        select_menu = 0
        self.close()

    def stop(self):
        self.worker.power = False
        self.worker.quit()
        self.worker.wait(3000)
        print("nav 종료")


class ADD(QWidget):
    def __init__(self):
        super(ADD, self).__init__()
        self.initUi()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def stop(self):
        self.worker.power = False
        self.worker.quit()
        self.worker.wait(3000)
        print("add 종료")

    def initUi(self):
        self.setWindowTitle('ADD GOAL')
        self.resize(800, 480)
        self.center()
        btn = QPushButton('ADD GOAL to main', self)
        btn.move(50, 50)
        btn.resize(btn.sizeHint())
        # sub = rospy.Subscriber('map', OccupancyGrid,self.map_callbackFunction)
        btn.clicked.connect(self.btn_second_to_main)
        btn2 = QPushButton("stop", self)
        btn2.move(50, 100)
        btn.clicked.connect(self.btn_stop)

        self.line_edit = QLineEdit(self)
        self.line_edit.move(75, 150)

        self.button = QPushButton(self)
        self.button.move(75, 175)
        self.button.setText('rviz에서 장소 선택하기')
        self.button.clicked.connect(self.button_event)

        self.show()

    def button_event(self):
        self.text = self.line_edit.text()  # line_edit text 값 가져오기
        self.worker = Worker_ADD(self)
        self.worker.start()

    def btn_second_to_main(self):
        self.stop()
        global select_menu
        select_menu = 0
        self.anotherwindow = MyApp()
        self.anotherwindow.show()
        self.close()

    def btn_stop(self):
        self.stop()
        self.close()


class MODIFY(QWidget):
    def __init__(self):
        super(MODIFY, self).__init__()
        self.initUi()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def stop(self):
        self.worker.power = False
        self.worker.quit()
        self.worker.wait(3000)
        print("modify 종료")

    def initUi(self):
        self.setWindowTitle('MODIFY GOAL')
        self.resize(800, 480)
        self.center()
        btn = QPushButton('MODIFY GOAL to main', self)
        btn.move(50, 50)
        btn.resize(btn.sizeHint())
        # sub = rospy.Subscriber('map', OccupancyGrid,self.map_callbackFunction)
        btn.clicked.connect(self.btn_second_to_main)
        btn2 = QPushButton("stop", self)
        btn2.move(50, 100)
        btn.clicked.connect(self.btn_stop)
        self.show()
        self.worker = Worker_MODIFY()
        self.worker.start()

        # self.show()

    def btn_second_to_main(self):
        global select_menu
        self.anotherwindow = MyApp()
        self.anotherwindow.show()
        select_menu = 0
        self.stop()
        self.close()

    def btn_stop(self):
        self.stop()
        self.close()


class Worker_NAV(QThread):
    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        navigation()
        self.stop()

    def resume(self):
        self.running = True

    def pause(self):
        self.running = False

    def stop(self):
        self.power = False
        self.quit()


class Worker_ADD(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.running = True
        self.parent = parent

    def run(self):
        Add_goal(self.parent.text)
        self.stop()

    def resume(self):
        self.running = True

    def pause(self):
        self.running = False

    def stop(self):
        self.power = False
        self.quit()
        self.wait(3000)  # 3초 대기 (바로 안꺼질수도)


class Worker_MODIFY(QThread):
    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        Modify_goal()
        self.stop()

    def resume(self):
        self.running = True

    def pause(self):
        self.running = False

    def stop(self):
        self.power = False
        self.quit()
        self.wait(3000)  # 3초 대기 (바로 안꺼질수도)


class MAIN(QWidget):

    def __init__(self):
        super(MAIN, self).__init__()
        self.initUi()

    global select_menu

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUi(self):
        self.setWindowTitle('MAIN_FUNC')
        self.resize(800, 480)
        self.center()

        self.close()
        # self.show()

    def map_callbackFunction(msg):
        map_1 = msg
        print(map_1)

    def btn_second_to_main(self):
        self.anotherwindow = MyApp()
        self.anotherwindow.show()
        self.close()


if __name__ == '__main__':
    rospy.init_node('goal_pose')
    read_file()
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())