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
setConfigOptions, InfiniteLine, ImageItem, GraphicsView, GraphicsLayout, GraphicsWindow, ViewBox, PlotDataItem, colorStr, mkColor, BarGraphItem, plot, LegendItem, PlotItem
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
        self.windowView = GraphicsView(useOpenGL=True)
        self.plotWindow = GraphicsLayout()
        self.windowView.setCentralItem(self.plotWindow)
        self.windowView.show()
        # self.windowView.setWindowTitle('Realtime prediction')
        self.plotVBox = QtGui.QVBoxLayout()
        self.bpmChargePlot = PlotItem()
        self.bpmChargePlot.enableAutoScale()
        self.bpmChargeBarGraph = BarGraphItem(x=range(numBPMs), height=1, width=0.5, brush=0.9, pen='b', name='BPM charge')
        self.wcmChargeBarGraph = PlotDataItem(x=range(numBPMs), y=range(numBPMs), brush=0.9, symbol='o', pen='r')
        # self.bpmChargePlot = plot()
        # self.wcmChargePlot = plot()
        # self.bpmChargePlot.addLegend()
        # self.bpmChargePlot.addItem(self.bpmChargeBarGraph)
        # self.bpmChargePlot.addItem(self.wcmChargeBarGraph)
        self.bpmChargePlot.addItem(self.bpmChargeBarGraph)
        self.bpmChargePlot.addItem(self.wcmChargeBarGraph)
        self.bpmChargePlot.showGrid(x=True, y=True)
        self.bpmChargePlot.layout.setMinimumWidth(1140.0)
        self.bpmChargePlot.layout.setMinimumHeight(500.0)
        self.bpmChargePlot.layout.setMaximumWidth(1140.0)
        self.bpmChargePlot.layout.setMaximumHeight(500.0)
        self.windowView.addItem(self.bpmChargePlot)
        self.plotVBox.addWidget(self.windowView)
        self.bpmChargeBarGraph.setOpts(height=10)
        self.calibrateButton = QtGui.QPushButton()
        self.calibrateButton.setObjectName(_fromUtf8("calibrateButton"))
        self.calibrateButton.setMinimumSize(QtCore.QSize(100,100))
        self.beamlineGroupBox = QtGui.QGroupBox()
        self.beamlineGroupBox.setObjectName(_fromUtf8("beamlineGroupBox"))
        self.claraPH1Button = QtGui.QRadioButton(self.beamlineGroupBox)
        self.claraPH1Button.setObjectName(_fromUtf8("claraPH1Button"))
        self.c2BA1Button = QtGui.QRadioButton(self.beamlineGroupBox)
        self.c2BA1Button.setObjectName(_fromUtf8("c2BA1Button"))
        self.c2S02Button = QtGui.QRadioButton(self.beamlineGroupBox)
        self.c2S02Button.setObjectName(_fromUtf8("c2S02Button"))
        self.radioButtonVBoxLayout = QtGui.QVBoxLayout()
        self.radioButtonVBoxLayout.setObjectName(_fromUtf8("radioButtonVBoxLayout"))
        self.claraPH1Button.setAutoExclusive(True)
        self.claraPH1Button.setCheckable(True)
        self.c2BA1Button.setAutoExclusive(True)
        self.c2BA1Button.setCheckable(True)
        self.c2S02Button.setAutoExclusive(True)
        self.c2S02Button.setCheckable(True)
        self.radioButtonVBoxLayout.addWidget(self.claraPH1Button)
        self.radioButtonVBoxLayout.addWidget(self.c2BA1Button)
        self.radioButtonVBoxLayout.addWidget(self.c2S02Button)
        self.beamlineGroupBox.setLayout(self.radioButtonVBoxLayout)
        self.plotVBox.addWidget(self.calibrateButton)
        self.plotVBox.addWidget(self.beamlineGroupBox)
        self.mainBox.addLayout(self.plotVBox)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "BPM Calibration", None))
        self.calibrateButton.setText(_translate("MainWindow", "Calibrate BPMs", None))
        self.beamlineGroupBox.setTitle(_translate("MainWindow", "Choose beamline", None))
        self.claraPH1Button.setText(_translate("MainWindow", "CLARA PH1", None))
        self.c2BA1Button.setText(_translate("MainWindow", "CLARA to BA1", None))
        self.c2S02Button.setText(_translate("MainWindow", "CLARA to S02", None))
        # self.MainWindow.setTabText(self.MainWindow.indexOf(self.tab), _translate("MainWindow", "Settings", None))
        self.newFont = QtGui.QFont("Comic Sans", 20, QtGui.QFont.Bold)

    def closeEvent(self, event):
        self.closing.emit()