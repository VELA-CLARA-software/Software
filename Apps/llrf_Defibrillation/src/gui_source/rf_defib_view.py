# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rf_defib_view.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(193, 74)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gun_check_box = QtGui.QCheckBox(self.centralwidget)
        self.gun_check_box.setMaximumSize(QtCore.QSize(100, 16777215))
        self.gun_check_box.setObjectName(_fromUtf8("gun_check_box"))
        self.verticalLayout.addWidget(self.gun_check_box)
        self.linac_check_box = QtGui.QCheckBox(self.centralwidget)
        self.linac_check_box.setMaximumSize(QtCore.QSize(100, 16777215))
        self.linac_check_box.setObjectName(_fromUtf8("linac_check_box"))
        self.verticalLayout.addWidget(self.linac_check_box)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gun_value = QtGui.QPushButton(self.centralwidget)
        self.gun_value.setMaximumSize(QtCore.QSize(25, 16777215))
        self.gun_value.setText(_fromUtf8(""))
        self.gun_value.setObjectName(_fromUtf8("gun_value"))
        self.verticalLayout_2.addWidget(self.gun_value)
        self.linac_value = QtGui.QPushButton(self.centralwidget)
        self.linac_value.setMaximumSize(QtCore.QSize(25, 16777215))
        self.linac_value.setText(_fromUtf8(""))
        self.linac_value.setObjectName(_fromUtf8("linac_value"))
        self.verticalLayout_2.addWidget(self.linac_value)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.gun_is_keeping_alive = QtGui.QCheckBox(self.centralwidget)
        self.gun_is_keeping_alive.setText(_fromUtf8(""))
        self.gun_is_keeping_alive.setObjectName(_fromUtf8("gun_is_keeping_alive"))
        self.verticalLayout_3.addWidget(self.gun_is_keeping_alive)
        self.linac_is_keeping_alive = QtGui.QCheckBox(self.centralwidget)
        self.linac_is_keeping_alive.setText(_fromUtf8(""))
        self.linac_is_keeping_alive.setObjectName(_fromUtf8("linac_is_keeping_alive"))
        self.verticalLayout_3.addWidget(self.linac_is_keeping_alive)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.gun_check_box.setText(_translate("MainWindow", "Gun HeartBeat", None))
        self.linac_check_box.setText(_translate("MainWindow", "Linac HeartBeat", None))

