# With help from https://stackoverflow.com/questions/20484984/telnet-read-until-function-doesnt-work

import telnetlib, socket, ftplib, time, datetime
import re
import logging
import numpy as np
np.set_printoptions(threshold=np.inf)


log = logging.getLogger('root')

class FLIR(object):
    def __init__(self, host):
        self.tn = None
        self.host = host
        self.port = 23
        self.timeout = 2

    def connect(self):
        try:
            self.tn = telnetlib.Telnet(self.host, self.port, self.timeout)
        except socket.timeout:
            log.info("FLIR.connect() socket.timeout")
        # when connecting, just read until you reach the prompt
        self.tn.read_until(b'msc]', 1)

        # self.getImgTemp()

    # 如果支持
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

        # command_result = self.tn.read_all().decode('ascii')
        # command_result = self.tn.read_very_eager().decode('ascii')
        # log.info('命令执行结果：%s' % command_result)
        # print(type(command_result))

    def getImgTemp(self):
        # self.tn.write(b'rls .image.sysimg.basicImgData.extraInfo \n')
        # print(self.tn.read_until(b'>', 1).decode('ascii'))

        self.tn.write(b'rls .image.sysimg.basicImgData.extraInfo.highT \n')
        strH = self.tn.read_until(b'>', 1).decode('ascii')
        highT = float(re.findall(r"\d+\.?\d*", strH)[0])-273.15     # 正则表达式取温度数字

        self.tn.write(b'rls .image.sysimg.basicImgData.extraInfo.levelT \n')
        strA = self.tn.read_until(b'>', 1).decode('ascii')
        avgT = float(re.findall(r"\d+\.?\d*", strA)[0]) - 273.15

        self.tn.write(b'rls .image.sysimg.basicImgData.extraInfo.lowT \n')
        strL = self.tn.read_until(b'>', 1).decode('ascii')
        lowT = float(re.findall(r"\d+\.?\d*", strL)[0])-273.15
        # print(round(highT, 2), round(lowT, 2))
        return (round(highT, 2), round(avgT, 2), round(lowT, 2))


    # Set camera date and time to the computer time
    def setDateTime(self):
        # Set the date
        self.tn.write(b'date\n')
        self.tn.read_until(b'Enter new date (mm/dd/yyyy): ', 1).decode('ascii')
        datenow = str(datetime.datetime.now().strftime('%m/%d/%Y')).encode('ascii')  # store date string
        self.tn.write(datenow + b'\n')
        self.tn.read_until(b'>', 1).decode('ascii')
        # Set the time
        self.tn.write(b'time\n')
        self.tn.read_until(b'Enter new time: ', 1).decode('ascii')
        timenow = str(datetime.datetime.now().strftime('%H:%M:%S')).encode('ascii')  # store time string
        self.tn.write(timenow + b'\n')
        self.tn.read_until(b'>', 1).decode('ascii')


    # Set file format to file containing temperature data
    def setFormat(self):
        self.tn.write(b'rset .image.services.store.format \"JPEG+PNG\"\n')
        self.tn.read_until(b'>', 1).decode('ascii')

    # Set colour palette
    # pal can be: bw, iron, rainbow. I like iron the most
    def setPal(self, pal):
        self.tn.write(b'rset .image.sysimg.palette.readFile ' + pal.encode('ascii') + b'\n')
        self.tn.read_until(b'>', 1).decode('ascii')

    # Quick Autofocus
    def quickFocus(self):
        self.tn.write(b'rset .system.focus.autofast true\n')
        time.sleep(2)
        self.tn.read_until(b'>', 1).decode('ascii')

    # Slow but full autofocus
    def slowFocus(self):
        self.tn.write(b'rset .system.focus.autofull true\n')
        time.sleep(5)
        self.tn.read_until(b'>', 1).decode('ascii')

    # Enable/disable overlay
    def overlay(self, enable):
        if (enable):
            print('enable')
            # Enable the legend
            self.tn.write(b'rset .image.services.store.overlay true\n')
            self.tn.read_until(b'>', 1).decode('ascii')
        else:
            print('disable')
            # Disable the legend
            self.tn.write(b'rset .image.services.store.overlay false\n')
            self.tn.read_until(b'>', 1).decode('ascii')

    # Enable/disable legend
    def legend(self, enable):
        if (enable):
            print('enable')
            # Enable the legend
            self.tn.write(b'rset .gui.system.hideGraphics false\n')
            self.tn.read_until(b'>', 1).decode('ascii')
        else:
            print('disable')
            # Disable the legend
            self.tn.write(b'rset .gui.system.hideGraphics true\n')
            self.tn.read_until(b'>', 1).decode('ascii')

    # self.tn.write(b'rest .rtp.pframes')
    # Shoot image and transfer
    def shootJPG(self, path):  # TODO: OPTION TO SET PATH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # shoot the image and store it temporarily on the camera
        self.tn.write(b'store -j temp.jpg\n')
        time.sleep(2)
        # Set the filename for storage on the computer, with date/time info
        filename = path + 'file-' + str(datetime.datetime.now().strftime('%Y%m%d-%H%M%S')) + '.jpg'
        # Transmit file from the camera through FTP
        ftp = ftplib.FTP(self.host)
        ftp.login()
        ftp.cwd('/')
        ftp.retrbinary('RETR ' + 'temp.jpg', open(filename, 'wb').write)
        ftp.quit()
        # After successful transmission of the file, delete it on the camera
        self.tn.write(b'del temp.jpg\n')
        self.tn.read_until(b'>', 1).decode('ascii')
        return filename

    def shootFFF(self, path):  # TODO: OPTION TO SET PATH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # TODO infor: https://developer.flir.com/forums/topic/metadata-format/
        # shoot the image and store it temporarily on the camera
        self.tn.write(b'store temp.fff\n')
        time.sleep(2)
        # Set the filename for storage on the computer, with date/time info
        filename = path + 'file-' + str(datetime.datetime.now().strftime('%Y%m%d-%H%M%S')) + '.fff'
        # Transmit file from the camera through FTP
        ftp = ftplib.FTP(self.host)
        ftp.login()
        ftp.cwd('/')
        ftp.retrbinary('RETR ' + 'temp.fff', open(filename, 'wb').write)
        ftp.quit()
        # After successful transmission of the file, delete it on the camera
        self.tn.write(b'del temp.fff\n')
        self.tn.read_until(b'>', 1).decode('ascii')
        return filename

    # Generic functions that allow more fine-grained, individual control of the camera
    def write(self, msg):
        self.tn.write(msg.encode('ascii') + b"\n")
        return True

    def read_until(self, value):
        return self.tn.read_until(value)

    def read_all(self):
        try:
            return self.tn.read_all().decode('ascii')
        except socket.timeout:
            print("read_all socket.timeout")
            return False

    def close(self):
        self.tn.write(b'exit\n')
        self.tn.close()
        return True

    def request(self, msg):
        self.__init__()
        self.connect()
        if self.write(msg) == True:
            self.close()
            resp = self.read_all()
            return resp
        else:
            return False
