# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled1.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import pyqtgraph, qrangeslider

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

class Ui_TabWidget(object):
    def setupUi(self, TabWidget):
        self.TabWidget = TabWidget
        self.TabWidget.setObjectName(_fromUtf8("TabWidget"))
        self.TabWidget.resize(699, 602)
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.launchATTButton = QtGui.QPushButton(self.tab)
        self.launchATTButton.setGeometry(QtCore.QRect(460, 60, 151, 41))
        self.launchATTButton.setObjectName(_fromUtf8("launchATTButton"))
        self.launchDLYButton = QtGui.QPushButton(self.tab)
        self.launchDLYButton.setGeometry(QtCore.QRect(460, 120, 151, 41))
        self.launchDLYButton.setObjectName(_fromUtf8("launchDLYButton"))
        self.launchTrajButton = QtGui.QPushButton(self.tab)
        self.launchTrajButton.setGeometry(QtCore.QRect(460, 180, 151, 41))
        self.launchTrajButton.setObjectName(_fromUtf8("launchTrajButton"))
        self.launchMonButton = QtGui.QPushButton(self.tab)
        self.launchMonButton.setGeometry(QtCore.QRect(460, 240, 151, 41))
        self.launchMonButton.setObjectName(_fromUtf8("launchMonButton"))
        self.beamlineButton = QtGui.QGroupBox(self.tab)
        self.beamlineButton.setGeometry(QtCore.QRect(308, 50, 131, 212))
        self.beamlineButton.setObjectName(_fromUtf8("beamlineButton"))
        self.velaINJButton = QtGui.QRadioButton(self.beamlineButton)
        self.velaINJButton.setGeometry(QtCore.QRect(308, 20, 131, 32))
        self.velaINJButton.setObjectName(_fromUtf8("velaINJButton"))
        self.velaBA1Button = QtGui.QRadioButton(self.beamlineButton)
        self.velaBA1Button.setGeometry(QtCore.QRect(308, 60, 131, 32))
        self.velaBA1Button.setObjectName(_fromUtf8("velaBA1Button"))
        self.velaBA2Button = QtGui.QRadioButton(self.beamlineButton)
        self.velaBA2Button.setGeometry(QtCore.QRect(308, 100, 131, 32))
        self.velaBA2Button.setObjectName(_fromUtf8("velaBA2Button"))
        self.claraButton = QtGui.QRadioButton(self.beamlineButton)
        self.claraButton.setGeometry(QtCore.QRect(308, 140, 131, 52))
        self.claraButton.setObjectName(_fromUtf8("claraButton"))
        self.c2vButton = QtGui.QRadioButton(self.beamlineButton)
        self.c2vButton.setGeometry(QtCore.QRect(308, 180, 131, 52))
        self.c2vButton.setObjectName(_fromUtf8("c2vButton"))
        self.radioButtonVBoxLayout = QtGui.QVBoxLayout(self.tab)
        self.radioButtonVBoxLayout.setGeometry(QtCore.QRect(308, 10, 231, 112))
        self.radioButtonVBoxLayout.setObjectName(_fromUtf8("radioButtonVBoxLayout"))
        self.velaINJButton.setAutoExclusive(True)
        self.velaINJButton.setCheckable(True)
        self.velaBA1Button.setAutoExclusive(True)
        self.velaBA1Button.setCheckable(True)
        self.velaBA2Button.setAutoExclusive(True)
        self.velaBA2Button.setCheckable(True)
        self.claraButton.setAutoExclusive(True)
        self.claraButton.setCheckable(True)
        self.c2vButton.setAutoExclusive(True)
        self.c2vButton.setCheckable(True)
        self.radioButtonVBoxLayout.addWidget(self.velaINJButton)
        self.radioButtonVBoxLayout.addWidget(self.velaBA1Button)
        self.radioButtonVBoxLayout.addWidget(self.velaBA2Button)
        self.radioButtonVBoxLayout.addWidget(self.claraButton)
        self.radioButtonVBoxLayout.addWidget(self.c2vButton)
        self.beamlineButton.setLayout(self.radioButtonVBoxLayout)
        self.velaINJButton.setChecked(True)
        self.matrixButton = QtGui.QGroupBox(self.tab)
        self.matrixButton.setGeometry(QtCore.QRect(308, 350, 131, 112))
        self.matrixButton.setObjectName(_fromUtf8("matrixButton"))
        self.controllerTypeVBoxLayout = QtGui.QVBoxLayout(self.tab)
        self.controllerTypeVBoxLayout.setGeometry(QtCore.QRect(308, 360, 231, 112))
        self.controllerTypeVBoxLayout.setObjectName(_fromUtf8("controllerTypeVBoxLayout"))
        self.physicalButton = QtGui.QRadioButton(self.matrixButton)
        self.physicalButton.setGeometry(QtCore.QRect(308, 380, 131, 32))
        self.physicalButton.setObjectName(_fromUtf8("physicalButton"))
        self.virtualButton = QtGui.QRadioButton(self.matrixButton)
        self.virtualButton.setGeometry(QtCore.QRect(308, 420, 131, 32))
        self.virtualButton.setObjectName(_fromUtf8("virtualButton"))
        self.offlineButton = QtGui.QRadioButton(self.matrixButton)
        self.offlineButton.setGeometry(QtCore.QRect(308, 460, 131, 32))
        self.offlineButton.setObjectName(_fromUtf8("offlineButton"))
        self.controllerTypeVBoxLayout.addWidget(self.physicalButton)
        self.controllerTypeVBoxLayout.addWidget(self.virtualButton)
        self.controllerTypeVBoxLayout.addWidget(self.offlineButton)
        self.matrixButton.setLayout(self.controllerTypeVBoxLayout)
        self.physicalButton.setAutoExclusive(True)
        self.physicalButton.setCheckable(True)
        self.virtualButton.setAutoExclusive(True)
        self.virtualButton.setCheckable(True)
        self.offlineButton.setAutoExclusive(True)
        self.offlineButton.setCheckable(True)
        self.virtualButton.setChecked(True)
        self.iconLabel = QtGui.QLabel(self.tab)
        self.iconLabel.setGeometry(QtCore.QRect(10, 370, 231, 232))
        self.appPixMap = QtGui.QPixmap("bpmSchematic.jpg")
        self.iconLabel.setPixmap(self.appPixMap)
        self.titleLabel = QtGui.QLabel(self.tab)
        self.titleLabel.setGeometry(QtCore.QRect(10, 50, 270, 150))
        self.titleLabel.setObjectName(_fromUtf8("titleLabel"))
        self.infoLabel = QtGui.QLabel(self.tab)
        self.infoLabel.setGeometry(QtCore.QRect(10, 250, 270, 100))
        self.infoLabel.setObjectName(_fromUtf8("infoLabel"))
        self.TabWidget.addTab(self.tab, _fromUtf8(""))

        self.retranslateUi(self.TabWidget)
        QtCore.QMetaObject.connectSlotsByName(self.TabWidget)

    def retranslateUi(self, TabWidget):
        self.TabWidget.setWindowTitle(_translate("TabWidget", "TabWidget", None))
        self.launchATTButton.setText(_translate("TabWidget", "Calibrate Attenuation", None))
        self.launchDLYButton.setText(_translate("TabWidget", "Calibrate Delays", None))
        self.launchTrajButton.setText(_translate("TabWidget", "Trajectory Plot", None))
        self.launchMonButton.setText(_translate("TabWidget", "Monitor GUI", None))
        self.beamlineButton.setTitle(_translate("MainWindow", "Choose Beamline", None))
        self.velaINJButton.setText(_translate("MainWindow", "VELA-INJ", None))
        self.velaBA1Button.setText(_translate("MainWindow", "VELA-BA1", None))
        self.velaBA2Button.setText(_translate("MainWindow", "VELA-BA2", None))
        self.claraButton.setText(_translate("MainWindow", "CLARA", None))
        #self.iconLabel.setText(_translate("MainWindow", "iconLabel", None))
        self.c2vButton.setText(_translate("MainWindow", "CLARA-2-VELA", None))
        self.matrixButton.setTitle(_translate("MainWindow", "Choose Controller Type", None))
        self.physicalButton.setText(_translate("MainWindow", "Physical", None))
        self.virtualButton.setText(_translate("MainWindow", "Virtual", None))
        self.offlineButton.setText(_translate("MainWindow", "Offline", None))
        self.newFont = QtGui.QFont("Comic Sans", 20, QtGui.QFont.Bold)
        self.titleLabel.setFont(self.newFont)
        self.titleLabel.setText(_translate("TabWidget", "VELA/CLARA Beam \nPosition Monitor \nMaster App", None))
        self.infoText = "All applications related to calibrating and monitoring \nBPMs can be found here. First choose the beamline"
        self.infoText2 = self.infoText+"\nto initialise the controllers, and the controller type - "
        self.infoText3 = self.infoText2+"\nphysical, virtual or offline. Then select the app you \nwould like to launch using the buttons."
        self.infoLabel.setText(_translate("TabWidget", self.infoText3, None))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.tab), _translate("TabWidget", "BPM Master", None))
