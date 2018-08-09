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
setConfigOptions, InfiniteLine, ImageItem, GraphicsView, GraphicsLayout, GraphicsWindow, ViewBox, PlotDataItem, colorStr, mkColor, BarGraphItem, plot, LegendItem
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
    def setupUi(self, MainWindow, numBPMs):
        MainWindow.setObjectName(_fromUtf8("BPM Charge Plotter"))
        MainWindow.resize(1151, 759)
        self.numBPMs = numBPMs
        self.mainWidget = QtGui.QWidget(MainWindow)
        self.mainWidget.resize(1140, 750)
        self.mainBox = QtGui.QHBoxLayout(self.mainWidget)
        self.plotVBox = QtGui.QVBoxLayout()
        self.bpmChargeBarGraph = BarGraphItem(x=range(numBPMs), height=1, width=0.5, brush=0.7, pen='r', name='BPM charge')
        self.wcmChargeBarGraph = BarGraphItem(x=range(numBPMs), height=0.1, width=0.5, brush=0.1, pen='b', name='WCM charge')
        self.bpmChargePlot = plot()
        self.wcmChargePlot = plot()
        self.bpmChargePlot.addLegend()
        self.bpmChargePlot.addItem(self.bpmChargeBarGraph)
        self.bpmChargePlot.addItem(self.wcmChargeBarGraph)
        self.bpmChargePlot.showGrid(x=True, y=True)
        self.plotVBox.addWidget(self.bpmChargePlot)
        self.bpmChargeBarGraph.setOpts(height=10)
        self.calibrateButton = QtGui.QPushButton()
        self.calibrateButton.setObjectName(_fromUtf8("calibrateButton"))
        self.calibrateButton.setMinimumSize(QtCore.QSize(100,100))
        self.plotVBox.addWidget(self.calibrateButton)
        self.mainBox.addLayout(self.plotVBox)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "BPM Calibration", None))
        self.calibrateButton.setText(_translate("MainWindow", "Calibrate BPMs", None))
        # self.MainWindow.setTabText(self.MainWindow.indexOf(self.tab), _translate("MainWindow", "Settings", None))
        self.newFont = QtGui.QFont("Comic Sans", 20, QtGui.QFont.Bold)

    def closeEvent(self, event):
        self.closing.emit()