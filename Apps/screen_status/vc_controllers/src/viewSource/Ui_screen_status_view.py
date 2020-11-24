# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_screen_status_view.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_screen_status_view(object):
    def setupUi(self, screen_status_view):
        screen_status_view.setObjectName(_fromUtf8("screen_status_view"))
        screen_status_view.resize(214, 332)
        self.centralwidget = QtGui.QWidget(screen_status_view)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.allout_Button = QtGui.QPushButton(self.widget)
        self.allout_Button.setMinimumSize(QtCore.QSize(100, 25))
        self.allout_Button.setObjectName(_fromUtf8("allout_Button"))
        self.verticalLayout_2.addWidget(self.allout_Button)
        self.checkDevices_Button = QtGui.QPushButton(self.widget)
        self.checkDevices_Button.setObjectName(_fromUtf8("checkDevices_Button"))
        self.verticalLayout_2.addWidget(self.checkDevices_Button)
        self.clara_led_button = QtGui.QPushButton(self.widget)
        self.clara_led_button.setObjectName(_fromUtf8("clara_led_button"))
        self.verticalLayout_2.addWidget(self.clara_led_button)
        self.vela_led_button = QtGui.QPushButton(self.widget)
        self.vela_led_button.setObjectName(_fromUtf8("vela_led_button"))
        self.verticalLayout_2.addWidget(self.vela_led_button)
        self.groupBox = QtGui.QGroupBox(self.widget)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_2.addWidget(self.groupBox)
        self.verticalLayout.addWidget(self.widget)
        screen_status_view.setCentralWidget(self.centralwidget)

        self.retranslateUi(screen_status_view)
        QtCore.QMetaObject.connectSlotsByName(screen_status_view)

    def retranslateUi(self, screen_status_view):
        screen_status_view.setWindowTitle(_translate("screen_status_view", "Screen State", None))
        self.allout_Button.setText(_translate("screen_status_view", "ALL OUT", None))
        self.checkDevices_Button.setText(_translate("screen_status_view", "Check Devices", None))
        self.clara_led_button.setText(_translate("screen_status_view", "CLARA- LED", None))
        self.vela_led_button.setText(_translate("screen_status_view", "VELA-LED", None))
        self.groupBox.setTitle(_translate("screen_status_view", "Screen", None))

