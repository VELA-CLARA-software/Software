# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled1.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow
import pyqtgraph
import sys, os, time, math, datetime, copy, re
import glob
from PyQt5.QtCore import QObject, pyqtSignal, QThread, QTimer, QRectF, Qt
from PyQt5.QtGui import * #QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QTabWidget, QLineEdit, QFileDialog, QLabel, QAction, QPixmap, qApp, QStyle, QGroupBox, QSpinBox
from pyqtgraph import LegendItem, mkPen, mkBrush, LabelItem, TableWidget, GraphicsLayoutWidget, setConfigOption, \
setConfigOptions, InfiniteLine, ImageItem, GraphicsView, GraphicsLayout, GraphicsWindow, ViewBox, PlotDataItem, colorStr, mkColor
from pyqtgraph.graphicsItems.LegendItem import ItemSample
import argparse
import imageio
import numpy as np


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
        MainWindow.setObjectName(_fromUtf8("Charge measurement"))
        MainWindow.resize(1151, 759)
        self.mainWidget = QtGui.QWidget(MainWindow)
        self.mainWidget.resize(1140, 750)
        self.mainBox = QtGui.QHBoxLayout(self.mainWidget)
        self.labelBox = QtGui.QVBoxLayout()
        self.midVBox = QtGui.QVBoxLayout()
        self.plotVBox = QtGui.QVBoxLayout()
        self.numShotsHBox = QtGui.QHBoxLayout()
        self.titleLabel = QtGui.QLabel()
        self.infoLabel = QtGui.QLabel()
        self.labelBox.addWidget(self.titleLabel)
        self.labelBox.addWidget(self.infoLabel)
        self.labelBox.addStretch()
        self.scanButton = QtGui.QPushButton()
        self.scanButton.setObjectName(_fromUtf8("scanButton"))
        self.scanButton.setMinimumSize(QtCore.QSize(100,100))
        self.comboBox = QtGui.QComboBox()
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.groupBox = QtGui.QGroupBox()
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.groupBox.setMinimumSize(QtCore.QSize(200,200))
        self.newValsVBox = QtGui.QVBoxLayout()
        self.newVals = QtGui.QTextEdit()
        self.newVals.setText(_fromUtf8(""))
        self.newVals.setObjectName(_fromUtf8("newVals"))
        self.newValsVBox.addWidget(self.newVals)
        self.groupBox.setLayout(self.newValsVBox)
        self.numShotsLabel = QtGui.QLabel()
        self.numShotsLabel.setObjectName(_fromUtf8("numShotsLabel"))
        self.numShotsOutputWidget = QtGui.QPlainTextEdit()
        self.numShotsOutputWidget.setObjectName(_fromUtf8("numShotsOutputWidget"))
        self.numShotsOutputWidget.setMinimumSize(QtCore.QSize(30,30))
        self.numShotsOutputWidget.setMaximumSize(QtCore.QSize(30,30))
        self.numShotsHBox.addWidget(self.numShotsLabel)
        self.numShotsHBox.addWidget(self.numShotsOutputWidget)
        self.numShotsHBox.addSpacing(300)
        self.measureTypeGroupBox = QtGui.QGroupBox()
        self.measureTypeGroupBox.setObjectName(_fromUtf8("measureTypeGroupBox"))
        self.attenuationButton = QtGui.QRadioButton(self.measureTypeGroupBox)
        self.attenuationButton.setObjectName(_fromUtf8("attenuationButton"))
        self.delayButton = QtGui.QRadioButton(self.measureTypeGroupBox)
        self.delayButton.setObjectName(_fromUtf8("delayButton"))
        self.radioButtonVBoxLayout = QtGui.QVBoxLayout()
        self.radioButtonVBoxLayout.setObjectName(_fromUtf8("radioButtonVBoxLayout"))
        self.attenuationButton.setAutoExclusive(True)
        self.attenuationButton.setCheckable(True)
        self.delayButton.setAutoExclusive(True)
        self.delayButton.setCheckable(True)
        self.radioButtonVBoxLayout.addWidget(self.attenuationButton)
        self.radioButtonVBoxLayout.addWidget(self.delayButton)
        self.measureTypeGroupBox.setLayout(self.radioButtonVBoxLayout)
        self.scanRangeHBox = QtGui.QHBoxLayout()
        self.rangeLabelVBox = QtGui.QVBoxLayout()
        self.lowerBoundVBox = QtGui.QVBoxLayout()
        self.upperBoundVBox = QtGui.QVBoxLayout()
        self.numStepsVBox = QtGui.QVBoxLayout()
        self.lowerBoundOutputWidget = QtGui.QPlainTextEdit()
        self.lowerBoundOutputWidget.setObjectName(_fromUtf8("lowerBoundOutputWidget"))
        self.upperBoundOutputWidget = QtGui.QPlainTextEdit()
        self.upperBoundOutputWidget.setObjectName(_fromUtf8("upperBoundOutputWidget"))
        self.numStepsOutputWidget = QtGui.QPlainTextEdit()
        self.numStepsOutputWidget.setObjectName(_fromUtf8("numStepsOutputWidget"))
        self.scanRangeSpacer = QtGui.QLabel()
        self.scanRangeSpacer.setObjectName(_fromUtf8("scanRangeSpacer"))
        self.scanRangeLabel = QtGui.QLabel()
        self.scanRangeLabel.setObjectName(_fromUtf8("scanRangeLabel"))
        self.lowerBoundLabel = QtGui.QLabel()
        self.lowerBoundLabel.setObjectName(_fromUtf8("lowerBoundLabel"))
        self.upperBoundLabel = QtGui.QLabel()
        self.upperBoundLabel.setObjectName(_fromUtf8("upperBoundLabel"))
        self.numStepsLabel = QtGui.QLabel()
        self.numStepsLabel.setObjectName(_fromUtf8("numStepsLabel"))
        self.lowerBoundOutputWidget.setMinimumSize(QtCore.QSize(30,30))
        self.lowerBoundOutputWidget.setMaximumSize(QtCore.QSize(30,30))
        self.upperBoundOutputWidget.setMinimumSize(QtCore.QSize(30, 30))
        self.upperBoundOutputWidget.setMaximumSize(QtCore.QSize(30, 30))
        self.numStepsOutputWidget.setMinimumSize(QtCore.QSize(30,30))
        self.numStepsOutputWidget.setMaximumSize(QtCore.QSize(30,30))
        self.rangeLabelVBox.addWidget(self.scanRangeSpacer)
        self.rangeLabelVBox.addWidget(self.scanRangeLabel)
        self.lowerBoundVBox.addWidget(self.lowerBoundLabel)
        self.lowerBoundVBox.addWidget(self.lowerBoundOutputWidget)
        self.upperBoundVBox.addWidget(self.upperBoundLabel)
        self.upperBoundVBox.addWidget(self.upperBoundOutputWidget)
        self.numStepsVBox.addWidget(self.numStepsLabel)
        self.numStepsVBox.addWidget(self.numStepsOutputWidget)
        self.rangeLabelVBox.addStretch()
        self.lowerBoundVBox.addStretch()
        self.upperBoundVBox.addStretch()
        self.numStepsVBox.addStretch()
        self.scanRangeHBox.addLayout(self.rangeLabelVBox)
        self.scanRangeHBox.addLayout(self.lowerBoundVBox)
        self.scanRangeHBox.addLayout(self.upperBoundVBox)
        self.scanRangeHBox.addLayout(self.numStepsVBox)
        self.scanRangeHBox.addStretch()
        self.messageHBox = QtGui.QHBoxLayout()
        self.messageLabel = QtGui.QLabel()
        self.messageLabel.setObjectName(_fromUtf8("messageHBox"))
        self.messageHBox.addWidget(self.messageLabel)
        self.progressBar = QtGui.QProgressBar()
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.messageHBox.addWidget(self.progressBar)
        self.messageHBox.addStretch()
        self.bunchChargeHBox = QtGui.QHBoxLayout()
        self.bunchChargeLabel = QtGui.QLabel()
        self.bunchChargeLabel.setObjectName(_fromUtf8("bunchChargeLabel"))
        self.bunchChargeChannelLabel = QtGui.QLabel()
        self.bunchChargeChannelLabel.setObjectName(_fromUtf8("bunchChargeChannelLabel"))
        self.bunchChargeDiagTypeLabel = QtGui.QLabel()
        self.bunchChargeDiagTypeLabel.setObjectName(_fromUtf8("bunchChargeDiagTypeLabel"))
        self.bunchChargeOutputWidget = QtGui.QLabel()
        self.bunchChargeOutputWidget.setObjectName(_fromUtf8("bunchChargeOutputWidget"))
        self.bunchChargeHBox.addWidget(self.bunchChargeLabel)
        self.bunchChargeHBox.addWidget(self.bunchChargeDiagTypeLabel)
        self.bunchChargeHBox.addWidget(self.bunchChargeOutputWidget)
        self.midVBox.addWidget(self.comboBox)
        self.midVBox.addLayout(self.numShotsHBox)
        # self.midVBox.addWidget(self.measureTypeGroupBox)
        self.midVBox.addWidget(self.scanButton)
        self.midVBox.addWidget(self.groupBox)
        self.midVBox.addLayout(self.scanRangeHBox)
        self.midVBox.addLayout(self.messageHBox)
        self.midVBox.addLayout(self.bunchChargeHBox)
        self.chargePlotWidget = QWidget()
        self.chargePlotLayout = QVBoxLayout()
        self.chargePlotWidget.setLayout(self.chargePlotLayout)
        self.chargePlotView = GraphicsView(self.chargePlotWidget,useOpenGL=True)
        self.chargePlotWidgetGraphicsLayout = GraphicsLayout()
        self.chargePlotView.setCentralItem(self.chargePlotWidgetGraphicsLayout)
        self.plotItem = pyqtgraph.ErrorBarItem(x=np.array([]), y=np.array([]), height=np.array([]), beam=None, pen={'color':'b', 'width':2})
        self.chargePlot = self.chargePlotWidgetGraphicsLayout.addPlot(title='wcm vs ophir',x=np.array([]), y=np.array([]), height=np.array([]), width=np.array([]), beam=None, pen={'color':'b', 'width':2})
        self.chargePlot.showGrid(x=True, y=True)
        self.plotVBox.addWidget(self.chargePlotView)
        self.mainBox.addLayout(self.midVBox)
        self.mainBox.addLayout(self.plotVBox)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Charge measurement", None))
        self.scanButton.setText(_translate("MainWindow", "Scan laser attenuator", None))
        self.groupBox.setTitle(_translate("MainWindow", "Comments", None))
        self.numShotsOutputWidget.setPlainText(_translate("MainWindow", "10", None))
        self.numShotsLabel.setText(_translate("MainWindow", "# Shots", None))
        self.measureTypeGroupBox.setTitle(_translate("MainWindow", "Choose calibration type", None))
        self.attenuationButton.setText(_translate("MainWindow", "Attenuation", None))
        self.delayButton.setText(_translate("MainWindow", "Delay", None))
        self.scanRangeLabel.setText(_translate("MainWindow", "Scan Range", None))
        self.newVals.setText(_translate("MainWindow", "", None))
        self.lowerBoundLabel.setText(_translate("MainWindow", "Lower Bound", None))
        self.upperBoundLabel.setText(_translate("MainWindow", "Upper Bound", None))
        self.numStepsLabel.setText(_translate("MainWindow", "# steps", None))
        self.lowerBoundOutputWidget.setPlainText(_translate("MainWindow", "-9.0", None))
        self.upperBoundOutputWidget.setPlainText(_translate("MainWindow", "-1.0", None))
        self.numStepsOutputWidget.setPlainText(_translate("MainWindow", "20", None))
        self.bunchChargeLabel.setText(_translate("MainWindow", "Bunch charge - monitoring from", None))
        # self.MainWindow.setTabText(self.MainWindow.indexOf(self.tab), _translate("MainWindow", "Settings", None))
        self.newFont = QtGui.QFont("Comic Sans", 20, QtGui.QFont.Bold)
        self.titleLabel.setFont(self.newFont)
        self.titleLabel.setText(_translate("MainWindow", "VELA/CLARA Beam \nPosition Monitor \nCalibrator", None))
        self.infoText1 = "Please select the BPMs to calibrate from the list using \nthe drop-down menu and the 'Calibrate BPM' button."
        self.infoText2 = self.infoText1+"\nThe number of shots for each attenuation/delay setting,\n and the range to scan over (from 1 - 20 \n or 0 - 511), can also be set."
        self.infoText3 = self.infoText2+" Click 'Calibrate BPMs' when \nready. The tabs generated will show the results."
        self.infoLabel.setText(_translate("MainWindow", self.infoText3, None))
        #self.TabWidget.setTabText(self.TabWidget.indexOf(self.tab1), _translate("TabWidget", "Tab 2", None))

    def closeEvent(self, event):
        self.closing.emit()