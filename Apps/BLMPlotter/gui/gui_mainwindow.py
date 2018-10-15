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
        MainWindow.setObjectName(_fromUtf8("BPM Attenuation Calibrator"))
        MainWindow.resize(1151, 759)
        self.mainWidget = QtGui.QWidget(MainWindow)
        self.mainWidget.resize(1140, 750)
        self.mainBox = QtGui.QVBoxLayout(self.mainWidget)
        self.plotHBox = QtGui.QHBoxLayout(self.mainWidget)
        self.blmPlotWidget = QWidget()
        self.blmPlotLayout = QVBoxLayout()
        self.blmPlotWidget.setLayout(self.blmPlotLayout)
        self.blmPlotView = GraphicsView(self.blmPlotWidget, useOpenGL=True)
        self.blmPlotWidgetGraphicsLayout = GraphicsLayout()
        self.blmPlotView.setCentralItem(self.blmPlotWidgetGraphicsLayout)
        self.blmPlot = self.blmPlotWidgetGraphicsLayout.addPlot(title='blm')
        self.blmPlot.showGrid(x=True, y=True)
        self.plotHBox.addWidget(self.blmPlotView)
        self.radioButtonHBoxLayout = QtGui.QHBoxLayout()
        self.radioButtonHBoxLayout.setObjectName(_fromUtf8("radioButtonVBoxLayout"))
        self.filterGroupBox = QtGui.QGroupBox()
        self.filterGroupBox.setObjectName(_fromUtf8("filterGroupBox"))
        self.filterYesButton = QtGui.QRadioButton(self.filterGroupBox)
        self.filterYesButton.setObjectName(_fromUtf8("filterYesButton"))
        self.filterNoButton = QtGui.QRadioButton(self.filterGroupBox)
        self.filterNoButton.setObjectName(_fromUtf8("filterNoButton"))
        self.filterYesButton.setAutoExclusive(True)
        self.filterYesButton.setCheckable(True)
        self.filterNoButton.setAutoExclusive(True)
        self.filterNoButton.setCheckable(True)
        self.filterNoButton.setChecked(True)
        self.radioButtonHBoxLayout.addWidget(self.filterYesButton)
        self.radioButtonHBoxLayout.addWidget(self.filterNoButton)
        self.filterGroupBox.setLayout(self.radioButtonHBoxLayout)
        self.filterSizeLabel = QtGui.QLabel()
        self.filterSizeLabel.setObjectName(_fromUtf8("filterSizeLabel"))
        self.filterSizeOutputWidget = QtGui.QPlainTextEdit()
        self.filterSizeOutputWidget.setObjectName(_fromUtf8("filterSizeOutputWidget"))
        self.filterGroupBox.setMaximumSize(QtCore.QSize(1100, 50))
        self.filterSizeOutputWidget.setMinimumSize(QtCore.QSize(50, 30))
        self.filterSizeOutputWidget.setMaximumSize(QtCore.QSize(50, 30))
        self.radioButtonHBoxLayout.addWidget(self.filterSizeOutputWidget)
        self.radioButtonHBoxLayout.addWidget(self.filterSizeLabel)
        self.numShotsHBox = QtGui.QHBoxLayout()
        self.numShotsLabel = QtGui.QLabel()
        self.numShotsLabel.setObjectName(_fromUtf8("numShotsLabel"))
        self.setNumShotsButton = QtGui.QPushButton()
        self.setNumShotsButton.setObjectName(_fromUtf8("setNumShotsButton"))
        self.setNumShotsButton.setMinimumSize(QtCore.QSize(60, 40))
        self.numShotsOutputWidget = QtGui.QPlainTextEdit()
        self.numShotsOutputWidget.setObjectName(_fromUtf8("numShotsOutputWidget"))
        self.numShotsOutputWidget.setMinimumSize(QtCore.QSize(30,30))
        self.numShotsOutputWidget.setMaximumSize(QtCore.QSize(30,30))
        self.numShotsHBox.addWidget(self.numShotsLabel)
        self.numShotsHBox.addWidget(self.numShotsOutputWidget)
        self.numShotsHBox.addWidget(self.setNumShotsButton)
        # self.numShotsHBox.addSpacing(300)
        self.bunchChargeHBox = QtGui.QHBoxLayout()
        self.bunchChargeDiagTypeLabel = QtGui.QLabel()
        self.bunchChargeDiagTypeLabel.setObjectName(_fromUtf8("bunchChargeDiagTypeLabel"))
        self.bunchChargeOutputWidget = QtGui.QLabel()
        self.bunchChargeOutputWidget.setObjectName(_fromUtf8("bunchChargeOutputWidget"))
        self.bunchChargeHBox.addWidget(self.bunchChargeDiagTypeLabel)
        self.bunchChargeHBox.addWidget(self.bunchChargeOutputWidget)
        self.saveDataHBox = QtGui.QHBoxLayout()
        self.saveDataButton = QtGui.QPushButton()
        self.saveDataButton.setObjectName(_fromUtf8("saveDataButton"))
        self.saveDataButton.setMinimumSize(QtCore.QSize(100, 100))
        self.saveDataHBox.addWidget(self.saveDataButton)
        self.mainBox.addLayout(self.plotHBox)
        self.mainBox.addWidget(self.filterGroupBox)
        self.mainBox.addLayout(self.numShotsHBox)
        self.mainBox.addLayout(self.bunchChargeHBox)
        self.mainBox.addLayout(self.saveDataHBox)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Beam loss monitor monitor", None))
        self.numShotsOutputWidget.setPlainText(_translate("MainWindow", "2", None))
        self.filterSizeOutputWidget.setPlainText(_translate("MainWindow", "1", None))
        self.setNumShotsButton.setText(_translate("MainWindow", "Set num shots", None))
        self.numShotsLabel.setText(_translate("MainWindow", "# Shots", None))
        self.saveDataButton.setText(_translate("MainWindow", "Save data", None))
        self.filterYesButton.setText(_translate("MainWindow", "Filter", None))
        self.filterNoButton.setText(_translate("MainWindow", "No filter", None))
        self.filterSizeLabel.setText(_translate("MainWindow", "Filter size", None))
        # self.MainWindow.setTabText(self.MainWindow.indexOf(self.tab), _translate("MainWindow", "Settings", None))
        self.newFont = QtGui.QFont("Comic Sans", 20, QtGui.QFont.Bold)

    def closeEvent(self, event):
        self.closing.emit()