# -------------------------------------------------------------------------------
# Name:        FLIR A320 control software
# Purpose:	   This software controls the FLIR A320
#
# Author:      Jonathan D. Müller
#
# Created:     03/09/2017
# Copyright:   (c) Jonathan D. Müller 2017
# Licence:     GPL
# -------------------------------------------------------------------------------

# System stuff
import datetime, ctypes
from time import strftime  # For logging
from os.path import expanduser  # for user directory
import os.path

# Import Qt5
# from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# Import the user interface
from Interface import *
import functions.flir

import cv2
import time

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


class Main(QMainWindow, Ui_Dialog):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        log.info("Starting FLIR program")
        self.cam = None
        self.currentImg = None
        self.logFolder = ''

        # initialise the data list: 1x Date, 2x Arduino, 4x 6262
        # self.data = [float('nan')]*7
        # These threads run in the background
        self.initUI()

        self.flir_running = False
        self.logging_running = False

        # set up timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timed_tasks)

    def initUI(self):
        # Check for COM ports and add them
        #
        self.ui.connect.clicked.connect(self.connectFLIR)  # & flirIP
        self.ui.autofocusFull.clicked.connect(self.autofocusFull)
        self.ui.autofocusQuick.clicked.connect(self.autofocusQuick)
        self.ui.shootNow.clicked.connect(self.shootNow)
        self.ui.setAtmT.clicked.connect(self.setAtmT)  # atmT
        self.ui.setAmbT.clicked.connect(self.setAmbT)  # ambT
        self.ui.setDist.clicked.connect(self.setDist)  # dist
        self.ui.setRH.clicked.connect(self.setRH)  # rh
        self.ui.setEmissivity.clicked.connect(self.setEmissivity)  # emissivity
        self.ui.IntervalSet.clicked.connect(self.setInterval)  # IntervalTime
        self.ui.chooseFolderButton.clicked.connect(self.folderChooser)
        self.ui.LogStart.clicked.connect(self.logStart)
        # put in some new default
        # self.ui.IntervalTime.setText("240")

    def timed_tasks(self):
        self.shootNow()

    def connectFLIR(self):
        if (self.flir_running == True):
            log.info("Disconnecting FLIR")
            self.cam.close()
            del self.cam
            self.ui.connect.setText("Connect")
            self.flir_running = False
        else:
            log.info("Connecting FLIR " + self.ui.flirIP.text())
            self.cam = flir(self.ui.flirIP.text())
            try:
                self.cam.connect()
            except:
                pass
            else:
                log.info("Setting camera date & time")
                self.cam.setDateTime()
                self.ui.connect.setText("Disconnect")
                self.flir_running = True
                log.info("Camera ready")

                m_pVLC_Inst = vlc.libvlc_new(0, sys.argv[1:])
                red_ip = b"rtsp://%s" % (self.ui.flirIP.text()).encode("ascii")
                vlcMedia = vlc.libvlc_media_new_location(m_pVLC_Inst, red_ip)
                if vlcMedia:
                    print("vlcMedia ----- get")
                else:
                    print("vlcMedia ----- error")
                m_pVLC_Player = vlc.libvlc_media_player_new_from_media(vlcMedia)
                vlc.libvlc_media_release(vlcMedia)
                vlc.libvlc_media_player_set_hwnd(m_pVLC_Player, self.ui.currentImg.winId().__int__())
                print(self.ui.currentImg.winId())
                ret = vlc.libvlc_media_player_play(m_pVLC_Player)
                print(ret)


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

    # 自动聚焦
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
        else:
            # Now show the resulting image
            log.info("Created file " + self.currentImg)
            image = QtGui.QImage(self.currentImg)
            image = image.scaled(640, 480, aspectRatioMode=QtCore.Qt.KeepAspectRatio,
                                 transformMode=QtCore.Qt.SmoothTransformation)  # To scale image for example and keep its Aspect Ration
            self.ui.currentImg.setPixmap(QtGui.QPixmap.fromImage(image))

    def setAtmT(self):
        log.info("set atmospheric T " + self.ui.atmT.text())
        try:
            self.cam.setAtmT(float(self.ui.atmT.text()))
        except:
            QMessageBox.warning(None, "Connect", "Please connect the camera.")

    def setAmbT(self):
        log.info("set ambient T " + self.ui.ambT.text())
        try:
            self.cam.setAmbT(float(self.ui.ambT.text()))
        except:
            QMessageBox.warning(None, "Connect", "Please connect the camera.")

    def setDist(self):
        log.info("set distance " + self.ui.dist.text())
        try:
            self.cam.setDist(float(self.ui.dist.text()))
        except:
            QMessageBox.warning(None, "Connect", "Please connect the camera.")

    def setRH(self):
        log.info("set relative humidity " + self.ui.rh.text())
        self.cam.setRH(float(self.ui.rh.text()) / 100)
        try:
            self.cam.setRH(float(self.ui.rh.text()) / 100)
        except:
            QMessageBox.warning(None, "Connect", "Please connect the camera.")

    def setEmissivity(self):
        log.info("set emissivity " + self.ui.emissivity.text())
        try:
            self.cam.setEmiss(float(self.ui.emissivity.text()))
        except:
            QMessageBox.warning(None, "Connect", "Please connect the camera.")

    def setInterval(self):
        log.info("set interval " + self.ui.IntervalTime.text())
        try:
            pass
        except:
            QMessageBox.warning(None, "Connect", "Please connect the camera.")
    # 选择存储路径
    def folderChooser(self):
        fname = QFileDialog.getExistingDirectory(self, "Select Directory",
                                                 expanduser("~\Documents"))
        if (fname == ""):
            log.debug("No folder selected")
            QMessageBox.warning(None, "No folder selected", "Please select a log folder.")
        else:
            log.info("Log data to: " + fname)
            self.logFolder = fname
            self.ui.logfolder.setText(fname)

    def logStart(self):
        if (self.logging_running == True):
            log.info("Stop logging")
            self.ui.LogStart.setText("Start logging")
            self.timer.stop()
            self.logging_running = False
        else:
            # Check if devices are connected
            if (self.flir_running == True):
                # Run every X seconds
                # self.autofocusFull() # first focus
                self.ui.LogStart.setText("Stop logging")
                self.timer.start(int(self.ui.IntervalTime.text()) * 1000)
                self.logging_running = True
            else:
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
    myappid = 'mycompany.myproduct.subproduct.version'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app = QApplication(sys.argv)
    myapp = Main()
    myapp.show()

    sys.exit(app.exec_())
