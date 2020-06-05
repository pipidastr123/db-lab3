# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connection.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class ConnectionMainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(524, 237)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.confirmationButtons = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.confirmationButtons.setGeometry(QtCore.QRect(170, 140, 174, 32))
        self.confirmationButtons.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.confirmationButtons.setCenterButtons(False)
        self.confirmationButtons.setObjectName("confirmationButtons")
        self.chooseFileButton = QtWidgets.QPushButton(self.centralwidget)
        self.chooseFileButton.setGeometry(QtCore.QRect(420, 33, 71, 32))
        self.chooseFileButton.setObjectName("chooseFileButton")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(20, 30, 399, 81))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.hostTF = QtWidgets.QLineEdit(self.widget)
        self.hostTF.setObjectName("hostTF")
        self.horizontalLayout.addWidget(self.hostTF)
        self.dbNameTF = QtWidgets.QLineEdit(self.widget)
        self.dbNameTF.setText("")
        self.dbNameTF.setObjectName("dbNameTF")
        self.horizontalLayout.addWidget(self.dbNameTF)
        self.fileTF = QtWidgets.QLineEdit(self.widget)
        self.fileTF.setObjectName("fileTF")
        self.horizontalLayout.addWidget(self.fileTF)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.portTF = QtWidgets.QLineEdit(self.widget)
        self.portTF.setObjectName("portTF")
        self.horizontalLayout_2.addWidget(self.portTF)
        self.loginTF = QtWidgets.QLineEdit(self.widget)
        self.loginTF.setText("")
        self.loginTF.setObjectName("loginTF")
        self.horizontalLayout_2.addWidget(self.loginTF)
        self.passwordTF = QtWidgets.QLineEdit(self.widget)
        self.passwordTF.setObjectName("passwordTF")
        self.horizontalLayout_2.addWidget(self.passwordTF)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 524, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.chooseFileButton.setText(_translate("MainWindow", "Choose"))
        self.hostTF.setPlaceholderText(_translate("MainWindow", " Host"))
        self.dbNameTF.setPlaceholderText(_translate("MainWindow", "Database\' name"))
        self.fileTF.setPlaceholderText(_translate("MainWindow", "SQL source file"))
        self.portTF.setPlaceholderText(_translate("MainWindow", " Port"))
        self.loginTF.setPlaceholderText(_translate("MainWindow", "Login"))
        self.passwordTF.setPlaceholderText(_translate("MainWindow", "Password"))
