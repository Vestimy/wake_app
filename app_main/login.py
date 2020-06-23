# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/vestimy/WakePark/Style/login.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Login_Form(object):
    def setupUi(self, Login_Form):
        Login_Form.setObjectName("Login_Form")
        Login_Form.resize(640, 420)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Login_Form.sizePolicy().hasHeightForWidth())
        Login_Form.setSizePolicy(sizePolicy)
        Login_Form.setMinimumSize(QtCore.QSize(640, 420))
        Login_Form.setMaximumSize(QtCore.QSize(640, 420))
        icon = QtGui.QIcon.fromTheme(":/icons/wakeboarding.png")
        Login_Form.setWindowIcon(icon)
        Login_Form.setStyleSheet("#Login_Form { \n"
"    background: rgba(32, 80, 96, 100); }\n"
"#topPanel { \n"
"    background-color: qlineargradient(spread:reflect, x1:0.5, y1:0, x2:0, y2:0, stop:0 rgba(91, 204, 233, 100), stop:1 rgba(32, 80, 96, 100)); \n"
"}\n"
"#loginForm\n"
"{\n"
"  background: rgba(0, 0, 0, 80);\n"
"  border-radius: 8px;\n"
"}\n"
"QLabel { \n"
"    color: white; }\n"
"QLineEdit { \n"
"    border-radius: 3px; }\n"
"\n"
"QPushButton\n"
"{\n"
"  color: white;\n"
"  background-color: #27a9e3;\n"
"\n"
"  background-color: qlineargradient(spread:pad, x1:0.469, y1:0, x2:0.503, y2:1, stop:0 rgba(39, 169, 227, 255), stop:1 rgba(51, 93, 112, 255));\n"
"  border-width: 0px;\n"
"  border-radius: 3px;\n"
"}:active\n"
"\n"
"QPushButton:hover { \n"
"background-color: #66c011; \n"
"background-color:qlineargradient(spread:reflect, x1:0.478, y1:0, x2:0.472, y2:1, stop:0 rgba(51, 93, 112, 255), stop:0.99435 rgba(39, 169, 227, 255)); \n"
"}\n"
"")
        Login_Form.setSizeGripEnabled(False)
        self.verticalLayout = QtWidgets.QVBoxLayout(Login_Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.topPanel = QtWidgets.QWidget(Login_Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.topPanel.sizePolicy().hasHeightForWidth())
        self.topPanel.setSizePolicy(sizePolicy)
        self.topPanel.setMinimumSize(QtCore.QSize(0, 45))
        self.topPanel.setObjectName("topPanel")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.topPanel)
        self.horizontalLayout.setContentsMargins(6, 5, 6, 5)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.currentDateTime = QtWidgets.QLabel(self.topPanel)
        self.currentDateTime.setObjectName("currentDateTime")
        self.horizontalLayout.addWidget(self.currentDateTime)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.restartButton = QtWidgets.QPushButton(self.topPanel)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.restartButton.sizePolicy().hasHeightForWidth())
        self.restartButton.setSizePolicy(sizePolicy)
        self.restartButton.setMinimumSize(QtCore.QSize(40, 40))
        self.restartButton.setText("")
        self.restartButton.setObjectName("restartButton")
        self.horizontalLayout.addWidget(self.restartButton)
        self.shutdownButton = QtWidgets.QPushButton(self.topPanel)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.shutdownButton.sizePolicy().hasHeightForWidth())
        self.shutdownButton.setSizePolicy(sizePolicy)
        self.shutdownButton.setMinimumSize(QtCore.QSize(40, 40))
        self.shutdownButton.setText("")
        self.shutdownButton.setObjectName("shutdownButton")
        self.horizontalLayout.addWidget(self.shutdownButton)
        self.verticalLayout.addWidget(self.topPanel)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(-1, 5, -1, 5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalWidget = QtWidgets.QWidget(Login_Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalWidget.sizePolicy().hasHeightForWidth())
        self.horizontalWidget.setSizePolicy(sizePolicy)
        self.horizontalWidget.setMinimumSize(QtCore.QSize(399, 152))
        self.horizontalWidget.setStyleSheet("\n"
"border-image: url(:/images/in_bott.jpg);\n"
"border-radius:55px;")
        self.horizontalWidget.setObjectName("horizontalWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalWidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2.addWidget(self.horizontalWidget, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.loginForm = QtWidgets.QWidget(Login_Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loginForm.sizePolicy().hasHeightForWidth())
        self.loginForm.setSizePolicy(sizePolicy)
        self.loginForm.setMinimumSize(QtCore.QSize(350, 180))
        self.loginForm.setStyleSheet("#loginForm { border: 1px solid; }")
        self.loginForm.setObjectName("loginForm")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.loginForm)
        self.verticalLayout_3.setContentsMargins(35, 35, 35, 35)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(20, 15, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_3.addItem(spacerItem1)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lineEdit_Pass = QtWidgets.QLineEdit(self.loginForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_Pass.sizePolicy().hasHeightForWidth())
        self.lineEdit_Pass.setSizePolicy(sizePolicy)
        self.lineEdit_Pass.setMinimumSize(QtCore.QSize(280, 25))
        self.lineEdit_Pass.setInputMask("")
        self.lineEdit_Pass.setMaxLength(32767)
        self.lineEdit_Pass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_Pass.setObjectName("lineEdit_Pass")
        self.verticalLayout_4.addWidget(self.lineEdit_Pass)
        self.verticalLayout_3.addLayout(self.verticalLayout_4)
        self.pushButtonLogin = QtWidgets.QPushButton(self.loginForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonLogin.sizePolicy().hasHeightForWidth())
        self.pushButtonLogin.setSizePolicy(sizePolicy)
        self.pushButtonLogin.setMinimumSize(QtCore.QSize(280, 25))
        self.pushButtonLogin.setObjectName("pushButtonLogin")
        self.verticalLayout_3.addWidget(self.pushButtonLogin)
        spacerItem2 = QtWidgets.QSpacerItem(20, 15, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_3.addItem(spacerItem2)
        self.horizontalLayout_3.addWidget(self.loginForm)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.lcheck = QtWidgets.QLabel(Login_Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lcheck.sizePolicy().hasHeightForWidth())
        self.lcheck.setSizePolicy(sizePolicy)
        self.lcheck.setMinimumSize(QtCore.QSize(0, 10))
        self.lcheck.setText("")
        self.lcheck.setObjectName("lcheck")
        self.horizontalLayout_4.addWidget(self.lcheck)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(Login_Form)
        self.shutdownButton.clicked.connect(Login_Form.close)
        QtCore.QMetaObject.connectSlotsByName(Login_Form)
        Login_Form.setTabOrder(self.lineEdit_Pass, self.pushButtonLogin)
        Login_Form.setTabOrder(self.pushButtonLogin, self.restartButton)
        Login_Form.setTabOrder(self.restartButton, self.shutdownButton)

    def retranslateUi(self, Login_Form):
        _translate = QtCore.QCoreApplication.translate
        Login_Form.setWindowTitle(_translate("Login_Form", "FreeWake"))
        self.currentDateTime.setText(_translate("Login_Form", "Monday, 25-10-2015 3:14 PM"))
        self.lineEdit_Pass.setPlaceholderText(_translate("Login_Form", "Введите пароль"))
        self.pushButtonLogin.setText(_translate("Login_Form", "ВОЙТИ"))
        self.pushButtonLogin.setShortcut(_translate("Login_Form", "Return"))
import source_rc
