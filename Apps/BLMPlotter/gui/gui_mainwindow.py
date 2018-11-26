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
        self.radioButtonHBoxLayout.setObjectName(_fromUtf8("radioButtonHBoxLayout"))
        self.filterHBoxLayout = QtGui.QHBoxLayout()
        self.filterHBoxLayout.setObjectName(_fromUtf8("filterHBoxLayout"))
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
        self.filterHBoxLayout.addWidget(self.filterYesButton)
        self.filterHBoxLayout.addWidget(self.filterNoButton)
        self.filterSizeLabel = QtGui.QLabel()
        self.filterSizeLabel.setObjectName(_fromUtf8("filterSizeLabel"))
        self.filterSizeOutputWidget = QtGui.QPlainTextEdit()
        self.filterSizeOutputWidget.setObjectName(_fromUtf8("filterSizeOutputWidget"))
        self.filterGroupBox.setMinimumSize(QtCore.QSize(700, 50))
        self.filterGroupBox.setMaximumSize(QtCore.QSize(700, 50))
        self.filterSizeOutputWidget.setMinimumSize(QtCore.QSize(50, 25))
        self.filterSizeOutputWidget.setMaximumSize(QtCore.QSize(50, 25))
        self.filterHBoxLayout.addWidget(self.filterSizeOutputWidget)
        self.filterHBoxLayout.addWidget(self.filterSizeLabel)
        self.calibrateHBoxLayout = QtGui.QHBoxLayout()
        self.calibrateHBoxLayout.setObjectName(_fromUtf8("calibrateHBoxLayout"))
        self.channelNamesGroupBox = QtGui.QGroupBox()
        self.channelNamesComboBox1 = QtGui.QComboBox(self.channelNamesGroupBox)
        self.channelNamesComboBox1.setObjectName(_fromUtf8("comboBox"))
        self.channelNamesComboBox1.addItem("CH1")
        self.channelNamesComboBox1.addItem("CH2")
        self.channelNamesComboBox1.addItem("CH3")
        self.channelNamesComboBox1.addItem("CH4")
        self.channelNamesComboBox1.update()
        self.channelNamesComboBox2 = QtGui.QComboBox(self.channelNamesGroupBox)
        self.channelNamesComboBox2.setObjectName(_fromUtf8("comboBox"))
        self.channelNamesComboBox2.addItem("CH1")
        self.channelNamesComboBox2.addItem("CH2")
        self.channelNamesComboBox2.addItem("CH3")
        self.channelNamesComboBox2.addItem("CH4")
        self.channelNamesComboBox2.update()
        self.channelNamesComboBox1.setMaximumSize(QtCore.QSize(100, 20))
        self.channelNamesComboBox2.setMaximumSize(QtCore.QSize(100, 20))
        self.channelNamesGroupBox.setMinimumSize(QtCore.QSize(600, 50))
        self.channelNamesGroupBox.setMaximumSize(QtCore.QSize(600, 50))
        self.calibrateButton = QtGui.QPushButton()
        self.calibrateButton.setObjectName(_fromUtf8("calibrateButton"))
        self.calibrateButton.setMaximumSize(QtCore.QSize(100, 30))
        self.calibrateHBoxLayout.addWidget(self.channelNamesComboBox1)
        self.calibrateHBoxLayout.addWidget(self.channelNamesComboBox2)
        self.calibrateHBoxLayout.addWidget(self.calibrateButton)
        self.filterGroupBox.setLayout(self.filterHBoxLayout)
        self.channelNamesGroupBox.setLayout(self.calibrateHBoxLayout)
        self.radioButtonHBoxLayout.addWidget(self.filterGroupBox)
        self.radioButtonHBoxLayout.addWidget(self.channelNamesGroupBox)
        self.numShotsHBox = QtGui.QHBoxLayout()
        self.ch1CheckBox = QtGui.QCheckBox()
        self.ch2CheckBox = QtGui.QCheckBox()
        self.ch3CheckBox = QtGui.QCheckBox()
        self.ch4CheckBox = QtGui.QCheckBox()
        self.checkboxes = [self.ch1CheckBox,self.ch2CheckBox,self.ch3CheckBox,self.ch4CheckBox]
        self.rollingAverageButton = QtGui.QPushButton()
        self.rollingAverageButton.setObjectName(_fromUtf8("setNumShotsButton"))
        self.rollingAverageButton.setMinimumSize(QtCore.QSize(60, 40))
        self.numShotsLabel = QtGui.QLabel()
        self.numShotsLabel.setObjectName(_fromUtf8("numShotsLabel"))
        self.setNumShotsButton = QtGui.QPushButton()
        self.setNumShotsButton.setObjectName(_fromUtf8("setNumShotsButton"))
        self.setNumShotsButton.setMinimumSize(QtCore.QSize(60, 40))
        self.numShotsOutputWidget = QtGui.QPlainTextEdit()
        self.numShotsOutputWidget.setObjectName(_fromUtf8("numShotsOutputWidget"))
        self.numShotsOutputWidget.setMinimumSize(QtCore.QSize(30,30))
        self.numShotsOutputWidget.setMaximumSize(QtCore.QSize(30,30))
        self.numShotsHBox.addWidget(self.ch1CheckBox)
        self.numShotsHBox.addWidget(self.ch2CheckBox)
        self.numShotsHBox.addWidget(self.ch3CheckBox)
        self.numShotsHBox.addWidget(self.ch4CheckBox)
        self.numShotsHBox.addWidget(self.numShotsLabel)
        self.numShotsHBox.addWidget(self.numShotsOutputWidget)
        self.numShotsHBox.addWidget(self.setNumShotsButton)
        self.numShotsHBox.addWidget(self.rollingAverageButton)
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
        self.mainBox.addLayout(self.radioButtonHBoxLayout)
        self.mainBox.addLayout(self.numShotsHBox)
        self.mainBox.addLayout(self.bunchChargeHBox)
        self.mainBox.addLayout(self.saveDataHBox)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Beam loss monitor monitor", None))
        self.numShotsOutputWidget.setPlainText(_translate("MainWindow", "20", None))
        self.filterSizeOutputWidget.setPlainText(_translate("MainWindow", "1", None))
        self.rollingAverageButton.setText(_translate("MainWindow", "Set rolling average", None))
        self.setNumShotsButton.setText(_translate("MainWindow", "Set num shots", None))
        self.filterGroupBox.setTitle(_translate("MainWindow", "Filter settings", None))
        self.channelNamesGroupBox.setTitle(_translate("MainWindow", "Calibration measurement", None))
        self.numShotsLabel.setText(_translate("MainWindow", "# Shots", None))
        self.saveDataButton.setText(_translate("MainWindow", "Save data", None))
        self.calibrateButton.setText(_translate("MainWindow", "Calibrate", None))
        self.filterYesButton.setText(_translate("MainWindow", "Filter", None))
        self.filterNoButton.setText(_translate("MainWindow", "No filter", None))
        self.filterSizeLabel.setText(_translate("MainWindow", "Filter size", None))
        self.ch1CheckBox.setText(_translate("MainWindow", "CH1", None))
        self.ch2CheckBox.setText(_translate("MainWindow", "CH2", None))
        self.ch3CheckBox.setText(_translate("MainWindow", "CH3", None))
        self.ch4CheckBox.setText(_translate("MainWindow", "CH4", None))
        # self.MainWindow.setTabText(self.MainWindow.indexOf(self.tab), _translate("MainWindow", "Settings", None))
        self.newFont = QtGui.QFont("Comic Sans", 20, QtGui.QFont.Bold)

    def closeEvent(self, event):
        self.closing.emit()