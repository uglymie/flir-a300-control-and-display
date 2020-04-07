import telnetlib, socket, ftplib
import logging

log = logging.getLogger('root')

class FLIR(object):
    def __init__(self):
        self.tn = None
        self.host = '169.254.13.237'    # 192.168.1.135
        self.port = 23
        self.timeout = 2
    def connect(self):
        try:
            self.tn = telnetlib.Telnet(self.host, self.port, self.timeout)
        except socket.timeout:
            log.info("FLIR.connect() socket.timeout")
        # when connecting, just read until you reach the prompt
        self.tn.read_until(b'msc', 1)

    def getBoxTemp(self, height, width, rx, ry):
        self.tn.write(b'rset .image.sysimg.measureFuncs.mbox.1.active true\n')
        self.tn.read_until(b'>', 1).decode('ascii')
        self.tn.write(b'rset .image.sysimg.measureFuncs.mbox.1.height ' + str(height).encode('ascii') + b'\n')
        self.tn.read_until(b'>', 1).decode('ascii')     # 读取直到遇到预期的给定字节字符串，或直到超时秒过去
        self.tn.write(b'rset .image.sysimg.measureFuncs.mbox.1.width ' + str(width).encode('ascii') + b'\n')
        self.tn.read_until(b'>', 1).decode('ascii')
        self.tn.write(b'rset .image.sysimg.measureFuncs.mbox.1.x ' + str(rx).encode('ascii') + b'\n')
        self.tn.read_until(b'>', 1).decode('ascii')
        self.tn.write(b'rset .image.sysimg.measureFuncs.mbox.1.y ' + str(ry).encode('ascii') + b'\n')
        self.tn.read_until(b'>', 1).decode('ascii')

        # self.tn.write(b'rls -t .image.sysimg.measureFuncs.mbox.1.maxT\n')
        # self.tn.write(b'rls - .image.sysimg.measureFuncs.mbox.1.maxT \n')
        # self.tn.read_until(b'>', 1).decode('ascii')
        # log.info('命令执行结果：%s' % command_result)


    def getInfo(self):
        self.tn.write(b'rls .image.sysimg.measureFuncs\n')

        command_result = self.tn.read_until(b'>', 1).decode('ascii')

        print('命令执行结果：%s' % command_result)

if __name__ ==  "__main__":
    cam = FLIR()
    cam.connect()
    cam.getInfo()
