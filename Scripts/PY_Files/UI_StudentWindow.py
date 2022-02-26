# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './Scripts/UI_Files/StudentWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(392, 437)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 20, 361, 331))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.infoWidget = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.infoWidget.setContentsMargins(0, 0, 0, 0)
        self.infoWidget.setSpacing(2)
        self.infoWidget.setObjectName("infoWidget")
        self.videoWidget = QtWidgets.QHBoxLayout()
        self.videoWidget.setObjectName("videoWidget")
        self.lbl_camOut = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_camOut.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_camOut.setObjectName("lbl_camOut")
        self.videoWidget.addWidget(self.lbl_camOut)
        self.infoWidget.addLayout(self.videoWidget)
        self.buttomWidget = QtWidgets.QHBoxLayout()
        self.buttomWidget.setContentsMargins(20, -1, 20, -1)
        self.buttomWidget.setObjectName("buttomWidget")
        self.btn_open = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_open.setObjectName("btn_open")
        self.buttomWidget.addWidget(self.btn_open)
        self.btn_stop = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_stop.setObjectName("btn_stop")
        self.buttomWidget.addWidget(self.btn_stop)
        self.btn_connect = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_connect.setObjectName("btn_connect")
        self.buttomWidget.addWidget(self.btn_connect)
        self.infoWidget.addLayout(self.buttomWidget)
        self.infoWidget.setStretch(0, 4)
        self.infoWidget.setStretch(1, 1)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(19, 360, 361, 61))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.debugWidget = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.debugWidget.setContentsMargins(0, 0, 0, 0)
        self.debugWidget.setObjectName("debugWidget")
        self.lbl_Status = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.lbl_Status.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_Status.setObjectName("lbl_Status")
        self.debugWidget.addWidget(self.lbl_Status)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lbl_camOut.setText(_translate("MainWindow", "Wait For Image, Click \"Start\""))
        self.btn_open.setText(_translate("MainWindow", "Start"))
        self.btn_stop.setText(_translate("MainWindow", "Stop"))
        self.btn_connect.setText(_translate("MainWindow", "Connect"))
        self.lbl_Status.setText(_translate("MainWindow", "Wait For Score..."))
