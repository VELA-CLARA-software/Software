# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_magnetAppStartup.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_magnetAppStartup(object):
    def setupUi(self, magnetAppStartup):
        magnetAppStartup.setObjectName("magnetAppStartup")
        magnetAppStartup.resize(1014, 734)
        self.centralwidget = QtWidgets.QWidget(magnetAppStartup)
        self.centralwidget.setObjectName("centralwidget")
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(370, 440, 111, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.startButton.setFont(font)
        self.startButton.setObjectName("startButton")
        self.cancelButton = QtWidgets.QPushButton(self.centralwidget)
        self.cancelButton.setGeometry(QtCore.QRect(500, 440, 151, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.cancelButton.setFont(font)
        self.cancelButton.setObjectName("cancelButton")
        self.machineAreaSelection = QtWidgets.QGroupBox(self.centralwidget)
        self.machineAreaSelection.setGeometry(QtCore.QRect(320, 140, 231, 241))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.machineAreaSelection.setFont(font)
        self.machineAreaSelection.setAlignment(QtCore.Qt.AlignCenter)
        self.machineAreaSelection.setObjectName("machineAreaSelection")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.machineAreaSelection)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.VELA_INJ = QtWidgets.QRadioButton(self.machineAreaSelection)
        self.VELA_INJ.setObjectName("VELA_INJ")
        self.verticalLayout_3.addWidget(self.VELA_INJ)
        self.CLARA_2_BA1_BA2 = QtWidgets.QRadioButton(self.machineAreaSelection)
        self.CLARA_2_BA1_BA2.setObjectName("CLARA_2_BA1_BA2")
        self.verticalLayout_3.addWidget(self.CLARA_2_BA1_BA2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.CLARA_2_BA1_BA2.raise_()
        self.VELA_INJ.raise_()
        self.modeSelection = QtWidgets.QGroupBox(self.centralwidget)
        self.modeSelection.setGeometry(QtCore.QRect(580, 140, 301, 211))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.modeSelection.setFont(font)
        self.modeSelection.setObjectName("modeSelection")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.modeSelection)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.offlineMode = QtWidgets.QRadioButton(self.modeSelection)
        self.offlineMode.setObjectName("offlineMode")
        self.machineModeButtons = QtWidgets.QButtonGroup(magnetAppStartup)
        self.machineModeButtons.setObjectName("machineModeButtons")
        self.machineModeButtons.addButton(self.offlineMode)
        self.verticalLayout_2.addWidget(self.offlineMode)
        self.virtualMode = QtWidgets.QRadioButton(self.modeSelection)
        self.virtualMode.setObjectName("virtualMode")
        self.machineModeButtons.addButton(self.virtualMode)
        self.verticalLayout_2.addWidget(self.virtualMode)
        self.physicalMode = QtWidgets.QRadioButton(self.modeSelection)
        self.physicalMode.setObjectName("physicalMode")
        self.machineModeButtons.addButton(self.physicalMode)
        self.verticalLayout_2.addWidget(self.physicalMode)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.instructionLabel = QtWidgets.QLabel(self.centralwidget)
        self.instructionLabel.setGeometry(QtCore.QRect(350, 50, 611, 71))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.instructionLabel.setFont(font)
        self.instructionLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.instructionLabel.setObjectName("instructionLabel")
        self.iconLabel = QtWidgets.QLabel(self.centralwidget)
        self.iconLabel.setGeometry(QtCore.QRect(30, 100, 221, 261))
        self.iconLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.iconLabel.setObjectName("iconLabel")
        self.waitMessageLabel = QtWidgets.QLabel(self.centralwidget)
        self.waitMessageLabel.setGeometry(QtCore.QRect(100, 460, 491, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.waitMessageLabel.setFont(font)
        self.waitMessageLabel.setObjectName("waitMessageLabel")
        self.logoLabel = QtWidgets.QLabel(self.centralwidget)
        self.logoLabel.setGeometry(QtCore.QRect(30, 550, 951, 111))
        self.logoLabel.setObjectName("logoLabel")
        magnetAppStartup.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(magnetAppStartup)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1014, 21))
        self.menubar.setObjectName("menubar")
        magnetAppStartup.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(magnetAppStartup)
        self.statusbar.setObjectName("statusbar")
        magnetAppStartup.setStatusBar(self.statusbar)

        self.retranslateUi(magnetAppStartup)
        QtCore.QMetaObject.connectSlotsByName(magnetAppStartup)

    def retranslateUi(self, magnetAppStartup):
        _translate = QtCore.QCoreApplication.translate
        magnetAppStartup.setWindowTitle(_translate("magnetAppStartup", "MainWindow"))
        self.startButton.setText(_translate("magnetAppStartup", "START"))
        self.cancelButton.setText(_translate("magnetAppStartup", "CANCEL"))
        self.machineAreaSelection.setTitle(_translate("magnetAppStartup", "Machine Area"))
        self.VELA_INJ.setText(_translate("magnetAppStartup", "VELA INJECTOR"))
        self.CLARA_2_BA1_BA2.setText(_translate("magnetAppStartup", "CLARA 2 BA1 and BA2"))
        self.modeSelection.setTitle(_translate("magnetAppStartup", "Mode Selection"))
        self.offlineMode.setText(_translate("magnetAppStartup", "Offline   (No EPICS)"))
        self.virtualMode.setText(_translate("magnetAppStartup", "Virtual   (Connect to Virtual Machine)"))
        self.physicalMode.setText(_translate("magnetAppStartup", "Physical (Connect to Real Machine)"))
        self.instructionLabel.setText(_translate("magnetAppStartup", "Welcome to the VELA-CLARA Magnet Application \n"
"Please Choose a Machine Area and an Operating Mode \n"
"Then Press START "))
        self.iconLabel.setText(_translate("magnetAppStartup", "Icon Label "))
        self.waitMessageLabel.setText(_translate("magnetAppStartup", "placeholder"))
        self.logoLabel.setText(_translate("magnetAppStartup", "TextLabel"))