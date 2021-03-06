# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './Scripts/UI_Files/TeacherWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(817, 590)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.list_clients = QtWidgets.QListView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.list_clients.sizePolicy().hasHeightForWidth())
        self.list_clients.setSizePolicy(sizePolicy)
        self.list_clients.setObjectName("list_clients")
        self.gridLayout.addWidget(self.list_clients, 0, 0, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout)
        self.infromationbox = QtWidgets.QVBoxLayout()
        self.infromationbox.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.infromationbox.setSpacing(0)
        self.infromationbox.setObjectName("infromationbox")
        self.layout_totalScore = QtWidgets.QVBoxLayout()
        self.layout_totalScore.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.layout_totalScore.setSpacing(0)
        self.layout_totalScore.setObjectName("layout_totalScore")
        self.infromationbox.addLayout(self.layout_totalScore)
        self.operationWidget = QtWidgets.QHBoxLayout()
        self.operationWidget.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.operationWidget.setObjectName("operationWidget")
        self.widge_checkboxSetting = QtWidgets.QVBoxLayout()
        self.widge_checkboxSetting.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.widge_checkboxSetting.setObjectName("widge_checkboxSetting")
        self.check_setting1 = QtWidgets.QCheckBox(self.centralwidget)
        self.check_setting1.setObjectName("check_setting1")
        self.widge_checkboxSetting.addWidget(self.check_setting1)
        self.check_setting2 = QtWidgets.QCheckBox(self.centralwidget)
        self.check_setting2.setObjectName("check_setting2")
        self.widge_checkboxSetting.addWidget(self.check_setting2)
        self.check_setting3 = QtWidgets.QCheckBox(self.centralwidget)
        self.check_setting3.setObjectName("check_setting3")
        self.widge_checkboxSetting.addWidget(self.check_setting3)
        self.check_setting4 = QtWidgets.QCheckBox(self.centralwidget)
        self.check_setting4.setObjectName("check_setting4")
        self.widge_checkboxSetting.addWidget(self.check_setting4)
        self.operationWidget.addLayout(self.widge_checkboxSetting)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.text_currentScore = QtWidgets.QTextBrowser(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text_currentScore.sizePolicy().hasHeightForWidth())
        self.text_currentScore.setSizePolicy(sizePolicy)
        self.text_currentScore.setObjectName("text_currentScore")
        self.verticalLayout.addWidget(self.text_currentScore)
        self.operationWidget.addLayout(self.verticalLayout)
        self.widge_buttoms = QtWidgets.QVBoxLayout()
        self.widge_buttoms.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.widge_buttoms.setContentsMargins(-1, 20, -1, 20)
        self.widge_buttoms.setObjectName("widge_buttoms")
        self.btn_start = QtWidgets.QPushButton(self.centralwidget)
        self.btn_start.setObjectName("btn_start")
        self.widge_buttoms.addWidget(self.btn_start)
        self.btn_pause = QtWidgets.QPushButton(self.centralwidget)
        self.btn_pause.setObjectName("btn_pause")
        self.widge_buttoms.addWidget(self.btn_pause)
        self.btn_link = QtWidgets.QPushButton(self.centralwidget)
        self.btn_link.setObjectName("btn_link")
        self.widge_buttoms.addWidget(self.btn_link)
        self.btn_settings = QtWidgets.QPushButton(self.centralwidget)
        self.btn_settings.setObjectName("btn_settings")
        self.widge_buttoms.addWidget(self.btn_settings)
        self.operationWidget.addLayout(self.widge_buttoms)
        self.operationWidget.setStretch(0, 1)
        self.operationWidget.setStretch(1, 1)
        self.operationWidget.setStretch(2, 1)
        self.infromationbox.addLayout(self.operationWidget)
        self.horizontalLayout_2.addLayout(self.infromationbox)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.check_setting1.setText(_translate("MainWindow", "setting1"))
        self.check_setting2.setText(_translate("MainWindow", "setting2"))
        self.check_setting3.setText(_translate("MainWindow", "setting3"))
        self.check_setting4.setText(_translate("MainWindow", "setting4"))
        self.btn_start.setText(_translate("MainWindow", "Start"))
        self.btn_pause.setText(_translate("MainWindow", "Pause"))
        self.btn_link.setText(_translate("MainWindow", "Link"))
        self.btn_settings.setText(_translate("MainWindow", "Settings"))
