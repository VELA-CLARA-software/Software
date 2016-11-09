#!/usr/bin/env python

# embedding_in_qt4.py --- Simple Qt4 application embedding matplotlib canvases
#
# Copyright (C) 2005 Florent Rougon
#               2006 Darren Dale
#
# This file is an example program for matplotlib. It may be used and
# modified with no restriction; raw copies as well as modified versions
# may be distributed without limitation.

from __future__ import unicode_literals
import sys
import os
import random
import numpy
from matplotlib.backends import qt_compat
use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE
if use_pyside:
    from PySide import QtGui, QtCore
else:
    from PyQt4 import QtGui, QtCore

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

from numpy import arange, sin, pi
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

progname = os.path.basename(sys.argv[0])
progversion = "0.1"


class trajMyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100, data = None):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)
        self.data = data

        self.compute_initial_figure()

        #
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class trajMyDynamicMplCanvas(trajMyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        trajMyMplCanvas.__init__(self, *args, **kwargs)

    def update_figure(self, data):
        self.data = data
        self.width = 0.1
        self.locs = numpy.arange(len(self.data))
        self.bars = self.axes.bar(self.locs, self.data.values(), self.width)
        self.axes.set_xticks(self.locs)
        self.axes.set_xticklabels(self.data.keys())
        self.axes.set_ylabel("mm")
        #self.axes.set_offset_position(0.5)
        self.axes.set_xlim(0, len(self.data))
        self.axes.set_ylim(-10, 10,)
        self.draw()


class trajUi_MainWindow(QtCore.QObject):
    def setupUI(self, TabWidget, bpmCont, contType):
        self.TabWidget = TabWidget
        self.bpmCont = bpmCont
        self.contType = contType
        self.TabWidget.setObjectName("TabWidget")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.TabWidget.resize(699, 602)
        self.pushButton = QtGui.QPushButton(self.tab)
        self.pushButton.setGeometry(QtCore.QRect(308, 270, 231, 161))
        self.pushButton.setObjectName(("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(self.tab)
        self.pushButton_2.setGeometry(QtCore.QRect(560, 270, 81, 61))
        self.pushButton_2.setObjectName(("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(self.tab)
        self.pushButton_3.setGeometry(QtCore.QRect(560, 370, 80, 60))
        self.pushButton_3.setObjectName(("pushButton_3"))
        self.plainTextEdit = QtGui.QPlainTextEdit(self.tab)
        self.plainTextEdit.setGeometry(QtCore.QRect(560, 80, 101, 171))
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.groupButton = QtGui.QGroupBox(self.tab)
        self.groupButton.setGeometry(QtCore.QRect(308, 50, 231, 112))
        self.groupButton.setObjectName(_fromUtf8("groupButton"))
        self.individualButton = QtGui.QRadioButton(self.groupButton)
        self.individualButton.setGeometry(QtCore.QRect(308, 20, 231, 32))
        self.individualButton.setObjectName(_fromUtf8("individualButton"))
        self.trajectoryButton = QtGui.QRadioButton(self.groupButton)
        self.trajectoryButton.setGeometry(QtCore.QRect(308, 40, 231, 52))
        self.trajectoryButton.setObjectName(_fromUtf8("trajectoryButton"))
        self.radioButtonVBoxLayout = QtGui.QVBoxLayout(self.tab)
        self.radioButtonVBoxLayout.setGeometry(QtCore.QRect(308, 10, 231, 112))
        self.radioButtonVBoxLayout.setObjectName(_fromUtf8("radioButtonVBoxLayout"))
        self.individualButton.setAutoExclusive(True)
        self.individualButton.setCheckable(True)
        self.trajectoryButton.setAutoExclusive(True)
        self.trajectoryButton.setCheckable(True)
        self.radioButtonVBoxLayout.addWidget(self.individualButton)
        self.radioButtonVBoxLayout.addWidget(self.trajectoryButton)
        self.groupButton.setLayout(self.radioButtonVBoxLayout)
        self.individualButton.setChecked(True)
        self.comboBox = QtGui.QComboBox(self.tab)
        self.comboBox.setGeometry(QtCore.QRect(560, 50, 111, 16))
        self.comboBox.setObjectName(("comboBox"))
        self.titleLabel = QtGui.QLabel(self.tab)
        self.titleLabel.setGeometry(QtCore.QRect(10, 50, 270, 100))
        self.titleLabel.setObjectName(_fromUtf8("titleLabel"))
        self.infoLabel = QtGui.QLabel(self.tab)
        self.infoLabel.setGeometry(QtCore.QRect(10, 250, 270, 100))
        self.infoLabel.setObjectName(_fromUtf8("infoLabel"))
        self.data1 = [random.randint(-10, 10) for i in range(5)]

        self.tab1 = QtGui.QTabWidget()
        self.tab1.setObjectName(("tab1"))
        self.vBoxLayout = QtGui.QVBoxLayout(self.tab1)
        self.xPlot = trajMyDynamicMplCanvas(self.tab1, width=5, height=4, dpi=100, data = self.data1)
        self.yPlot = trajMyDynamicMplCanvas(self.tab1, width=5, height=4, dpi=100, data = self.data1)
        self.vBoxLayout.addWidget(self.xPlot)
        self.vBoxLayout.addWidget(self.yPlot)
        self.tab.setFocus()
        self.TabWidget.addTab(self.tab, (""))
        self.TabWidget.addTab(self.tab1, (""))
        self.retranslateUi(self.TabWidget)
        QtCore.QMetaObject.connectSlotsByName(self.TabWidget)

    def setComboBox(self, TabWidget):
        self.comboBox.clear()
        self.bpmPVList = self.bpmCont.getBPMNames()
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        if self.individualButton.isChecked():
            self.i = 0
            while self.i < len(self.bpmPVList):
                self.comboBox.setItemText(self.i, _translate("TabWidget", str(self.bpmPVList[self.i]), None))
                self.i = self.i + 1
        elif self.trajectoryButton.isChecked() and self.contType == "VELA_INJ":
            self.comboBox.setItemText(0, _translate("TabWidget", "VELA INJ", None))
            self.comboBox.setItemText(1, _translate("TabWidget", "VELA Spectrometer", None))
        elif self.trajectoryButton.isChecked() and self.contType == "VELA_BA1":
            self.comboBox.setItemText(0, _translate("TabWidget", "VELA BA1", None))
        elif self.trajectoryButton.isChecked() and self.contType == "VELA_BA2":
            self.comboBox.setItemText(0, _translate("TabWidget", "VELA BA2", None))
        elif self.trajectoryButton.isChecked() and self.contType == "CLARA":
            self.comboBox.setItemText(0, _translate("TabWidget", "CLARA BA2", None))
        elif self.trajectoryButton.isChecked() and self.contType == "C2V":
            self.comboBox.setItemText(0, _translate("TabWidget", "C2V", None))

    def retranslateUi(self, TabWidget):
        self.TabWidget.setWindowTitle(_translate("TabWidget", "TabWidget", None))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.tab), _translate("TabWidget", "Settings", None))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.tab1), _translate("TabWidget", "Plot", None))
        self.pushButton.setText(_translate("TabWidget", "Go", None))
        self.pushButton_2.setText(_translate("TabWidget", "Append", None))
        self.pushButton_3.setText(_translate("TabWidget", "Clear PV List", None))
        self.setComboBox(TabWidget)
        self.groupButton.setTitle(_translate("MainWindow", "Choose Trajectory or Individual BPMs?", None))
        self.individualButton.setText(_translate("MainWindow", "BPMs", None))
        self.trajectoryButton.setText(_translate("MainWindow", "Trajectory", None))
        self.newFont = QtGui.QFont("Comic Sans", 20, QtGui.QFont.Bold)
        self.titleLabel.setFont(self.newFont)
        self.titleLabel.setText(_translate("TabWidget", "VELA/CLARA Beam \nPosition Monitor \nTrajectory Plotter", None))
        self.infoText = "Please select whether you would like to monitor \nindividual BPMs, or select a beamline."
        self.infoText2 = self.infoText+"\nIf selecting individual BPMs, append them to \nthe list using the 'Append' button."
        self.infoText3 = self.infoText2+" Then click 'Go'."
        self.infoLabel.setText(_translate("TabWidget", self.infoText3, None))
