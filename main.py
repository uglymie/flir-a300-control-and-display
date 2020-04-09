# System stuff
import datetime, ctypes
from time import strftime  # For logging
from os.path import expanduser  # for user directory
import os.path

from PyQt5.QtWidgets import *

# Import the user interface
from Interface import *
import functions.flir

flir = functions.flir.FLIR

# Logging
import logging
import sys

os.environ['PYTHON_VLC_MODULE_PATH'] = "./functions/sdk"
import vlc

log = logging.getLogger('root')
log.setLevel(logging.DEBUG)
stream = logging.StreamHandler(sys.stdout)
stream.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] %(levelname)8s %(module)15s: %(message)s')
stream.setFormatter(formatter)
log.addHandler(stream)


class Main(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        # QMainWindow.__init__(self)
        # self.ui = Ui_Dialog()
        self.setupUi(self)
        log.info("Starting FLIR program")
        self.cam = None
        self.currentImg = None
        self.logFolder = ''

        # These threads run in the background
        self.initUI()

        self.flir_running = False
        self.logging_running = False

    def initUI(self):
        # Check for COM ports and add them
        self.connect_B.clicked.connect(self.connectFLIR)  # & flirIP
        # self.ui.autofocusFull.clicked.connect(self.autofocusFull)
        self.autofocusQuick_B.clicked.connect(self.autofocusQuick)
        self.shootNow_B.clicked.connect(self.shootNow)

        # self.exit_B.clicked.connect(self.close())

    # 连接相机显示实时流
    def connectFLIR(self):
        if (self.flir_running == True):
            log.info("Disconnecting FLIR")
            self.cam.close()
            del self.cam
            self.connect_B.setText("连接")
            self.flir_running = False
        else:
            log.info("Connecting FLIR " + self.flirIP.text())
            self.cam = flir(self.flirIP.text())
            try:
                self.cam.connect()
            except:
                pass
            else:
                log.info("Setting camera date & time")
                self.cam.setDateTime()
                self.connect_B.setText("断开")
                self.flir_running = True
                log.info("Camera ready")
                self.getStream()

    def getStream(self):
        # 使用VLC播放库
        m_pVLC_Inst = vlc.libvlc_new(0, sys.argv[1:])
        red_ip = b"rtsp://%s" % (self.flirIP.text()).encode("ascii")
        vlcMedia = vlc.libvlc_media_new_location(m_pVLC_Inst, red_ip)
        if vlcMedia:
            print("vlcMedia ----- get")
        else:
            print("vlcMedia ----- error")
        m_pVLC_Player = vlc.libvlc_media_player_new_from_media(vlcMedia)
        vlc.libvlc_media_release(vlcMedia)
        vlc.libvlc_media_player_set_hwnd(m_pVLC_Player, self.currentImg.winId().__int__())
        ret = vlc.libvlc_media_player_play(m_pVLC_Player)

        # 如果opencv可用
        # cap = cv2.VideoCapture("rtsp://%s/mpeg4" % (self.ui.flirIP.text()))
        # if cap.isOpened():
        #     log.info('FLIR A300 8Hz')
        # else:
        #     log.info("请检查协议。")
        # while True:
        #     frame = cap.read()[1]
        #     self.height, self.width, self.deep = frame.shape
        #     self.bytesPerLine = self.deep * self.width
        #     self.rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #     # image = QtGui.QImage(self.currentImg)
        #     image = QtGui.QImage(self.rgb.data, 640, 480, self.bytesPerLine, QtGui.QImage.Format_RGB888)
        #     image = image.scaled( 640, 480, aspectRatioMode=QtCore.Qt.KeepAspectRatio,
        #                          transformMode=QtCore.Qt.SmoothTransformation)  # To scale image for example and keep its Aspect Ration
        #     self.ui.currentImg.setPixmap(QtGui.QPixmap.fromImage(image))

    # 自动聚焦（预留）
    def autofocusFull(self):
        log.info("Full autofocus")
        try:
            self.cam.slowFocus()
        except:
            QMessageBox.warning(None, "Connect", "Please connect the camera.")

    # 快速聚焦
    def autofocusQuick(self):
        log.info("Quick autofocus")
        try:
            self.cam.quickFocus()
        except:
            QMessageBox.warning(None, "Connect", "Please connect the camera.")

    # 抓图
    def shootNow(self):
        log.info("shoot to " + self.logFolder)
        folder = ''
        if (self.logFolder == ''):
            folder = self.logFolder
        else:
            folder = self.logFolder + "/"

        try:
            self.currentImg = self.cam.shootJPG(folder)
        except:
            QMessageBox.warning(None, "Connect", "Please connect the camera.")

    def closeEvent(self, event):  # This is when the window is clicked to close
        log.info("Shutting down application")
        try:
            self.cam.close()
        except:
            pass
        log.info("Shutdown completed")
        log.info('------------------')
        event.accept()


# Show the image
if __name__ == "__main__":
    # This tells Windows to use my icon
    # myappid = 'mycompany.myproduct.subproduct.version'  # arbitrary string
    # ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app = QApplication(sys.argv)
    myapp = Main()
    myapp.show()

    sys.exit(app.exec_())
