# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled1.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QMainWindow
import pyqtgraph
import sys, os, time, math, datetime, copy, re
import glob
from PyQt4.QtCore import QObject, pyqtSignal, QThread, QTimer, QRectF, Qt
from PyQt4.QtGui import * #QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QTabWidget, QLineEdit, QFileDialog, QLabel, QAction, QPixmap, qApp, QStyle, QGroupBox, QSpinBox
from pyqtgraph import LegendItem, mkPen, mkBrush, LabelItem, TableWidget, GraphicsLayoutWidget, setConfigOption, \
setConfigOptions, InfiniteLine, ImageItem, GraphicsView, GraphicsLayout, AxisItem, ViewBox, PlotDataItem, colorStr, mkColor
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
        MainWindow.setObjectName(_fromUtf8("BPM Attenuation Calibrator"))
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
        self.calibrateButton = QtGui.QPushButton()
        self.calibrateButton.setObjectName(_fromUtf8("calibrateButton"))
        self.calibrateButton.setMinimumSize(QtCore.QSize(100,100))
        self.comboBox = QtGui.QComboBox()
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.groupBox = QtGui.QGroupBox()
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.groupBox.setMinimumSize(QtCore.QSize(200,200))
        self.newATTValsVBox = QtGui.QVBoxLayout()
        self.newATTVals = QtGui.QTextEdit()
        self.newATTVals.setText(_fromUtf8(""))
        self.newATTVals.setObjectName(_fromUtf8("newATTVals"))
        self.newATTValsVBox.addWidget(self.newATTVals)
        self.groupBox.setLayout(self.newATTValsVBox)
        self.numShotsLabel = QtGui.QLabel()
        self.numShotsLabel.setObjectName(_fromUtf8("numShotsLabel"))
        self.numShotsOutputWidget = QtGui.QPlainTextEdit()
        self.numShotsOutputWidget.setObjectName(_fromUtf8("numShotsOutputWidget"))
        self.numShotsOutputWidget.setMinimumSize(QtCore.QSize(30,30))
        self.numShotsOutputWidget.setMaximumSize(QtCore.QSize(30,30))
        self.numShotsHBox.addWidget(self.numShotsLabel)
        self.numShotsHBox.addWidget(self.numShotsOutputWidget)
        self.numShotsHBox.addSpacing(300)
        self.scanRangeHBox = QtGui.QHBoxLayout()
        self.rangeLabelVBox = QtGui.QVBoxLayout()
        self.lowerBoundVBox = QtGui.QVBoxLayout()
        self.upperBoundVBox = QtGui.QVBoxLayout()
        self.lowerATTBoundOutputWidget = QtGui.QPlainTextEdit()
        self.lowerATTBoundOutputWidget.setObjectName(_fromUtf8("lowerATTBoundOutputWidget"))
        self.upperATTBoundOutputWidget = QtGui.QPlainTextEdit()
        self.upperATTBoundOutputWidget.setObjectName(_fromUtf8("upperATTBoundOutputWidget"))
        self.scanRangeSpacer = QtGui.QLabel()
        self.scanRangeSpacer.setObjectName(_fromUtf8("scanRangeSpacer"))
        self.scanRangeLabel = QtGui.QLabel()
        self.scanRangeLabel.setObjectName(_fromUtf8("scanRangeLabel"))
        self.lowerBoundLabel = QtGui.QLabel()
        self.lowerBoundLabel.setObjectName(_fromUtf8("lowerBoundLabel"))
        self.upperBoundLabel = QtGui.QLabel()
        self.upperBoundLabel.setObjectName(_fromUtf8("upperBoundLabel"))
        self.lowerATTBoundOutputWidget.setMinimumSize(QtCore.QSize(30,30))
        self.lowerATTBoundOutputWidget.setMaximumSize(QtCore.QSize(30,30))
        self.upperATTBoundOutputWidget.setMinimumSize(QtCore.QSize(30,30))
        self.upperATTBoundOutputWidget.setMaximumSize(QtCore.QSize(30,30))
        self.rangeLabelVBox.addWidget(self.scanRangeSpacer)
        self.rangeLabelVBox.addWidget(self.scanRangeLabel)
        self.lowerBoundVBox.addWidget(self.lowerBoundLabel)
        self.lowerBoundVBox.addWidget(self.lowerATTBoundOutputWidget)
        self.upperBoundVBox.addWidget(self.upperBoundLabel)
        self.upperBoundVBox.addWidget(self.upperATTBoundOutputWidget)
        self.rangeLabelVBox.addStretch()
        self.lowerBoundVBox.addStretch()
        self.upperBoundVBox.addStretch()
        self.scanRangeHBox.addLayout(self.rangeLabelVBox)
        self.scanRangeHBox.addLayout(self.lowerBoundVBox)
        self.scanRangeHBox.addLayout(self.upperBoundVBox)
        self.scanRangeHBox.addStretch()
        self.bunchChargeHBox = QtGui.QHBoxLayout()
        self.bunchChargeLabel = QtGui.QLabel()
        self.bunchChargeLabel.setObjectName(_fromUtf8("bunchChargeLabel"))
        self.bunchChargeScopeLabel = QtGui.QLabel()
        self.bunchChargeScopeLabel.setObjectName(_fromUtf8("bunchChargeScopeLabel"))
        self.bunchChargeChannelLabel = QtGui.QLabel()
        self.bunchChargeChannelLabel.setObjectName(_fromUtf8("bunchChargeChannelLabel"))
        self.bunchChargeDiagTypeLabel = QtGui.QLabel()
        self.bunchChargeDiagTypeLabel.setObjectName(_fromUtf8("bunchChargeDiagTypeLabel"))
        self.bunchChargeOutputWidget = QtGui.QLabel()
        self.bunchChargeOutputWidget.setObjectName(_fromUtf8("bunchChargeOutputWidget"))
        self.bunchChargeHBox.addWidget(self.bunchChargeLabel)
        self.bunchChargeHBox.addWidget(self.bunchChargeScopeLabel)
        self.bunchChargeHBox.addWidget(self.bunchChargeChannelLabel)
        self.bunchChargeHBox.addWidget(self.bunchChargeDiagTypeLabel)
        self.bunchChargeHBox.addWidget(self.bunchChargeOutputWidget)
        self.midVBox.addWidget(self.comboBox)
        self.midVBox.addLayout(self.numShotsHBox)
        self.midVBox.addWidget(self.calibrateButton)
        self.midVBox.addWidget(self.groupBox)
        self.midVBox.addLayout(self.scanRangeHBox)
        self.midVBox.addLayout(self.bunchChargeHBox)
        self.bpmxPlotWidget = QWidget()
        self.bpmxPlotLayout = QVBoxLayout()
        self.bpmxPlotWidget.setLayout(self.bpmxPlotLayout)
        self.bpmxPlotView = GraphicsView(self.bpmxPlotWidget,useOpenGL=True)
        self.bpmxPlotWidgetGraphicsLayout = GraphicsLayout()
        self.bpmxPlotView.setCentralItem(self.bpmxPlotWidgetGraphicsLayout)
        self.bpmxPlot = self.bpmxPlotWidgetGraphicsLayout.addPlot(title='bpmx')
        self.bpmxPlot.showGrid(x=True, y=True)
        self.bpmyPlotWidget = QWidget()
        self.bpmyPlotLayout = QVBoxLayout()
        self.bpmyPlotWidget.setLayout(self.bpmyPlotLayout)
        self.bpmyPlotView = GraphicsView(self.bpmyPlotWidget, useOpenGL=True)
        self.bpmyPlotWidgetGraphicsLayout = GraphicsLayout()
        self.bpmyPlotView.setCentralItem(self.bpmyPlotWidgetGraphicsLayout)
        self.bpmyPlot = self.bpmyPlotWidgetGraphicsLayout.addPlot(title='bpmy')
        self.bpmyPlot.showGrid(x=True, y=True)
        self.plotVBox.addWidget(self.bpmxPlotView)
        self.plotVBox.addWidget(self.bpmyPlotView)
        self.mainBox.addLayout(self.labelBox)
        self.mainBox.addLayout(self.midVBox)
        self.mainBox.addLayout(self.plotVBox)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "BPM Attenuation Calibrator", None))
        self.calibrateButton.setText(_translate("MainWindow", "Calibrate Attenuations", None))
        self.groupBox.setTitle(_translate("MainWindow", "New BPM Attenuation Values", None))
        self.numShotsOutputWidget.setPlainText(_translate("MainWindow", "2", None))
        self.numShotsLabel.setText(_translate("MainWindow", "# Shots", None))
        self.scanRangeLabel.setText(_translate("MainWindow", "ATT Scan Range", None))
        self.newATTVals.setText(_translate("MainWindow", "", None))
        self.lowerBoundLabel.setText(_translate("MainWindow", "Lower Bound", None))
        self.upperBoundLabel.setText(_translate("MainWindow", "Upper Bound", None))
        self.lowerATTBoundOutputWidget.setPlainText(_translate("MainWindow", "2", None))
        self.upperATTBoundOutputWidget.setPlainText(_translate("MainWindow", "10", None))
        self.bunchChargeLabel.setText(_translate("MainWindow", "Bunch charge - monitoring from", None))
        # self.MainWindow.setTabText(self.MainWindow.indexOf(self.tab), _translate("MainWindow", "Settings", None))
        self.newFont = QtGui.QFont("Comic Sans", 20, QtGui.QFont.Bold)
        self.titleLabel.setFont(self.newFont)
        self.titleLabel.setText(_translate("MainWindow", "VELA/CLARA Beam \nPosition Monitor \nAttenuation \nCalibrator", None))
        self.infoText1 = "Please select the BPMs to calibrate from the list using \nthe drop-down menu and the 'Calibrate BPM' button."
        self.infoText2 = self.infoText1+"\nThe number of shots for each attenuation setting,\n and the range to scan over (from 1 - 20),\n can also be set."
        self.infoText3 = self.infoText2+" Click 'Calibrate attenuations' when \nready. The tabs generated will show the results."
        self.infoLabel.setText(_translate("MainWindow", self.infoText3, None))
        #self.TabWidget.setTabText(self.TabWidget.indexOf(self.tab1), _translate("TabWidget", "Tab 2", None))

    def addPlotTab(self, MainWindow, pvName):
        self.MainWindow = MainWindow
        self.MainWindow.setObjectName(_fromUtf8("MainWindow"))
        self.MainWindow.resize(699, 602)
        self.tab1 = QtGui.QWidget()
        self.tab1.setObjectName(_fromUtf8("tab"))
        self.MainWindow.setTabText(self.MainWindow.indexOf(self.tab1), _translate("MainWindow", self.pvName, None))
        self.graphicsView = pyqtgraph.GraphicsView(self.tab1)
        self.graphicsView.setGeometry(QtCore.QRect(140, 20, 441, 261))
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.glayoutOutput = pyqtgraph.GraphicsLayout(border = (400,400,400))
        self.graphicsView.setCentralItem(self.glayoutOutput)
        self.graphicsView_2 = pyqtgraph.GraphicsView(self.tab1)
        self.graphicsView_2.setGeometry(QtCore.QRect(140, 290, 441, 261))
        self.graphicsView_2.setObjectName(_fromUtf8("graphicsView_2"))
        self.glayoutOutput_2 = pyqtgraph.GraphicsLayout(border = (400,400,400))
        self.graphicsView_2.setCentralItem(self.glayoutOutput_2)
        self.glayoutOutputs[self.pvName] = self.glayoutOutput
        self.glayoutOutputs_2[self.pvName] = self.glayoutOutput_2

    def closeEvent(self, event):
        self.closing.emit()