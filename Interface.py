# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Interface.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(892, 502)
        Dialog.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Israel))
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.img_lable = QtWidgets.QLabel(Dialog)
        self.img_lable.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.img_lable.setText("")
        self.img_lable.setObjectName("currentImg")
        self.gridLayout.addWidget(self.img_lable, 0, 0, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.flirIP = QtWidgets.QLineEdit(Dialog)
        self.flirIP.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.flirIP.setObjectName("flirIP")
        self.horizontalLayout_4.addWidget(self.flirIP)
        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(1, 2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.connect_B = QtWidgets.QPushButton(Dialog)
        self.connect_B.setObjectName("connect_B")
        self.horizontalLayout_5.addWidget(self.connect_B)
        self.exit_B = QtWidgets.QPushButton(Dialog)
        self.exit_B.setObjectName("exit_B")
        self.horizontalLayout_5.addWidget(self.exit_B)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.line_5 = QtWidgets.QFrame(Dialog)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.verticalLayout_3.addWidget(self.line_5)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_28 = QtWidgets.QLabel(Dialog)
        self.label_28.setObjectName("label_28")
        self.horizontalLayout.addWidget(self.label_28)
        self.maxT_label = QtWidgets.QLabel(Dialog)
        self.maxT_label.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.maxT_label.setText("")
        self.maxT_label.setObjectName("maxT_label")
        self.horizontalLayout.addWidget(self.maxT_label)
        self.label_29 = QtWidgets.QLabel(Dialog)
        self.label_29.setObjectName("label_29")
        self.horizontalLayout.addWidget(self.label_29)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_30 = QtWidgets.QLabel(Dialog)
        self.label_30.setObjectName("label_30")
        self.horizontalLayout_2.addWidget(self.label_30)
        self.minT_label = QtWidgets.QLabel(Dialog)
        self.minT_label.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.minT_label.setText("")
        self.minT_label.setObjectName("minT_label")
        self.horizontalLayout_2.addWidget(self.minT_label)
        self.label_31 = QtWidgets.QLabel(Dialog)
        self.label_31.setObjectName("label_31")
        self.horizontalLayout_2.addWidget(self.label_31)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_20 = QtWidgets.QLabel(Dialog)
        self.label_20.setObjectName("label_20")
        self.horizontalLayout_3.addWidget(self.label_20)
        self.avgT_label = QtWidgets.QLabel(Dialog)
        self.avgT_label.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.avgT_label.setText("")
        self.avgT_label.setObjectName("AVGT_label")
        self.horizontalLayout_3.addWidget(self.avgT_label)
        self.label_22 = QtWidgets.QLabel(Dialog)
        self.label_22.setObjectName("label_22")
        self.horizontalLayout_3.addWidget(self.label_22)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(17, 37, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_3.addWidget(self.line)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.autofocusQuick_B = QtWidgets.QPushButton(Dialog)
        self.autofocusQuick_B.setObjectName("autofocusQuick_B")
        self.horizontalLayout_6.addWidget(self.autofocusQuick_B)
        self.shootNow_B = QtWidgets.QPushButton(Dialog)
        self.shootNow_B.setObjectName("shootNow_B")
        self.horizontalLayout_6.addWidget(self.shootNow_B)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.verticalLayout_3.setStretch(0, 2)
        self.verticalLayout_3.setStretch(1, 1)
        self.verticalLayout_3.setStretch(2, 2)
        self.verticalLayout_3.setStretch(3, 1)
        self.verticalLayout_3.setStretch(4, 2)
        self.verticalLayout_3.setStretch(5, 2)
        self.verticalLayout_3.setStretch(6, 2)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 3)
        self.gridLayout.setColumnStretch(1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "FLIR A300 control"))
        self.label_2.setText(_translate("Dialog", "address:"))
        self.flirIP.setText(_translate("Dialog", "169.254.13.237"))
        self.connect_B.setText(_translate("Dialog", "连接"))
        self.exit_B.setText(_translate("Dialog", "退出"))
        self.label_28.setText(_translate("Dialog", "Max T:"))
        self.label_29.setText(_translate("Dialog", "°C"))
        self.label_30.setText(_translate("Dialog", "Min T:"))
        self.label_31.setText(_translate("Dialog", "°C"))
        self.label_20.setText(_translate("Dialog", "AVG T:"))
        self.label_22.setText(_translate("Dialog", "°C"))
        self.autofocusQuick_B.setText(_translate("Dialog", "快速聚焦"))
        self.shootNow_B.setText(_translate("Dialog", "抓图"))
