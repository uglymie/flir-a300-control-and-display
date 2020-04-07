# -*- coding:utf-8 -*-
import socket
ip_port = ('169.254.13.237', 23)
sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
# sk.bind(ip_port)
sk.connect(ip_port)

while True:
    cmd = input("Please input cmd:")  # 与人交互，输入命令
    # sk.sendall(b".image.sysimg.measureFuncs.spot.1.maxT \n")  # 把命令发送给对端
    sk.send(cmd.encode('utf-8'))
    data = sk.recv(1024)
    print(data)

# sk.sendall(b".image.sysimg.measureFuncs.spot.1.maxT \n")  # 把命令发送给对端
# sk.send(b"store -j temp.jpg\n")

# data = sk.recv(1024)
# print(data)
sk.close()
