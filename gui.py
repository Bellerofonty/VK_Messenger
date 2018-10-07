# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.10

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_VkMessenger(object):
    def setupUi(self, VkMessenger):
        VkMessenger.setObjectName("VkMessenger")
        VkMessenger.resize(531, 389)
        self.verticalLayoutWidget = QtWidgets.QWidget(VkMessenger)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(440, 230, 81, 121))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.btn_login = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_login.setObjectName("btn_login")
        self.verticalLayout.addWidget(self.btn_login)
        self.btn_start = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_start.setObjectName("btn_start")
        self.verticalLayout.addWidget(self.btn_start)
        self.btn_stop = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_stop.setObjectName("btn_stop")
        self.btn_stop.setEnabled(False)
        self.verticalLayout.addWidget(self.btn_stop)
        self.log = QtWidgets.QTextBrowser(VkMessenger)
        self.log.setGeometry(QtCore.QRect(10, 10, 421, 371))
        self.log.setObjectName("log")

        self.retranslateUi(VkMessenger)
        QtCore.QMetaObject.connectSlotsByName(VkMessenger)

    def retranslateUi(self, VkMessenger):
        _translate = QtCore.QCoreApplication.translate
        VkMessenger.setWindowTitle(_translate("VkMessenger", "VK Messenger"))
        self.btn_login.setText(_translate("VkMessenger", "Log in"))
        self.btn_start.setText(_translate("VkMessenger", "Start"))
        self.btn_stop.setText(_translate("VkMessenger", "Stop"))

