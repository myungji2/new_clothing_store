import socket

SERVER_IP = '192.168.126.248'  # 서버의 IP 주소
PORT = 12345                # 서버와 동일한 포트 번호

# 소켓 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(1)
# 서버에 연결
client_socket.connect((SERVER_IP, PORT))
print(2)
# 데이터 전송
message = '3'
client_socket.sendall(message.encode())
print(3)
# 데이터 수신 및 출력
data = client_socket.recv(1024)
print('수신한 데이터:', data.decode())

# 연결 종료
client_socket.close()