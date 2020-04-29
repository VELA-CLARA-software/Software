# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fb_radio.ui'
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
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(40, 40, 371, 71))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.allMagnets = QtGui.QRadioButton(self.groupBox)
        self.allMagnets.setObjectName(_fromUtf8("allMagnets"))
        self.horizontalLayout.addWidget(self.allMagnets)
        self.quadMagnets = QtGui.QRadioButton(self.groupBox)
        self.quadMagnets.setObjectName(_fromUtf8("quadMagnets"))
        self.horizontalLayout.addWidget(self.quadMagnets)
        self.corrMagnets = QtGui.QRadioButton(self.groupBox)
        self.corrMagnets.setObjectName(_fromUtf8("corrMagnets"))
        self.horizontalLayout.addWidget(self.corrMagnets)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.groupBox.setTitle(_translate("MainWindow", "Which Magnets To Apply File To ", None))
        self.allMagnets.setText(_translate("MainWindow", "All", None))
        self.quadMagnets.setText(_translate("MainWindow", "Quads ", None))
        self.corrMagnets.setText(_translate("MainWindow", "Correctors", None))

