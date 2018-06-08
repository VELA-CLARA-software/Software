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

class Ui_view(object):
    def setupUi(self, view):
        view.setObjectName(_fromUtf8("view"))
        view.resize(211, 347)
        self.centralwidget = QtGui.QWidget(view)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(20, 0, 181, 282))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.closeButton = QtGui.QPushButton(self.widget)
        self.closeButton.setMinimumSize(QtCore.QSize(100, 25))
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.verticalLayout_2.addWidget(self.closeButton)
        self.openButton = QtGui.QPushButton(self.widget)
        self.openButton.setMinimumSize(QtCore.QSize(100, 25))
        self.openButton.setObjectName(_fromUtf8("openButton"))
        self.verticalLayout_2.addWidget(self.openButton)
        self.groupBox = QtGui.QGroupBox(self.widget)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_2.addWidget(self.groupBox)
        view.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(view)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        view.setStatusBar(self.statusbar)

        self.retranslateUi(view)
        QtCore.QMetaObject.connectSlotsByName(view)

    def retranslateUi(self, view):
        view.setWindowTitle(_translate("view", "MainWindow", None))
        self.closeButton.setText(_translate("view", "CLOSE ALL", None))
        self.openButton.setText(_translate("view", "OPEN ALL", None))
        self.groupBox.setTitle(_translate("view", "Valves", None))

