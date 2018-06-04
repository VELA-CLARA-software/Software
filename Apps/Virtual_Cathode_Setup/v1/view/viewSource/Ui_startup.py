# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_startup.ui'
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

class Ui_magnetAppStartup(object):
    def setupUi(self, magnetAppStartup):
        magnetAppStartup.setObjectName(_fromUtf8("magnetAppStartup"))
        magnetAppStartup.resize(779, 624)
        self.centralwidget = QtGui.QWidget(magnetAppStartup)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.startButton = QtGui.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(350, 430, 111, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.startButton.setFont(font)
        self.startButton.setObjectName(_fromUtf8("startButton"))
        self.cancelButton = QtGui.QPushButton(self.centralwidget)
        self.cancelButton.setGeometry(QtCore.QRect(480, 430, 151, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.cancelButton.setFont(font)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.modeSelection = QtGui.QGroupBox(self.centralwidget)
        self.modeSelection.setGeometry(QtCore.QRect(340, 170, 301, 211))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.modeSelection.setFont(font)
        self.modeSelection.setObjectName(_fromUtf8("modeSelection"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.modeSelection)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.offlineMode = QtGui.QRadioButton(self.modeSelection)
        self.offlineMode.setObjectName(_fromUtf8("offlineMode"))
        self.machineModeButtons = QtGui.QButtonGroup(magnetAppStartup)
        self.machineModeButtons.setObjectName(_fromUtf8("machineModeButtons"))
        self.machineModeButtons.addButton(self.offlineMode)
        self.verticalLayout_2.addWidget(self.offlineMode)
        self.virtualMode = QtGui.QRadioButton(self.modeSelection)
        self.virtualMode.setObjectName(_fromUtf8("virtualMode"))
        self.machineModeButtons.addButton(self.virtualMode)
        self.verticalLayout_2.addWidget(self.virtualMode)
        self.physicalMode = QtGui.QRadioButton(self.modeSelection)
        self.physicalMode.setObjectName(_fromUtf8("physicalMode"))
        self.machineModeButtons.addButton(self.physicalMode)
        self.verticalLayout_2.addWidget(self.physicalMode)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.instructionLabel = QtGui.QLabel(self.centralwidget)
        self.instructionLabel.setGeometry(QtCore.QRect(350, 50, 221, 71))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.instructionLabel.setFont(font)
        self.instructionLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.instructionLabel.setObjectName(_fromUtf8("instructionLabel"))
        self.iconLabel = QtGui.QLabel(self.centralwidget)
        self.iconLabel.setGeometry(QtCore.QRect(30, 100, 221, 261))
        self.iconLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.iconLabel.setObjectName(_fromUtf8("iconLabel"))
        self.waitMessageLabel = QtGui.QLabel(self.centralwidget)
        self.waitMessageLabel.setGeometry(QtCore.QRect(100, 460, 491, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.waitMessageLabel.setFont(font)
        self.waitMessageLabel.setObjectName(_fromUtf8("waitMessageLabel"))
        self.logoLabel = QtGui.QLabel(self.centralwidget)
        self.logoLabel.setGeometry(QtCore.QRect(260, 490, 571, 21))
        self.logoLabel.setObjectName(_fromUtf8("logoLabel"))
        magnetAppStartup.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(magnetAppStartup)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 779, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        magnetAppStartup.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(magnetAppStartup)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        magnetAppStartup.setStatusBar(self.statusbar)

        self.retranslateUi(magnetAppStartup)
        QtCore.QMetaObject.connectSlotsByName(magnetAppStartup)

    def retranslateUi(self, magnetAppStartup):
        magnetAppStartup.setWindowTitle(_translate("magnetAppStartup", "MainWindow", None))
        self.startButton.setText(_translate("magnetAppStartup", "START", None))
        self.cancelButton.setText(_translate("magnetAppStartup", "CANCEL", None))
        self.modeSelection.setTitle(_translate("magnetAppStartup", "Mode Selection", None))
        self.offlineMode.setText(_translate("magnetAppStartup", "Offline   (No EPICS)", None))
        self.virtualMode.setText(_translate("magnetAppStartup", "Virtual   (Connect to Virtual Machine)", None))
        self.physicalMode.setText(_translate("magnetAppStartup", "Physical (Connect to Real Machine)", None))
        self.instructionLabel.setText(_translate("magnetAppStartup", "Virtual Cathode Set-up ", None))
        self.iconLabel.setText(_translate("magnetAppStartup", "Icon Label ", None))
        self.waitMessageLabel.setText(_translate("magnetAppStartup", "placeholder", None))
        self.logoLabel.setText(_translate("magnetAppStartup", "TextLabel", None))
