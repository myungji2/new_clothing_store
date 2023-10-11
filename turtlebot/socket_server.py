#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import socket
import signal
import sys

HOST = '0.0.0.0'  # 서버 IP 주소
PORT = 12345     # 포트 번호

class SocketServer:
    def __init__(self):
        self.socket = None

    def start(self):
        # 소켓 생성
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 소켓 주소 바인딩
        self.socket.bind((HOST, PORT))

        # 연결 대기
        self.socket.listen()

        print('서버 대기 중...')

        rospy.init_node('talker', anonymous=True)
        pub = rospy.Publisher('chatter', String, queue_size=10)

        try:
            while not rospy.is_shutdown():
                # 클라이언트 연결 대기 및 처리
                client_socket, client_address = self.socket.accept()
                print('클라이언트 연결됨:', client_address)

                # 데이터 수신
                data = client_socket.recv(1024).decode()
                print('수신한 데이터:', data)

                # ROS 토픽으로 데이터 발행
                rospy.loginfo(data)
                pub.publish(str(data))

                # 클라이언트에게 데이터 재전송
                client_socket.sendall(data.encode())

                # 대기: 다음 데이터 도착까지
                next_data = client_socket.recv(1024).decode()

                # 클라이언트 소켓 연결 종료
                client_socket.close()

        except rospy.ROSInterruptException:
            pass
        finally:
            # 서버 소켓 연결 종료
            if self.socket:
                self.socket.close()

def signal_handler(sig, frame):
    print('프로그램 종료')
    sys.exit(0)

if __name__ == '__main__':
    server = SocketServer()
    signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C 시 프로그램 종료
    try:
        server.start()
    except rospy.ROSInterruptException:
        pass
