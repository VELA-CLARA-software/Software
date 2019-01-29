# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_view.ui'
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

class Ui_CamState(object):
    def setupUi(self, CamState):
        CamState.setObjectName(_fromUtf8("CamState"))
        CamState.resize(211, 435)
        self.centralwidget = QtGui.QWidget(CamState)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.stopButton = QtGui.QPushButton(self.widget)
        self.stopButton.setMinimumSize(QtCore.QSize(100, 25))
        self.stopButton.setObjectName(_fromUtf8("stopButton"))
        self.verticalLayout_2.addWidget(self.stopButton)
        self.groupBox = QtGui.QGroupBox(self.widget)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_2.addWidget(self.groupBox)
        self.verticalLayout.addWidget(self.widget)
        CamState.setCentralWidget(self.centralwidget)

        self.retranslateUi(CamState)
        QtCore.QMetaObject.connectSlotsByName(CamState)

    def retranslateUi(self, CamState):
        CamState.setWindowTitle(_translate("CamState", "Screen State", None))
        self.stopButton.setText(_translate("CamState", "ALL OUT", None))
        self.groupBox.setTitle(_translate("CamState", "Screen", None))

