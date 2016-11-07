# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI_v4.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

import sys	


from PyQt4 import QtCore, QtGui

import imageAnalyser as IA

import pyqtgraph as pg
import pyqtgraph.exporters
import numpy as np
import math as m
import time
import matplotlib
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import scipy.optimize as opt
import lmfit


import ConfigParser

image = IA.imageAnalyser()


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
	#bools for check boxes
    showOrigImageCheck = False
    showSatPixCheck = False
    bkgrndImageCheck = False
    showDirectFitCheck = False
    show1DFitsCheck = False
    showParamsInMMCheck = False
	#BVN PARAM
    muX = 0 
    muY = 0
    sX = 0
    sY = 0
    sXY = 0
    rho = 0
    #DIRECT PARAM
    muXD = 0 
    muYD = 0
    sXD = 0
    sYD = 0
    sXYD = 0
    rhoD = 0
	#1D ESTIMATE OF PARAM
    muX1D = 0
    sX1D = 0
    muY1D = 0
    sY1D = 0
	
    ptmRatio = 1
    satValES = 4095
    satVAlCheck = False
    defaultSatVal=4095
	
    showCrosshairsAndContours = False
    updateGraphImage = False
    pixVals=[]
	
	#arrays for batches of images
    batchImages=[]
    batchBackgroundImages=[]
	#This bit is disgusting as made by Qt Developer and setups up the layout of the GUI
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1350, 856)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(91, 91, 91))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(131, 131, 131))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.NoRole, brush)
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(91, 91, 91))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(131, 131, 131))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.NoRole, brush)
        brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(91, 91, 91))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(51, 153, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(131, 131, 131))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.NoRole, brush)
        MainWindow.setPalette(palette)
        MainWindow.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet(_fromUtf8("QToolTip\n"
		"{\n"
		"     border: 1px solid black;\n"
		"     background-color: #ffa02f;\n"
		"     padding: 1px;\n"
		"     border-radius: 3px;\n"
		"     opacity: 100;\n"
		"}\n"
		"\n"
		"QWidget\n"
		"{\n"
		"    color: #b1b1b1;\n"
		"    background-color: #323232;\n"
		"}\n"
		"\n"
		"QWidget:item:hover\n"
		"{\n"
		"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #ca0619);\n"
		"    color: #000000;\n"
		"}\n"
		"\n"
		"QWidget:item:selected\n"
		"{\n"
		"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
		"}\n"
		"\n"
		"QMenuBar::item\n"
		"{\n"
		"    background: transparent;\n"
		"}\n"
		"\n"
		"QMenuBar::item:selected\n"
		"{\n"
		"    background: transparent;\n"
		"    border: 1px solid #ffaa00;\n"
		"}\n"
		"\n"
		"QMenuBar::item:pressed\n"
		"{\n"
		"    background: #444;\n"
		"    border: 1px solid #000;\n"
		"    background-color: QLinearGradient(\n"
		"        x1:0, y1:0,\n"
		"        x2:0, y2:1,\n"
		"        stop:1 #212121,\n"
		"        stop:0.4 #343434/*,\n"
		"        stop:0.2 #343434,\n"
		"        stop:0.1 #ffaa00*/\n"
		"    );\n"
		"    margin-bottom:-1px;\n"
		"    padding-bottom:1px;\n"
		"}\n"
		"\n"
		"QMenu\n"
		"{\n"
		"    border: 1px solid #000;\n"
		"}\n"
		"\n"
		"QMenu::item\n"
		"{\n"
		"    padding: 2px 20px 2px 20px;\n"
		"}\n"
		"\n"
		"QMenu::item:selected\n"
		"{\n"
		"    color: #000000;\n"
		"}\n"
		"\n"
		"QWidget:disabled\n"
		"{\n"
		"    color: #404040;\n"
		"    background-color: #323232;\n"
		"}\n"
		"\n"
		"QAbstractItemView\n"
		"{\n"
		"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0.1 #646464, stop: 1 #5d5d5d);\n"
		"}\n"
		"\n"
		"QWidget:focus\n"
		"{\n"
		"    /*border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);*/\n"
		"}\n"
		"\n"
		"QLineEdit\n"
		"{\n"
		"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0 #646464, stop: 1 #5d5d5d);\n"
		"    padding: 1px;\n"
		"    border-style: solid;\n"
		"    border: 1px solid #1e1e1e;\n"
		"    border-radius: 5;\n"
		"}\n"
		"\n"
		"QPushButton\n"
		"{\n"
		"    color: #b1b1b1;\n"
		"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);\n"
		"    border-width: 1px;\n"
		"    border-color: #1e1e1e;\n"
		"    border-style: solid;\n"
		"    border-radius: 6;\n"
		"    padding: 3px;\n"
		"    font-size: 12px;\n"
		"    padding-left: 5px;\n"
		"    padding-right: 5px;\n"
		"}\n"
		"\n"
		"QPushButton:pressed\n"
		"{\n"
		"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);\n"
		"}\n"
		"\n"
		"QComboBox\n"
		"{\n"
		"    selection-background-color: #ffaa00;\n"
		"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);\n"
		"    border-style: solid;\n"
		"    border: 1px solid #1e1e1e;\n"
		"    border-radius: 5;\n"
		"}\n"
		"\n"
		"QComboBox:hover,QPushButton:hover\n"
		"{\n"
		"    border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
		"}\n"
		"\n"
		"\n"
		"QComboBox:on\n"
		"{\n"
		"    padding-top: 3px;\n"
		"    padding-left: 4px;\n"
		"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);\n"
		"    selection-background-color: #ffaa00;\n"
		"}\n"
		"\n"
		"QComboBox QAbstractItemView\n"
		"{\n"
		"    border: 2px solid darkgray;\n"
		"    selection-background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
		"}\n"
		"\n"
		"QComboBox::drop-down\n"
		"{\n"
		"     subcontrol-origin: padding;\n"
		"     subcontrol-position: top right;\n"
		"     width: 15px;\n"
		"\n"
		"     border-left-width: 0px;\n"
		"     border-left-color: darkgray;\n"
		"     border-left-style: solid; /* just a single line */\n"
		"     border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
		"     border-bottom-right-radius: 3px;\n"
		" }\n"
		"\n"
		"QComboBox::down-arrow\n"
		"{\n"
		"     image: url(:/down_arrow.png);\n"
		"}\n"
		"\n"
		"QGroupBox:focus\n"
		"{\n"
		"border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
		"}\n"
		"\n"
		"QTextEdit:focus\n"
		"{\n"
		"    border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
		"}\n"
		"\n"
		"QScrollBar:horizontal {\n"
		"     border: 1px solid #222222;\n"
		"     background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0.0 #121212, stop: 0.2 #282828, stop: 1 #484848);\n"
		"     height: 7px;\n"
		"     margin: 0px 16px 0 16px;\n"
		"}\n"
		"\n"
		"QScrollBar::handle:horizontal\n"
		"{\n"
		"      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 0.5 #d7801a, stop: 1 #ffa02f);\n"
		"      min-height: 20px;\n"
		"      border-radius: 2px;\n"
		"}\n"
		"\n"
		"QScrollBar::add-line:horizontal {\n"
		"      border: 1px solid #1b1b19;\n"
		"      border-radius: 2px;\n"
		"      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
		"      width: 14px;\n"
		"      subcontrol-position: right;\n"
		"      subcontrol-origin: margin;\n"
		"}\n"
		"\n"
		"QScrollBar::sub-line:horizontal {\n"
		"      border: 1px solid #1b1b19;\n"
		"      border-radius: 2px;\n"
		"      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
		"      width: 14px;\n"
		"     subcontrol-position: left;\n"
		"     subcontrol-origin: margin;\n"
		"}\n"
		"\n"
		"QScrollBar::right-arrow:horizontal, QScrollBar::left-arrow:horizontal\n"
		"{\n"
		"      border: 1px solid black;\n"
		"      width: 1px;\n"
		"      height: 1px;\n"
		"      background: white;\n"
		"}\n"
		"\n"
		"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
		"{\n"
		"      background: none;\n"
		"}\n"
		"\n"
		"QScrollBar:vertical\n"
		"{\n"
		"      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0.0 #121212, stop: 0.2 #282828, stop: 1 #484848);\n"
		"      width: 7px;\n"
		"      margin: 16px 0 16px 0;\n"
		"      border: 1px solid #222222;\n"
		"}\n"
		"\n"
		"QScrollBar::handle:vertical\n"
		"{\n"
		"      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 0.5 #d7801a, stop: 1 #ffa02f);\n"
		"      min-height: 20px;\n"
		"      border-radius: 2px;\n"
		"}\n"
		"\n"
		"QScrollBar::add-line:vertical\n"
		"{\n"
		"      border: 1px solid #1b1b19;\n"
		"      border-radius: 2px;\n"
		"      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
		"      height: 14px;\n"
		"      subcontrol-position: bottom;\n"
		"      subcontrol-origin: margin;\n"
		"}\n"
		"\n"
		"QScrollBar::sub-line:vertical\n"
		"{\n"
		"      border: 1px solid #1b1b19;\n"
		"      border-radius: 2px;\n"
		"      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #d7801a, stop: 1 #ffa02f);\n"
		"      height: 14px;\n"
		"      subcontrol-position: top;\n"
		"      subcontrol-origin: margin;\n"
		"}\n"
		"\n"
		"QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical\n"
		"{\n"
		"      border: 1px solid black;\n"
		"      width: 1px;\n"
		"      height: 1px;\n"
		"      background: white;\n"
		"}\n"
		"\n"
		"\n"
		"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical\n"
		"{\n"
		"      background: none;\n"
		"}\n"
		"\n"
		"QTextEdit\n"
		"{\n"
		"    background-color: #242424;\n"
		"}\n"
		"\n"
		"QPlainTextEdit\n"
		"{\n"
		"    background-color: #242424;\n"
		"}\n"
		"\n"
		"QHeaderView::section\n"
		"{\n"
		"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #616161, stop: 0.5 #505050, stop: 0.6 #434343, stop:1 #656565);\n"
		"    color: white;\n"
		"    padding-left: 4px;\n"
		"    border: 1px solid #6c6c6c;\n"
		"}\n"
		"\n"
		"QCheckBox:disabled\n"
		"{\n"
		"color: #414141;\n"
		"}\n"
		"\n"
		"QDockWidget::title\n"
		"{\n"
		"    text-align: center;\n"
		"    spacing: 3px; /* spacing between items in the tool bar */\n"
		"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #323232, stop: 0.5 #242424, stop:1 #323232);\n"
		"}\n"
		"\n"
		"QDockWidget::close-button, QDockWidget::float-button\n"
		"{\n"
		"    text-align: center;\n"
		"    spacing: 1px; /* spacing between items in the tool bar */\n"
		"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #323232, stop: 0.5 #242424, stop:1 #323232);\n"
		"}\n"
		"\n"
		"QDockWidget::close-button:hover, QDockWidget::float-button:hover\n"
		"{\n"
		"    background: #242424;\n"
		"}\n"
		"\n"
		"QDockWidget::close-button:pressed, QDockWidget::float-button:pressed\n"
		"{\n"
		"    padding: 1px -1px -1px 1px;\n"
		"}\n"
		"\n"
		"QMainWindow::separator\n"
		"{\n"
		"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #161616, stop: 0.5 #151515, stop: 0.6 #212121, stop:1 #343434);\n"
		"    color: white;\n"
		"    padding-left: 4px;\n"
		"    border: 1px solid #4c4c4c;\n"
		"    spacing: 3px; /* spacing between items in the tool bar */\n"
		"}\n"
		"\n"
		"QMainWindow::separator:hover\n"
		"{\n"
		"\n"
		"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #d7801a, stop:0.5 #b56c17 stop:1 #ffa02f);\n"
		"    color: white;\n"
		"    padding-left: 4px;\n"
		"    border: 1px solid #6c6c6c;\n"
		"    spacing: 3px; /* spacing between items in the tool bar */\n"
		"}\n"
		"\n"
		"QToolBar::handle\n"
		"{\n"
		"     spacing: 3px; /* spacing between items in the tool bar */\n"
		"     background: url(:/images/handle.png);\n"
		"}\n"
		"\n"
		"QMenu::separator\n"
		"{\n"
		"    height: 2px;\n"
		"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #161616, stop: 0.5 #151515, stop: 0.6 #212121, stop:1 #343434);\n"
		"    color: white;\n"
		"    padding-left: 4px;\n"
		"    margin-left: 10px;\n"
		"    margin-right: 5px;\n"
		"}\n"
		"\n"
		"QProgressBar\n"
		"{\n"
		"    border: 2px solid grey;\n"
		"    border-radius: 5px;\n"
		"    text-align: center;\n"
		"}\n"
		"\n"
		"QProgressBar::chunk\n"
		"{\n"
		"    background-color: #d7801a;\n"
		"    width: 2.15px;\n"
		"    margin: 0.5px;\n"
		"}\n"
		"\n"
		"QTabBar::tab {\n"
		"    color: #b1b1b1;\n"
		"    border: 1px solid #444;\n"
		"    border-bottom-style: none;\n"
		"    background-color: #323232;\n"
		"    padding-left: 10px;\n"
		"    padding-right: 10px;\n"
		"    padding-top: 3px;\n"
		"    padding-bottom: 2px;\n"
		"    margin-right: -1px;\n"
		"}\n"
		"\n"
		"QTabWidget::pane {\n"
		"    border: 1px solid #444;\n"
		"    top: 1px;\n"
		"}\n"
		"\n"
		"QTabBar::tab:last\n"
		"{\n"
		"    margin-right: 0; /* the last selected tab has nothing to overlap with on the right */\n"
		"    border-top-right-radius: 3px;\n"
		"}\n"
		"\n"
		"QTabBar::tab:first:!selected\n"
		"{\n"
		" margin-left: 0px; /* the last selected tab has nothing to overlap with on the right */\n"
		"\n"
		"\n"
		"    border-top-left-radius: 3px;\n"
		"}\n"
		"\n"
		"QTabBar::tab:!selected\n"
		"{\n"
		"    color: #b1b1b1;\n"
		"    border-bottom-style: solid;\n"
		"    margin-top: 3px;\n"
		"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:1 #212121, stop:.4 #343434);\n"
		"}\n"
		"\n"
		"QTabBar::tab:selected\n"
		"{\n"
		"    border-top-left-radius: 3px;\n"
		"    border-top-right-radius: 3px;\n"
		"    margin-bottom: 0px;\n"
		"}\n"
		"\n"
		"QTabBar::tab:!selected:hover\n"
		"{\n"
		"    /*border-top: 2px solid #ffaa00;\n"
		"    padding-bottom: 3px;*/\n"
		"    border-top-left-radius: 3px;\n"
		"    border-top-right-radius: 3px;\n"
		"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:1 #212121, stop:0.4 #343434, stop:0.2 #343434, stop:0.1 #ffaa00);\n"
		"}\n"
		"\n"
		"QRadioButton::indicator:checked, QRadioButton::indicator:unchecked{\n"
		"    color: #b1b1b1;\n"
		"    background-color: #323232;\n"
		"    border: 1px solid #b1b1b1;\n"
		"    border-radius: 6px;\n"
		"}\n"
		"\n"
		"QRadioButton::indicator:checked\n"
		"{\n"
		"    background-color: qradialgradient(\n"
		"        cx: 0.5, cy: 0.5,\n"
		"        fx: 0.5, fy: 0.5,\n"
		"        radius: 1.0,\n"
		"        stop: 0.25 #ffaa00,\n"
		"        stop: 0.3 #323232\n"
		"    );\n"
		"}\n"
		"\n"
		"QCheckBox::indicator{\n"
		"    color: #b1b1b1;\n"
		"    background-color: #323232;\n"
		"    border: 1px solid #b1b1b1;\n"
		"    width: 9px;\n"
		"    height: 9px;\n"
		"}\n"
		"\n"
		"QRadioButton::indicator\n"
		"{\n"
		"    border-radius: 6px;\n"
		"}\n"
		"\n"
		"QRadioButton::indicator:hover, QCheckBox::indicator:hover\n"
		"{\n"
		"    border: 1px solid #ffaa00;\n"
		"}\n"
		"\n"
		"QCheckBox::indicator:checked\n"
		"{\n"
		"    background-color: qradialgradient(\n"
		"        cx: 0.5, cy: 0.5,\n"
		"        fx: 0.5, fy: 0.5,\n"
		"        radius: 1.0,\n"
		"        stop: 0.25 #ffaa00,\n"
		"        stop: 0.3 #323232\n"
		"    );\n"
		"    image:url(:/images/checkbox.png);\n"
		"}\n"
		"\n"
		"QCheckBox::indicator:disabled, QRadioButton::indicator:disabled\n"
		"{\n"
		"    border: 1px solid #444;\n"
		"}"))
        
		
		#CENTRAL WIDGET  
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
		#TAB
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1341, 751))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.homeTab = QtGui.QWidget()
        self.homeTab.setObjectName(_fromUtf8("homeTab"))
		
		#GRAPHICS VIEW			
        self.graphs = pg.GraphicsView(self.homeTab)
        self.graphs.setGeometry(QtCore.QRect(250, 10, 1081, 711))
        self.graphs.setObjectName(_fromUtf8("graphicsView"))
        glayout = pg.GraphicsLayout(border=(200,200,200))
        self.graphs.setCentralItem(glayout)
        self.graphs.show()

        global picture, xCrosshair,yCrosshair,projY, projX,img,bimg,bkgrndImage,c1,c2,c3,sat_img,lrx,lry
        picture = glayout.addPlot(row=0,col=0,rowspan=1,colspan=1)	
        projY = glayout.addPlot(row=0, col=2,rowspan=1,colspan=1)		
        projX = glayout.addPlot(col=0,row=2,rowspan=1,colspan=1)
        bkgrndImage = glayout.addPlot(col=2,row=2,rowspan=1,colspan=1,title="BACKGROUND")
        projY.setYLink(picture)
        projX.setXLink(picture)		

        img = pg.ImageItem()
        xCrosshair = picture.plot()
        yCrosshair = picture.plot()	
        c1 = picture.plot()	
        c2 = picture.plot()
        c3 = picture.plot()	
        sat_img = pg.ImageItem()		
        picture.addItem(img)
        picture.addItem(sat_img)
        picture.addItem(xCrosshair)
        picture.addItem(yCrosshair)
        picture.addItem(c1)
        picture.addItem(c2)
        picture.addItem(c3)
        xCrosshair.setZValue(11) 
        yCrosshair.setZValue(11)
        c1.setZValue(10)
        c2.setZValue(10)
        c3.setZValue(10)	
        sat_img.setZValue(5)	
		
		

		

		#SATURATED PIXEL COLOURING
        STEPS = np.array([0.0, 1.0])
        CLRS =           ['w', 'g']    			
        clrmp_sat = pg.ColorMap(STEPS, np.array([pg.colorTuple(pg.Color(c)) for c in CLRS]))
		## Get the LookupTable
        lut_sat = clrmp_sat.getLookupTable()	
        sat_img.setLookupTable(lut_sat)		
		
        bimg = pg.ImageItem()
        bkgrndImage.addItem(bimg)
       
		#ROI for manual cropping
        global roi
        roi = pg.ROI([0,0], [100,100])
        roi.addScaleHandle([0.5, 0], [0.5, 0.5])
        roi.addScaleHandle([1, 0.5], [0.5, 0.5])		
		
		#FIND BEAM
        self.findBeam = QtGui.QPushButton(self.homeTab)
        self.findBeam.setGeometry(QtCore.QRect(10, 10, 231, 71))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        gradient = QtGui.QLinearGradient(0.0, 0.0, 0.0, 1.0)
        gradient.setSpread(QtGui.QGradient.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(86, 86, 86))
        gradient.setColorAt(0.1, QtGui.QColor(82, 82, 82))
        gradient.setColorAt(0.5, QtGui.QColor(78, 78, 78))
        gradient.setColorAt(0.9, QtGui.QColor(74, 74, 74))
        gradient.setColorAt(1.0, QtGui.QColor(70, 70, 70))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        gradient = QtGui.QLinearGradient(0.0, 0.0, 0.0, 1.0)
        gradient.setSpread(QtGui.QGradient.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(86, 86, 86))
        gradient.setColorAt(0.1, QtGui.QColor(82, 82, 82))
        gradient.setColorAt(0.5, QtGui.QColor(78, 78, 78))
        gradient.setColorAt(0.9, QtGui.QColor(74, 74, 74))
        gradient.setColorAt(1.0, QtGui.QColor(70, 70, 70))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        gradient = QtGui.QLinearGradient(0.0, 0.0, 0.0, 1.0)
        gradient.setSpread(QtGui.QGradient.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(86, 86, 86))
        gradient.setColorAt(0.1, QtGui.QColor(82, 82, 82))
        gradient.setColorAt(0.5, QtGui.QColor(78, 78, 78))
        gradient.setColorAt(0.9, QtGui.QColor(74, 74, 74))
        gradient.setColorAt(1.0, QtGui.QColor(70, 70, 70))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        gradient = QtGui.QLinearGradient(0.0, 0.0, 0.0, 1.0)
        gradient.setSpread(QtGui.QGradient.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(86, 86, 86))
        gradient.setColorAt(0.1, QtGui.QColor(82, 82, 82))
        gradient.setColorAt(0.5, QtGui.QColor(78, 78, 78))
        gradient.setColorAt(0.9, QtGui.QColor(74, 74, 74))
        gradient.setColorAt(1.0, QtGui.QColor(70, 70, 70))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        gradient = QtGui.QLinearGradient(0.0, 0.0, 0.0, 1.0)
        gradient.setSpread(QtGui.QGradient.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(86, 86, 86))
        gradient.setColorAt(0.1, QtGui.QColor(82, 82, 82))
        gradient.setColorAt(0.5, QtGui.QColor(78, 78, 78))
        gradient.setColorAt(0.9, QtGui.QColor(74, 74, 74))
        gradient.setColorAt(1.0, QtGui.QColor(70, 70, 70))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        gradient = QtGui.QLinearGradient(0.0, 0.0, 0.0, 1.0)
        gradient.setSpread(QtGui.QGradient.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(86, 86, 86))
        gradient.setColorAt(0.1, QtGui.QColor(82, 82, 82))
        gradient.setColorAt(0.5, QtGui.QColor(78, 78, 78))
        gradient.setColorAt(0.9, QtGui.QColor(74, 74, 74))
        gradient.setColorAt(1.0, QtGui.QColor(70, 70, 70))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.findBeam.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(1)
        self.findBeam.setFont(font)
        self.findBeam.setObjectName(_fromUtf8("findBeam"))
        self.findBeam.clicked.connect(self.getBeamParameters)		

		#PARAMETERS DISPLAY		
        self.beamInfoDisplay = QtGui.QLabel(self.homeTab)
        self.beamInfoDisplay.setGeometry(QtCore.QRect(10, 300, 231, 131))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.beamInfoDisplay.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.beamInfoDisplay.setFont(font)
        self.beamInfoDisplay.setObjectName(_fromUtf8("beamInfoDisplay"))
		
		#CHECKBOXES ON HOME TAB
        self.groupBoxForChecks = QtGui.QGroupBox(self.homeTab)
        self.groupBoxForChecks.setGeometry(QtCore.QRect(10, 90, 231, 191))
        self.groupBoxForChecks.setTitle(_fromUtf8(""))
        self.groupBoxForChecks.setObjectName(_fromUtf8("groupBoxForChecks"))
		#BACKGROUND SUB
        self.subtractBackground = QtGui.QCheckBox(self.groupBoxForChecks)
        self.subtractBackground.setGeometry(QtCore.QRect(10, 10, 171, 17))
        self.subtractBackground.setObjectName(_fromUtf8("subtractBackground"))
        self.subtractBackground.stateChanged.connect(self.subBackground)
		#SHOW ORIGINAL IMAGE 
        self.showOriginalImage = QtGui.QCheckBox(self.groupBoxForChecks)
        self.showOriginalImage.setGeometry(QtCore.QRect(10, 30, 141, 17))
        self.showOriginalImage.setObjectName(_fromUtf8("showOriginalImage"))
        self.showOriginalImage.stateChanged.connect(self.originalImage)
		#HIGHLIGHT THE SATURATED PIXELS
        self.highlightSatPix = QtGui.QCheckBox(self.groupBoxForChecks)
        self.highlightSatPix.setGeometry(QtCore.QRect(10, 50, 191, 17))
        self.highlightSatPix.setObjectName(_fromUtf8("highlightSatPix"))
        self.highlightSatPix.stateChanged.connect(self.saturatedPix)
		#USE MANUAL CROP		
        self.useManualCrop = QtGui.QCheckBox(self.groupBoxForChecks)
        self.useManualCrop.setGeometry(QtCore.QRect(10, 70, 211, 17))
        self.useManualCrop.setObjectName(_fromUtf8("useManualCrop"))
        self.useManualCrop.stateChanged.connect(self.manualCrop)
		##SET UNITS FOR PARAM
        self.Unitsmm = QtGui.QCheckBox(self.groupBoxForChecks)
        self.Unitsmm.setGeometry(QtCore.QRect(10, 90, 141, 17))
        self.Unitsmm.setObjectName(_fromUtf8("Unitsmm"))
        self.Unitsmm.stateChanged.connect(self.units)
		#SHOW PROJECTION FITS
        self.showProjFits = QtGui.QCheckBox(self.groupBoxForChecks)
        self.showProjFits.setGeometry(QtCore.QRect(10, 110, 201, 17))
        self.showProjFits.setObjectName(_fromUtf8("checkBox_2"))
        self.showProjFits.stateChanged.connect(self.projFits)
		#SHOW DIRECT FIT
        self.showDirectFit = QtGui.QCheckBox(self.groupBoxForChecks)
        self.showDirectFit.setGeometry(QtCore.QRect(10, 130, 191, 17))
        self.showDirectFit.setObjectName(_fromUtf8("checkBox"))
        self.showDirectFit.stateChanged.connect(self.directFit)		
		
        self.comboBox = QtGui.QComboBox(self.groupBoxForChecks)
        self.comboBox.setGeometry(QtCore.QRect(10, 160, 211, 22))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        gradient = QtGui.QLinearGradient(0.0, 0.0, 0.0, 1.0)
        gradient.setSpread(QtGui.QGradient.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(86, 86, 86))
        gradient.setColorAt(0.1, QtGui.QColor(82, 82, 82))
        gradient.setColorAt(0.5, QtGui.QColor(78, 78, 78))
        gradient.setColorAt(0.9, QtGui.QColor(74, 74, 74))
        gradient.setColorAt(1.0, QtGui.QColor(70, 70, 70))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        gradient = QtGui.QLinearGradient(0.0, 0.0, 0.0, 1.0)
        gradient.setSpread(QtGui.QGradient.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(86, 86, 86))
        gradient.setColorAt(0.1, QtGui.QColor(82, 82, 82))
        gradient.setColorAt(0.5, QtGui.QColor(78, 78, 78))
        gradient.setColorAt(0.9, QtGui.QColor(74, 74, 74))
        gradient.setColorAt(1.0, QtGui.QColor(70, 70, 70))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        gradient = QtGui.QLinearGradient(0.0, 0.0, 0.0, 1.0)
        gradient.setSpread(QtGui.QGradient.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(86, 86, 86))
        gradient.setColorAt(0.1, QtGui.QColor(82, 82, 82))
        gradient.setColorAt(0.5, QtGui.QColor(78, 78, 78))
        gradient.setColorAt(0.9, QtGui.QColor(74, 74, 74))
        gradient.setColorAt(1.0, QtGui.QColor(70, 70, 70))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        gradient = QtGui.QLinearGradient(0.0, 0.0, 0.0, 1.0)
        gradient.setSpread(QtGui.QGradient.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(86, 86, 86))
        gradient.setColorAt(0.1, QtGui.QColor(82, 82, 82))
        gradient.setColorAt(0.5, QtGui.QColor(78, 78, 78))
        gradient.setColorAt(0.9, QtGui.QColor(74, 74, 74))
        gradient.setColorAt(1.0, QtGui.QColor(70, 70, 70))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        gradient = QtGui.QLinearGradient(0.0, 0.0, 0.0, 1.0)
        gradient.setSpread(QtGui.QGradient.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(86, 86, 86))
        gradient.setColorAt(0.1, QtGui.QColor(82, 82, 82))
        gradient.setColorAt(0.5, QtGui.QColor(78, 78, 78))
        gradient.setColorAt(0.9, QtGui.QColor(74, 74, 74))
        gradient.setColorAt(1.0, QtGui.QColor(70, 70, 70))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        gradient = QtGui.QLinearGradient(0.0, 0.0, 0.0, 1.0)
        gradient.setSpread(QtGui.QGradient.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(86, 86, 86))
        gradient.setColorAt(0.1, QtGui.QColor(82, 82, 82))
        gradient.setColorAt(0.5, QtGui.QColor(78, 78, 78))
        gradient.setColorAt(0.9, QtGui.QColor(74, 74, 74))
        gradient.setColorAt(1.0, QtGui.QColor(70, 70, 70))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, brush)
        self.comboBox.setPalette(palette)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8("Fire"))
        self.comboBox.addItem(_fromUtf8("Ice"))
        self.comboBox.addItem(_fromUtf8("Grayscale"))
        self.comboBox.addItem(_fromUtf8("Rainbow"))
        self.comboBox.activated[str].connect(self.style_choice)	
		


		#TEXT DISPLAY		
        self.textDisplay = QtGui.QTextEdit(self.homeTab)
        self.textDisplay.setGeometry(QtCore.QRect(10, 440, 231, 281))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(36, 36, 36))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(36, 36, 36))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(36, 36, 36))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(36, 36, 36))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(177, 177, 177))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(36, 36, 36))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(36, 36, 36))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.textDisplay.setPalette(palette)
        self.textDisplay.setObjectName(_fromUtf8("textDisplay"))
        self.tabWidget.addTab(self.homeTab, _fromUtf8(""))
		
		#EXPERT SETTINGS AND BATCH MODE TAB
        self.expertTab = QtGui.QWidget()
        self.expertTab.setObjectName(_fromUtf8("expertTab"))
        self.batchMode_groupbox = QtGui.QGroupBox(self.expertTab)
        self.batchMode_groupbox.setGeometry(QtCore.QRect(680, 10, 651, 701))
        self.batchMode_groupbox.setObjectName(_fromUtf8("batchMode_groupbox"))
        self.ES_groupbox = QtGui.QGroupBox(self.expertTab)
        self.ES_groupbox.setGeometry(QtCore.QRect(10, 10, 651, 701))
        self.ES_groupbox.setObjectName(_fromUtf8("ES_groupbox"))
		
		
        self.textEdit_Images = QtGui.QTextEdit(self.batchMode_groupbox)
        self.textEdit_Images.setGeometry(QtCore.QRect(20, 140, 291, 251))
        self.textEdit_Images.setObjectName(_fromUtf8("textEdit_Images"))
        self.line_7 = QtGui.QFrame(self.batchMode_groupbox)
        self.line_7.setGeometry(QtCore.QRect(10, 90, 631, 20))
        self.line_7.setFrameShape(QtGui.QFrame.HLine)
        self.line_7.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_7.setObjectName(_fromUtf8("line_7"))
        self.textEdit_BackgroundImages = QtGui.QTextEdit(self.batchMode_groupbox)
        self.textEdit_BackgroundImages.setGeometry(QtCore.QRect(330, 140, 301, 251))
        self.textEdit_BackgroundImages.setObjectName(_fromUtf8("textEdit_BackgroundImages"))
		#LOAD IMAGES BUTTON
        self.loadImagesBtn = QtGui.QPushButton(self.batchMode_groupbox)
        self.loadImagesBtn.setGeometry(QtCore.QRect(20, 110, 81, 23))
        self.loadImagesBtn.setObjectName(_fromUtf8("loadImagesBtn"))
        self.loadImagesBtn.clicked.connect(self.loadImages)	
		
		#LOAD BKGRND IMAGES BUTTON
        self.loadBkgrndImagesBtn = QtGui.QPushButton(self.batchMode_groupbox)
        self.loadBkgrndImagesBtn.setGeometry(QtCore.QRect(330, 110, 151, 23))
        self.loadBkgrndImagesBtn.setObjectName(_fromUtf8("loadBkgrndImagesBtn"))
        self.loadBkgrndImagesBtn.clicked.connect(self.loadBkgrndImages)
		
        self.progressBar_BatchMode = QtGui.QProgressBar(self.batchMode_groupbox)
        self.progressBar_BatchMode.setGeometry(QtCore.QRect(210, 660, 431, 23))
        self.progressBar_BatchMode.setProperty("value", 0)
        self.progressBar_BatchMode.setObjectName(_fromUtf8("progressBar_BatchMode"))


        self.runBatchBtn = QtGui.QPushButton(self.batchMode_groupbox)
        self.runBatchBtn.setGeometry(QtCore.QRect(10, 610, 191, 81))
        self.runBatchBtn.setObjectName(_fromUtf8("runBatchBtn"))
        self.runBatchBtn.clicked.connect(self.runBatchMode)
		
        self.groupBox = QtGui.QGroupBox(self.batchMode_groupbox)
        self.groupBox.setGeometry(QtCore.QRect(210, 409, 421, 241))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.line = QtGui.QFrame(self.groupBox)
        self.line.setGeometry(QtCore.QRect(200, 20, 21, 211))
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.centreMaskLabel_2 = QtGui.QLabel(self.groupBox)
        self.centreMaskLabel_2.setGeometry(QtCore.QRect(10, 20, 131, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.centreMaskLabel_2.setFont(font)
        self.centreMaskLabel_2.setObjectName(_fromUtf8("centreMaskLabel_2"))
        self.OutputFileName_le = QtGui.QLineEdit(self.groupBox)
        self.OutputFileName_le.setGeometry(QtCore.QRect(10, 50, 191, 20))
        self.OutputFileName_le.setObjectName(_fromUtf8("OutputFileName_le"))
        self.centreMaskLabel_3 = QtGui.QLabel(self.groupBox)
        self.centreMaskLabel_3.setGeometry(QtCore.QRect(10, 80, 131, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.centreMaskLabel_3.setFont(font)
        self.centreMaskLabel_3.setObjectName(_fromUtf8("centreMaskLabel_3"))
        self.checkBox_SaveBVN = QtGui.QCheckBox(self.groupBox)
        self.checkBox_SaveBVN.setGeometry(QtCore.QRect(10, 110, 181, 17))
        self.checkBox_SaveBVN.setObjectName(_fromUtf8("checkBox_SaveBVN"))
        self.checkBox_SaveDirect = QtGui.QCheckBox(self.groupBox)
        self.checkBox_SaveDirect.setGeometry(QtCore.QRect(10, 130, 181, 17))
        self.checkBox_SaveDirect.setObjectName(_fromUtf8("checkBox_SaveDirect"))
        self.checkBox_Save1D = QtGui.QCheckBox(self.groupBox)
        self.checkBox_Save1D.setGeometry(QtCore.QRect(10, 150, 181, 17))
        self.checkBox_Save1D.setObjectName(_fromUtf8("checkBox_Save1D"))
        #self.checkBox_SaveErrors = QtGui.QCheckBox(self.groupBox)
        #self.checkBox_SaveErrors.setGeometry(QtCore.QRect(10, 170, 121, 17))
        #self.checkBox_SaveErrors.setObjectName(_fromUtf8("checkBox_SaveErrors"))
        #self.checkBox_SaveGraphNames = QtGui.QCheckBox(self.groupBox)
        #self.checkBox_SaveGraphNames.setGeometry(QtCore.QRect(10, 190, 191, 17))
        #self.checkBox_SaveGraphNames.setObjectName(_fromUtf8("checkBox_SaveGraphNames"))
        self.centreMaskLabel_4 = QtGui.QLabel(self.groupBox)
        self.centreMaskLabel_4.setGeometry(QtCore.QRect(220, 20, 131, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.centreMaskLabel_4.setFont(font)
        self.centreMaskLabel_4.setObjectName(_fromUtf8("centreMaskLabel_4"))
        self.checkBox_ImageSave = QtGui.QCheckBox(self.groupBox)
        self.checkBox_ImageSave.setGeometry(QtCore.QRect(220, 50, 181, 17))
        self.checkBox_ImageSave.setObjectName(_fromUtf8("checkBox_ImageSave"))
        self.checkBox_XProjSave = QtGui.QCheckBox(self.groupBox)
        self.checkBox_XProjSave.setGeometry(QtCore.QRect(220, 70, 181, 17))
        self.checkBox_XProjSave.setObjectName(_fromUtf8("checkBox_XProjSave"))
        self.checkBox_YProjSave = QtGui.QCheckBox(self.groupBox)
        self.checkBox_YProjSave.setGeometry(QtCore.QRect(220, 90, 181, 17))
        self.checkBox_YProjSave.setObjectName(_fromUtf8("checkBox_YProjSave"))
        self.centreMaskLabel_5 = QtGui.QLabel(self.groupBox)
        self.centreMaskLabel_5.setGeometry(QtCore.QRect(220, 120, 131, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.centreMaskLabel_5.setFont(font)
        self.centreMaskLabel_5.setObjectName(_fromUtf8("centreMaskLabel_5"))
        self.checkBox_SaveAsPNG = QtGui.QCheckBox(self.groupBox)
        self.checkBox_SaveAsPNG.setGeometry(QtCore.QRect(220, 150, 70, 17))
        self.checkBox_SaveAsPNG.setObjectName(_fromUtf8("checkBox_SaveAsPNG"))
        self.checkBox_SaveAsSVG = QtGui.QCheckBox(self.groupBox)
        self.checkBox_SaveAsSVG.setGeometry(QtCore.QRect(220, 170, 70, 17))
        self.checkBox_SaveAsSVG.setObjectName(_fromUtf8("checkBox_SaveAsSVG"))
        self.checkBox_SaveAsCSV = QtGui.QCheckBox(self.groupBox)
        self.checkBox_SaveAsCSV.setGeometry(QtCore.QRect(220, 190, 70, 17))
        self.checkBox_SaveAsCSV.setObjectName(_fromUtf8("checkBox_SaveAsCSV"))
		
		
        self.expertSetLoad_Btn = QtGui.QPushButton(self.ES_groupbox)
        self.expertSetLoad_Btn.setGeometry(QtCore.QRect(10, 20, 141, 21))
        self.expertSetLoad_Btn.setObjectName(_fromUtf8("expertSetLoad_Btn"))
        self.expertSetLoad_Btn.clicked.connect(self.loadES)	
        self.expertSetSave_Btn = QtGui.QPushButton(self.ES_groupbox)
        self.expertSetSave_Btn.setGeometry(QtCore.QRect(10, 50, 141, 23))
        self.expertSetSave_Btn.setObjectName(_fromUtf8("expertSetSave_Btn"))
        self.expertSetSave_Btn.clicked.connect(self.saveES)	
        self.line_5 = QtGui.QFrame(self.ES_groupbox)
        self.line_5.setGeometry(QtCore.QRect(10, 100, 631, 20))
        self.line_5.setFrameShape(QtGui.QFrame.HLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName(_fromUtf8("line_5"))
        self.Mask = QtGui.QLabel(self.ES_groupbox)
        self.Mask.setGeometry(QtCore.QRect(10, 90, 111, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Mask.setFont(font)
        self.Mask.setObjectName(_fromUtf8("Mask"))
		#DEFINE A MASK
        self.useMask_checkBox = QtGui.QCheckBox(self.ES_groupbox)
        self.useMask_checkBox.setGeometry(QtCore.QRect(370, 200, 201, 17))
        self.useMask_checkBox.setObjectName(_fromUtf8("useMask_checkBox"))
        self.useMask_checkBox.stateChanged.connect(self.useMaskES)
		
        self.MaskInfo = QtGui.QLabel(self.ES_groupbox)
        self.MaskInfo.setGeometry(QtCore.QRect(10, 110, 631, 41))
        self.MaskInfo.setObjectName(_fromUtf8("MaskInfo"))
		
        self.centreMaskLabel = QtGui.QLabel(self.ES_groupbox)
        self.centreMaskLabel.setGeometry(QtCore.QRect(10, 150, 91, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.centreMaskLabel.setFont(font)
        self.centreMaskLabel.setObjectName(_fromUtf8("centreMaskLabel"))
		
        self.label_36 = QtGui.QLabel(self.ES_groupbox)
        self.label_36.setGeometry(QtCore.QRect(10, 180, 16, 21))
        self.label_36.setObjectName(_fromUtf8("label_36"))
		
        self.maskX_le = QtGui.QLineEdit(self.ES_groupbox)
        self.maskX_le.setGeometry(QtCore.QRect(30, 180, 113, 20))
        self.maskX_le.setObjectName(_fromUtf8("maskX_le"))
		
        self.label_37 = QtGui.QLabel(self.ES_groupbox)
        self.label_37.setGeometry(QtCore.QRect(10, 200, 16, 21))
        self.label_37.setObjectName(_fromUtf8("label_37"))
		
        self.maskY_le = QtGui.QLineEdit(self.ES_groupbox)
        self.maskY_le.setGeometry(QtCore.QRect(30, 200, 113, 20))
        self.maskY_le.setObjectName(_fromUtf8("maskY_le"))
		
        self.label_38 = QtGui.QLabel(self.ES_groupbox)
        self.label_38.setGeometry(QtCore.QRect(220, 180, 16, 21))
        self.label_38.setObjectName(_fromUtf8("label_38"))
		
        self.maskRX_le = QtGui.QLineEdit(self.ES_groupbox)
        self.maskRX_le.setGeometry(QtCore.QRect(240, 180, 113, 20))
        self.maskRX_le.setObjectName(_fromUtf8("maskRX_le"))
		
        self.RadiiMaskLabel = QtGui.QLabel(self.ES_groupbox)
        self.RadiiMaskLabel.setGeometry(QtCore.QRect(220, 150, 91, 31))
		
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.RadiiMaskLabel.setFont(font)
        self.RadiiMaskLabel.setObjectName(_fromUtf8("RadiiMaskLabel"))
		
        self.label_40 = QtGui.QLabel(self.ES_groupbox)
        self.label_40.setGeometry(QtCore.QRect(220, 200, 20, 21))
        self.label_40.setObjectName(_fromUtf8("label_40"))
		
        self.maskRY_le = QtGui.QLineEdit(self.ES_groupbox)
        self.maskRY_le.setGeometry(QtCore.QRect(240, 200, 113, 20))
        self.maskRY_le.setObjectName(_fromUtf8("maskRY_le"))
		
        self.line_6 = QtGui.QFrame(self.ES_groupbox)
        self.line_6.setGeometry(QtCore.QRect(10, 250, 631, 20))
        self.line_6.setFrameShape(QtGui.QFrame.HLine)
        self.line_6.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_6.setObjectName(_fromUtf8("line_6"))
		
        self.ESVariables = QtGui.QLabel(self.ES_groupbox)
        self.ESVariables.setGeometry(QtCore.QRect(10, 240, 291, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.ESVariables.setFont(font)
        self.ESVariables.setObjectName(_fromUtf8("ESVariables"))
		#MANUALY SET PIXELS TO MM
        self.pxtmm_le = QtGui.QLineEdit(self.ES_groupbox)
        self.pxtmm_le.setGeometry(QtCore.QRect(30, 330, 113, 20))
        self.pxtmm_le.setObjectName(_fromUtf8("pxtmm_le"))
		
        self.labelPixToMm = QtGui.QLabel(self.ES_groupbox)
        self.labelPixToMm.setGeometry(QtCore.QRect(10, 310, 111, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelPixToMm.setFont(font)
        self.labelPixToMm.setObjectName(_fromUtf8("labelPixToMm"))
		#MANUALLY ENTER CROP POSITION
        self.ManCropLabel = QtGui.QLabel(self.ES_groupbox)
        self.ManCropLabel.setGeometry(QtCore.QRect(10, 410, 181, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.ManCropLabel.setFont(font)
        self.ManCropLabel.setObjectName(_fromUtf8("ManCropLabel"))
		
        self.label_52 = QtGui.QLabel(self.ES_groupbox)
        self.label_52.setGeometry(QtCore.QRect(10, 430, 16, 21))
        self.label_52.setObjectName(_fromUtf8("label_52"))
		
        self.manCropX_le = QtGui.QLineEdit(self.ES_groupbox)
        self.manCropX_le.setGeometry(QtCore.QRect(30, 430, 113, 20))
        self.manCropX_le.setObjectName(_fromUtf8("manCropX_le"))
	
        self.manCropY_le = QtGui.QLineEdit(self.ES_groupbox)
        self.manCropY_le.setGeometry(QtCore.QRect(30, 450, 113, 20))
        self.manCropY_le.setObjectName(_fromUtf8("manCropY_le"))
		
        self.label_54 = QtGui.QLabel(self.ES_groupbox)
        self.label_54.setGeometry(QtCore.QRect(200, 430, 41, 21))
        self.label_54.setObjectName(_fromUtf8("label_54"))
		
        self.manCropW_le = QtGui.QLineEdit(self.ES_groupbox)
        self.manCropW_le.setGeometry(QtCore.QRect(240, 430, 113, 20))
        self.manCropW_le.setObjectName(_fromUtf8("manCropW_le"))
		
        self.label_55 = QtGui.QLabel(self.ES_groupbox)
        self.label_55.setGeometry(QtCore.QRect(200, 450, 41, 21))
        self.label_55.setObjectName(_fromUtf8("label_55"))
		
        self.manCropH_le = QtGui.QLineEdit(self.ES_groupbox)
        self.manCropH_le.setGeometry(QtCore.QRect(240, 450, 113, 20))
        self.manCropH_le.setObjectName(_fromUtf8("manCropH_le"))
		
		#DETERMINE SATURATED PIXEL VALUE
        self.satPixVal_le = QtGui.QLineEdit(self.ES_groupbox)
        self.satPixVal_le.setGeometry(QtCore.QRect(30, 380, 113, 20))
        self.satPixVal_le.setObjectName(_fromUtf8("satPixVal_le"))
		
        self.label_53 = QtGui.QLabel(self.ES_groupbox)
        self.label_53.setGeometry(QtCore.QRect(10, 450, 16, 21))
        self.label_53.setObjectName(_fromUtf8("label_53"))

        self.SatPixValLabel = QtGui.QLabel(self.ES_groupbox)
        self.SatPixValLabel.setGeometry(QtCore.QRect(10, 360, 191, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.SatPixValLabel.setFont(font)
        self.SatPixValLabel.setObjectName(_fromUtf8("SatPixValLabel"))
		#PTMM
        self.ptmm_checkBox = QtGui.QCheckBox(self.ES_groupbox)
        self.ptmm_checkBox.setGeometry(QtCore.QRect(160, 330, 21, 20))
        self.ptmm_checkBox.setText(_fromUtf8(""))
        self.ptmm_checkBox.setObjectName(_fromUtf8("ptmm_checkBox"))
        self.ptmm_checkBox.stateChanged.connect(self.usePixToMmES)
		#SAT PIXEL		
        self.satPixVal_checkBox = QtGui.QCheckBox(self.ES_groupbox)
        self.satPixVal_checkBox.setGeometry(QtCore.QRect(160, 380, 21, 20))
        self.satPixVal_checkBox.setText(_fromUtf8(""))
        self.satPixVal_checkBox.setObjectName(_fromUtf8("satPixVal_checkBox"))
        self.satPixVal_checkBox.stateChanged.connect(self.useSatValES)		
		#MANUAL CROP
        self.manCrop_checkBox = QtGui.QCheckBox(self.ES_groupbox)
        self.manCrop_checkBox.setGeometry(QtCore.QRect(370, 450, 21, 20))
        self.manCrop_checkBox.setText(_fromUtf8(""))
        self.manCrop_checkBox.setObjectName(_fromUtf8("manCrop_checkBox"))
        self.manCrop_checkBox.stateChanged.connect(self.useManualCropES)
		
        self.ESVariableInfo = QtGui.QLabel(self.ES_groupbox)
        self.ESVariableInfo.setGeometry(QtCore.QRect(10, 260, 631, 41))
        self.ESVariableInfo.setObjectName(_fromUtf8("ESVariableInfo"))
		#SET A SPECIFIC FILTER IN WHICH TO LOOK AT PROJECTIONS WITH
        self.filter_checkBox = QtGui.QCheckBox(self.ES_groupbox)
        self.filter_checkBox.setGeometry(QtCore.QRect(140, 550, 21, 20))
        self.filter_checkBox.setText(_fromUtf8(""))
        self.filter_checkBox.setObjectName(_fromUtf8("filter_checkBox"))
        self.filter_checkBox.stateChanged.connect(self.useFilterES)
		
        self.filter_le = QtGui.QLineEdit(self.ES_groupbox)
        self.filter_le.setGeometry(QtCore.QRect(10, 550, 113, 20))
        self.filter_le.setText(_fromUtf8(""))
        self.filter_le.setObjectName(_fromUtf8("filter_le"))
		
        self.specificFilterLabel = QtGui.QLabel(self.ES_groupbox)
        self.specificFilterLabel.setGeometry(QtCore.QRect(10, 480, 111, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.specificFilterLabel.setFont(font)
        self.specificFilterLabel.setObjectName(_fromUtf8("specificFilterLabel"))
		
        self.specFilterText = QtGui.QLabel(self.ES_groupbox)
        self.specFilterText.setGeometry(QtCore.QRect(10, 500, 631, 41))
        self.specFilterText.setObjectName(_fromUtf8("specFilterText"))
		#MANUALLY SET RR THRESHOLD
        self.RR_checkBox = QtGui.QCheckBox(self.ES_groupbox)
        self.RR_checkBox.setGeometry(QtCore.QRect(370, 330, 21, 20))
        self.RR_checkBox.setText(_fromUtf8(""))
        self.RR_checkBox.setObjectName(_fromUtf8("RR_checkBox"))
        self.RR_checkBox.stateChanged.connect(self.useRRES)
		
        self.RR_le = QtGui.QLineEdit(self.ES_groupbox)
        self.RR_le.setGeometry(QtCore.QRect(240, 330, 113, 20))
        self.RR_le.setObjectName(_fromUtf8("RR_le"))
		
        self.RRLabel = QtGui.QLabel(self.ES_groupbox)
        self.RRLabel.setGeometry(QtCore.QRect(230, 310, 141, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.RRLabel.setFont(font)
        self.RRLabel.setObjectName(_fromUtf8("RRLabel"))
		#MANUALLY SET SIGAM VALUE FOR CUT
        self.sigmaCut_checkBox = QtGui.QCheckBox(self.ES_groupbox)
        self.sigmaCut_checkBox.setGeometry(QtCore.QRect(370, 380, 21, 20))
        self.sigmaCut_checkBox.setText(_fromUtf8(""))
        self.sigmaCut_checkBox.setObjectName(_fromUtf8("sigmaCut_checkBox"))
        self.sigmaCut_checkBox.stateChanged.connect(self.useSigmaCutES)
		
        self.sigmaCut_le = QtGui.QLineEdit(self.ES_groupbox)
        self.sigmaCut_le.setGeometry(QtCore.QRect(240, 380, 113, 20))
        self.sigmaCut_le.setObjectName(_fromUtf8("sigmaCut_le"))
		
        self.sigmCutLabel = QtGui.QLabel(self.ES_groupbox)
        self.sigmCutLabel.setGeometry(QtCore.QRect(230, 360, 111, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.sigmCutLabel.setFont(font)
        self.sigmCutLabel.setObjectName(_fromUtf8("sigmCutLabel"))
		#SET LEVEL WHICH DIRECT METHOD INGORES A PIXEL
        self.directCut_checkBox = QtGui.QCheckBox(self.ES_groupbox)
        self.directCut_checkBox.setGeometry(QtCore.QRect(140, 650, 121, 20))
        self.directCut_checkBox.setText(_fromUtf8(""))
        self.directCut_checkBox.setObjectName(_fromUtf8("directCut_checkBox"))
        self.directCut_checkBox.stateChanged.connect(self.useDirectCutES)
		
        self.directCut_le = QtGui.QLineEdit(self.ES_groupbox)
        self.directCut_le.setGeometry(QtCore.QRect(10, 650, 113, 20))
        self.directCut_le.setText(_fromUtf8(""))
        self.directCut_le.setObjectName(_fromUtf8("directCut_le"))
		
        self.directCutText = QtGui.QLabel(self.ES_groupbox)
        self.directCutText.setGeometry(QtCore.QRect(10, 600, 631, 41))
        self.directCutText.setObjectName(_fromUtf8("directCutText"))
		
        self.batchModeText = QtGui.QLabel(self.batchMode_groupbox)
        self.batchModeText.setGeometry(QtCore.QRect(15, 20, 621, 71))
        self.batchModeText.setObjectName(_fromUtf8("directCutText"))
		
        self.directCutLabel = QtGui.QLabel(self.ES_groupbox)
        self.directCutLabel.setGeometry(QtCore.QRect(10, 580, 181, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.directCutLabel.setFont(font)
        self.directCutLabel.setObjectName(_fromUtf8("directCutLabel"))
		
        self.tabWidget.addTab(self.expertTab, _fromUtf8(""))

		
		#IMAGE STAUS
        self.statusInfo1 = QtGui.QLabel(self.centralwidget)
        self.statusInfo1.setGeometry(QtCore.QRect(10, 760, 1321, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.statusInfo1.setFont(font)
        self.statusInfo1.setObjectName(_fromUtf8("statusInfo1"))
		#BKGRND IMAGE STATUS
        self.statusInfo2 = QtGui.QLabel(self.centralwidget)
        self.statusInfo2.setGeometry(QtCore.QRect(10, 790, 1321, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.statusInfo2.setFont(font)
        self.statusInfo2.setObjectName(_fromUtf8("statusInfo2"))
		
		#MENU BAR AT TOP OF SCREEN		
        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1342, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
		#HAVENT SET THESE
       # self.menuFile = QtGui.QMenu(self.menubar)
       # self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuOpen = QtGui.QMenu(self.menubar)
        self.menuOpen.setObjectName(_fromUtf8("menuOpen"))
        self.menuSave = QtGui.QMenu(self.menubar)
        self.menuSave.setObjectName(_fromUtf8("menuSave"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
		
        #self.actionOpen = QtGui.QAction(MainWindow)
        #self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        #self.actionSave = QtGui.QAction(MainWindow)
        #self.actionSave.setObjectName(_fromUtf8("actionSave"))
		
		#ONE IMAGE
        self.actionImage = QtGui.QAction(MainWindow)
        self.actionImage.setObjectName(_fromUtf8("actionImage"))
        self.actionImage.triggered.connect(self.loadImage)
		#IMAGES
        self.actionIMages = QtGui.QAction(MainWindow)
        self.actionIMages.setObjectName(_fromUtf8("actionIMages"))
        self.actionIMages.triggered.connect(self.loadImages)
		#SAVE BEAM POSITIONS
        self.actionBeam_Positions = QtGui.QAction(MainWindow)
        self.actionBeam_Positions.setObjectName(_fromUtf8("actionBeam_Positions"))
        self.actionBeam_Positions.triggered.connect(self.saveParamters)
		#SET BACKGROUND
        self.actionSet_Backgound = QtGui.QAction(MainWindow)
        self.actionSet_Backgound.setObjectName(_fromUtf8("actionSet_Backgound"))
        self.actionSet_Backgound.triggered.connect(self.loadBackgroundImage)
		#SET BATCH BACKGROUNDS
        self.actionSet_Backgounds = QtGui.QAction(MainWindow)
        self.actionSet_Backgounds.setObjectName(_fromUtf8("actionSet_Backgounds"))
        self.actionSet_Backgounds.triggered.connect(self.loadBkgrndImages)
		
		#SAVE IMAGE
        self.actionSaveImage = QtGui.QAction(MainWindow)
        self.actionSaveImage.setObjectName(_fromUtf8("actionSaveImage"))
        self.actionSaveImage.triggered.connect(self.savePicturePNG)

		#SAVE X PROJECTION
        self.actionSaveXProj = QtGui.QAction(MainWindow)
        self.actionSaveXProj.setObjectName(_fromUtf8("actionSaveXProj"))
        self.actionSaveXProj.triggered.connect(self.saveXProjPNG)
		#SAVE Y PROJECTION
        self.actionSaveYProj = QtGui.QAction(MainWindow)
        self.actionSaveYProj.setObjectName(_fromUtf8("actionSaveYProj"))
        self.actionSaveYProj.triggered.connect(self.saveYProjPNG)
		
		
        #self.menuFile.addAction(self.actionOpen)
        #self.menuFile.addAction(self.actionSave)
        self.menuOpen.addAction(self.actionImage)
        self.menuOpen.addAction(self.actionIMages)
        self.menuOpen.addAction(self.actionSet_Backgound)
        self.menuOpen.addAction(self.actionSet_Backgounds)
        self.menuSave.addAction(self.actionBeam_Positions)
        self.menuSave.addAction(self.actionSaveImage)
        self.menuSave.addAction(self.actionSaveXProj)
        self.menuSave.addAction(self.actionSaveYProj)
        #self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuOpen.menuAction())
        self.menubar.addAction(self.menuSave.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
	
    #Functions  for buttons or options in GUI
    def savePicturePNG(self):
		#using pyqtgraph to export as png
        pg.exporters.ImageExporter(picture).export('IMAGE.png')    
    def saveXProjPNG(self):
	    #using pyqtgraph to export as png
        pg.exporters.ImageExporter(projX).export('X PROJECTION.png')    
    def saveYProjPNG(self):
	    #using pyqtgraph to export as png
        pg.exporters.ImageExporter(projY).export('Y PROJECTION.png')		
    def updateImage(self):#this is the updat the plot items on the graphics view when something has changes
		#clear screens
        sat_img.clear()
        img.clear()
        projY.clear()
        projX.clear()
        size = 1040*1392
        height = 1040
        width = 1392
		#Check whether or not to show original image
        if self.updateGraphImage == True: 	
			if self.showOrigImageCheck==True:	
				#Get and plot image
				self.pixVals = image.getOriginalPixIntensity()
				#plot X proj
				projX.plot(image.getOriginalXProjection())
				c=image.getOriginalYProjection()		
			elif self.showOrigImageCheck==False:
				#Get and plot image
				self.pixVals = image.getPixIntensity()
				size = image.getImageDataSize()
				height = image.getImageHeight()
				width = image.getImageWidth()
				#plot X proj
				projX.plot(image.getXProjection())
				c=image.getYProjection()	
		
		#Get pixel dat into nump array in order to manipulate it
        N = np.zeros(size)	
        for i in range(size):	
            N[i]=self.pixVals[i]	
			
		#Check whether or not to show saturated pixels
        if  self.showSatPixCheck==True:            
            N_sat = np.zeros(size)
            for i in range(size):
                if self.pixVals[i]>=self.satValES:
                    N_sat[i] = 1	
                else:
                    N_sat[i] = 0
			#Show saturated pixel image but at 40% transparency		
            A_sat= np.reshape(N_sat,(height,width)).T
            B_sat = np.fliplr(A_sat)
            sat_img.setImage(B_sat,opacity=0.4)
		
		#Show pixel data on image	
        A = np.reshape(N,(height,width)).T
        B = np.fliplr(A)
        img.setImage(B)
        picture.autoRange()

        #Have to rearrange (rotate) Y projection data abit to plot it well
        a = np.zeros(height)
        b = np.zeros(height)
        for i in range(height):
	        a[i]=i
	        b[i]=c[i]
		#plot
        projY.plot(y=a,x=b)	
        if self.showCrosshairsAndContours==True:
			#Plot and update lines on graph (i.e. contours and crosshairs)
			if self.showDirectFitCheck==False:
				mux = self.muX
				muy = self.muY
				Sx = self.sX
				Sy = self.sY
			else:
				mux = self.muXD
				muy = self.muYD
				Sx = self.sXD
				Sy = self.sYD
			errorX1 = np.array([mux-Sx,mux+Sx])
			errorY1 = np.array([mux,mux])
			errorX2 = np.array([muy,muy])
			errorY2 = np.array([muy-Sy,muy+Sy])
			#adjust position is showing the original image of not
			if self.showOrigImageCheck==False:
				for i in range(2):
					errorX1[i]-=image.getCroppedX()
					errorX2[i]-=image.getCroppedY()
					errorY1[i]-=image.getCroppedX()
					errorY2[i]-=image.getCroppedY()	
			
			#Plot crosshairs on graph		
			xCrosshair.clear()
			yCrosshair.clear()
			xCrosshair.setData(x=errorX1,y=errorX2,pen=(0,0,255))	
			yCrosshair.setData(x=errorY1,y=errorY2, pen=(0,0,255))
			
			#Get contours
			x = np.arange(0, 2000, 1)
			y = np.arange(0, 2000, 1)
			X, Y = np.meshgrid(x, y) 
			 
			if self.showDirectFitCheck==False:
				Z = mlab.bivariate_normal(X, Y,  self.sX,  self.sY, errorY1[0], errorX2[0], sigmaxy=self.sXY)
			else:
				Z = mlab.bivariate_normal(X, Y,  self.sXD,  self.sYD, errorY1[0], errorX2[0], sigmaxy=self.sXYD)
			#Plot contours
			cs = plt.contour(X,Y,Z,3)
			p = cs.collections[0].get_paths()[0]
			v1 = p.vertices
			c1.clear()
			c1.setData(x=v1[:,0],y=v1[:,1],pen=(0,255,0))
			p2 = cs.collections[1].get_paths()[0]
			v2 = p2.vertices
			c2.clear()
			c2.setData(x=v2[:,0],y=v2[:,1],pen=(0,255,0))
			p3 = cs.collections[2].get_paths()[0]
			v3 = p3.vertices
			c3.clear()
			c3.setData(x=v3[:,0],y=v3[:,1],pen=(0,255,0))
			
			#1D Projection Fits/Estimates
			if self.show1DFitsCheck==True:
				#Region indicates 1D estimates of projections
				x_s = self.muX1D-self.sX1D
				xs = self.muX1D+self.sX1D
				y_s = self.muY1D-self.sY1D
				ys = self.muY1D+self.sY1D
				if self.showOrigImageCheck==False:
					x_s -= image.getCroppedX()
					xs -= image.getCroppedX()
					y_s -= image.getCroppedY()
					ys -= image.getCroppedY()	   
				
				lrx = pg.LinearRegionItem([x_s,xs])
				lrx.setZValue(10)
				projX.addItem(lrx)	
				lry = pg.LinearRegionItem([y_s,ys],orientation=pg.LinearRegionItem.Horizontal)
				lry.setZValue(10)
				projY.addItem(lry)	
			
        self.textDisplay.setText("Updated Image and graphs.\n"+self.textDisplay.toPlainText())
    def updateParamLabel(self):
		#check desired units
        if self.showParamsInMMCheck==True:
            self.beamInfoDisplay.setText("\t\t BVN\tDirect"+
            "\nPosition x:\t"+str(round(self.muX/self.ptmRatio,3))+"\t"+str(round(self.muXD/self.ptmRatio,3))+
            "\nPosition y:\t"+str(round(self.muY/self.ptmRatio,3))+"\t"+str(round(self.muYD/self.ptmRatio,3))+
            "\n   Sigma x:\t"+str(round(self.sX/self.ptmRatio,3))+"\t"+str(round(self.sXD/self.ptmRatio,3))+
            "\n   Sigma y:\t"+str(round(self.sY/self.ptmRatio,3))+"\t"+str(round(self.sYD/self.ptmRatio,3))+
            "\n   Cov(xy):\t"+str(round(self.sXY/(self.ptmRatio*self.ptmRatio),3))+"\t"+str(round(self.sXYD/(self.ptmRatio*self.ptmRatio),3))+
            "\n          rho:\t"+str(self.rho)+"\t"+str(self.rhoD))	
        else:
            self.beamInfoDisplay.setText("\t\t BVN\tDirect"+
            "\nPosition x:\t"+str(self.muX)+"\t"+str(self.muXD)+
            "\nPosition y:\t"+str(self.muY)+"\t"+str(self.muYD)+
            "\n   Sigma x:\t"+str(self.sX)+"\t"+str(self.sXD)+
            "\n   Sigma y:\t"+str(self.sY)+"\t"+str(self.sYD)+
            "\n   Cov(xy):\t"+str(self.sXY)+"\t"+str(self.sXYD)+
            "\n          rho:\t"+str(self.rho)+"\t"+str(self.rhoD))				
    def loadBackgroundImage(self):
        fileName = QtGui.QFileDialog.getOpenFileName()
        image.loadBackgroundImageFromFile(str(fileName))
        self.bkgrndImageCheck=True
		#display bkgrnd image
        bimg.clear()
        n_b = image.getBackgroundImage()
        size = 1392*1040
        N = np.zeros(size)
        for i in range(size):
	        N[i] = n_b[i]	
        A = np.reshape(N,(1040,1392)).T
        B = np.fliplr(A)
        bimg.setImage(B)
        bkgrndImage.autoRange()
        self.textDisplay.setText("Loaded Background Image"+self.textDisplay.toPlainText())
        self.statusInfo2.setText("LOADED BACKGROUND IMAGE: "+str(fileName)) 
    def loadImage(self):
		#Choose a file
        fileName = QtGui.QFileDialog.getOpenFileName()
        if fileName == "":
            print("You did not select a file")
            self.textDisplay.setText("You did not select a file\n"+self.textDisplay.toPlainText())
            return
		#clear if these have already been set
        img.clear()
        c1.clear()
        c2.clear()
        c3.clear()
        xCrosshair.clear()
        yCrosshair.clear()
        projY.clear()
        projX.clear()
		
        #load image from file
        start = time.time()
        image.loadImageFromFile(str(fileName))
        end = time.time()
		
        #Get and plot original image
        self.pixVals = image.getOriginalPixIntensity()
        size = 1392*1040
        N = np.zeros(size)
        for i in range(size):
	        N[i] = self.pixVals[i]	
        A = np.reshape(N,(1040,1392)).T
        B = np.fliplr(A)
        img.setImage(B)
        picture.autoRange()

        #Get and plot projections
        c=image.getOriginalYProjection()
        #have to rearrange abit to plot it well
        a = np.zeros(1040)
        b = np.zeros(1040)
        for i in range(1040):
	        a[i]=i
	        b[i]=c[i]
        projY.plot(y=a,x=b)	
        projX.plot(image.getOriginalXProjection())
		
		#set bool such that any crosshair and conour lines wont show up
        self.showCrosshairsAndContours=False
        self.updateGraphImage = False 	
        #set Text in OUT  
        self.statusInfo1.setText("LOADED IMAGE: "+str(fileName))		
        self.textDisplay.setText("Loaded Image in "+str(end-start)+" seconds\n"+self.textDisplay.toPlainText())
        print("Loaded Image")
    def loadImages(self):	
		#clear any names previously stored
        del self.batchImages[:]
		# Make a an array of strings correspond the the image file names
        self.textEdit_Images.setText("")
        fileNames = QtGui.QFileDialog.getOpenFileNames()
        for i in range(fileNames.count()):
			self.batchImages.append(str(fileNames[i]))
			startOfName = str(fileNames[i]).rfind("\\")
			self.textEdit_Images.setText(str(fileNames[i])[startOfName+1:]+"\n"+self.textEdit_Images.toPlainText())
    def loadBkgrndImages(self):	
		#Same as self.loadImages
        del self.batchBackgroundImages[:]
        self.textEdit_BackgroundImages.setText("")
        fileNames = QtGui.QFileDialog.getOpenFileNames()
        for i in range(fileNames.count()):
			self.batchBackgroundImages.append(str(fileNames[i]))
			startOfName = str(fileNames[i]).rfind("\\")
			self.textEdit_BackgroundImages.setText(str(fileNames[i])[startOfName+1:]+"\n"+self.textEdit_BackgroundImages.toPlainText())		
    def runBatchMode(self):
		#used when you press the Run button
        text_file = open(str(self.OutputFileName_le.text()), "w")
        length = len(self.batchImages)

        for i in range(len(self.batchImages)):
			#load image
            image.loadImageFromFile(self.batchImages[i])
			#load background
            if len(self.batchBackgroundImages)==1:
			    image.loadBackgroundImageFromFile(self.batchBackgroundImages[0])	
            elif len(self.batchBackgroundImages)==0:	
                print("no backgrounds set")			
            else:
                image.loadBackgroundImageFromFile(self.batchBackgroundImages[i])
			#analyse
            param = image.getBeamParameters()
            self.graphCatchUp=True
			#set ptm ratio
            self.ptmRatio=image.getPTMRatio()
			
			#PYTHON BVN FITTING
            size = image.getImageDataSize()
            height = image.getImageHeight()
            width = image.getImageWidth()	

            def BVN((x, y),Bk,Amp,mx,my,sx,sy,sxy):
                Bk = float(Bk)
                Amp = float(Amp)
                mx = float(mx)
                my = float(my)
                sx = float(sx)
                sy = float(sy)
                sxy = float(sxy)		
                g = Bk + Amp*np.exp(-0.5*(sy*(x-mx)**2-2*sxy*(x-mx)*(y-my)+sx*(y-my)**2)/(sy*sx-sxy**2))
                return g.ravel()
		    # Create x and y indices
            x = np.linspace(0, width, width)
            y = np.linspace(0, height, height)
            x, y = np.meshgrid(x, y)
            initial_guess = (0,max(image.getPixIntensity()),param[10],param[12],param[11],param[13],0)
            popt, pcov = opt.curve_fit(BVN, (image.getX(), image.getY()), image.getPixIntensity(), p0=initial_guess)
			
			#BVN
            self.muX = round(popt[2]+image.getCroppedX(),3)
            self.muY = round(popt[3]+image.getCroppedY(),3)
            self.sX = round(m.sqrt(popt[4]),3)
            self.sY = round(m.sqrt(popt[5]),3)
            self.sXY = round(popt[6],3)
            self.rho = round(popt[6]/(m.sqrt(popt[4])*m.sqrt(popt[5])),3)
			
			#OPTION TO USE ROOT BVN FIT THEN UNCOMMENT THESE:
			
            # self.muX = round(param[0]/self.ptmRatio,3)
            # self.muY = round(param[1]/self.ptmRatio,3)
            # self.sX = round(m.sqrt(param[2])/self.ptmRatio,3)
            # self.sY = round(m.sqrt(param[3])/self.ptmRatio,3)
            # self.sXY = round(param[4]/(self.ptmRatio*self.ptmRatio),3)
            # self.rho = round(param[4]/(m.sqrt(param[2])*m.sqrt(param[3])),3)

			#Direct
            self.muXD = round(param[5],3)
            self.muYD = round(param[6],3)
            self.sXD = round(m.sqrt(param[7]),3)
            self.sYD = round(m.sqrt(param[8]),3)
            self.sXYD = round(param[9],3)
            self.rhoD = round(param[9]/(m.sqrt(param[7])*m.sqrt(param[8])),3)
		
			#1D Estimates
            self.muX1D = round(param[10],3)+(image.getCroppedX())
            self.muY1D = round(param[12],3)+(image.getCroppedY())
            self.sX1D = round(param[11],3)	
            self.sY1D = round(param[13],3)		

            picture.removeItem(roi)
            self.updateImage()	
			
			
            #OUTPUT DATA
            text_file.write("Image: "+str(self.batchImages[i])+"\n")		
            if len(self.batchBackgroundImages)==1:
    			text_file.write("Background Image: "+str(self.batchBackgroundImages[0])+"\n\n")	
            elif len(self.batchBackgroundImages)==0:	
                text_file.write("Background Image: NONE SET\n\n")			
            else:
                text_file.write("Background Image: "+str(self.batchBackgroundImages[i])+"\n\n")
				
			#SAVE IMAGES
            text_file.write("Images/Files associated with data:\n")
            startOfName = str(self.batchImages[i]).rfind("\\")
            dummyName = str(self.batchImages[i])[startOfName+1:-4]			
			#saving image	
            if self.checkBox_ImageSave.isChecked()==True:	
                if self.checkBox_SaveAsPNG.isChecked()==True:
                    ex = pg.exporters.ImageExporter(picture)
                    ex.export('IMAGE '+dummyName+'.png')
                    text_file.write('IMAGE '+dummyName+'.png\n')
                if self.checkBox_SaveAsSVG.isChecked()==True:
                    ex = pg.exporters.SVGExporter(picture)
                    ex.export('IMAGE '+dummyName+'.svg')
                    text_file.write('IMAGE '+dummyName+'.svg\n')
                if self.checkBox_SaveAsCSV.isChecked()==True:	
                    ex = pg.exporters.CSVExporter(picture)
                    ex.export('IMAGE '+dummyName+'.csv')	
                    text_file.write('IMAGE '+dummyName+'.csv\n')
					
			#saving X Projection		
            if self.checkBox_XProjSave.isChecked()==True:			
                if self.checkBox_SaveAsPNG.isChecked()==True:
                    ex = pg.exporters.ImageExporter(projX)
                    ex.export('PROJ X '+dummyName+'.png')
                    text_file.write('PROJ X '+dummyName+'.png\n')
                if self.checkBox_SaveAsSVG.isChecked()==True:
                    ex = pg.exporters.SVGExporter(projX)
                    ex.export('PROJ X '+dummyName+'.svg')
                    text_file.write('PROJ X '+dummyName+'.svg\n')
                if self.checkBox_SaveAsCSV.isChecked()==True:	
                    ex = pg.exporters.CSVExporter(projX)
                    ex.export('PROJ X '+dummyName+'.csv')	
                    text_file.write('PROJ X '+dummyName+'.csv\n')
					
			#saving Y Projection
            if self.checkBox_YProjSave.isChecked()==True:
                if self.checkBox_SaveAsPNG.isChecked()==True:
                    ex = pg.exporters.ImageExporter(projY)
                    ex.export('PROJ Y '+dummyName+'.png')
                    text_file.write('PROJ Y '+dummyName+'.png\n')
                if self.checkBox_SaveAsSVG.isChecked()==True:
                    ex = pg.exporters.SVGExporter(projY)
                    ex.export('PROJ Y '+dummyName+'.svg')
                    text_file.write('PROJ Y '+dummyName+'.svg\n')
                if self.checkBox_SaveAsCSV.isChecked()==True:	
                    ex = pg.exporters.CSVExporter(projY)
                    ex.export('PROJ Y '+dummyName+'.csv')	
                    text_file.write('PROJ Y '+dummyName+'.csv\n')
			
			#set units of output
            if self.showParamsInMMCheck==True:
                ratio = self.ptmRatio
                text_file.write("\n\nFollowing units are in millimetres\n")
            else:
                ratio = 1
                text_file.write("\n\nFollowing units are in pixels\n")
			#output parameters
            if self.checkBox_SaveBVN.isChecked()==True:			
				text_file.write(
				 "\nBVN Fit:-------------------------------------------------------------"+
				 "\nPosition x: "+str(self.muX/ratio)+
				 "\nPostion y: "+str(self.muY/ratio)+
				 "\nSigma x: "+str(self.sX/ratio)+
				 "\nSigma y: "+str(self.sY/ratio)+
				 "\nCov(xy): "+str(self.sXY/(ratio*ratio))+
				 "\nrho: "+str(self.rho))
            if self.checkBox_SaveDirect.isChecked()==True:	
				text_file.write(
				 "\nCovariance Matrix Fit:-------------------------------------------------------------"+
				 "\nPosition x: "+str(self.muXD/ratio)+
				 "\nPostion y: "+str(self.muYD/ratio)+
				 "\nSigma x: "+str(self.sXD/ratio)+
				 "\nSigma y: "+str(self.sYD/ratio)+
				 "\nCov(xy): "+str(self.sXYD/(ratio*ratio))+
				 "\nrho: "+str(self.rhoD))	
            if self.checkBox_Save1D.isChecked()==True:	
				text_file.write(	 
				 "\n1D Estimates:-------------------------------------------------------------"+
				 "\nPosition x:"+str(self.muX1D/ratio)+
				 "\nPosition y:"+str(self.muY1D/ratio)+
				 "\nSigma x:"+str(self.sX1D/ratio)+
				 "\nSigma y:"+str(self.sY1D/ratio))
			
            text_file.write("\n----------------------------------------------------------------------------------------------------------------------------------------------\n\n")
			#adjust progress bar
            self.progressBar_BatchMode.setValue((i+1)*100/length)

        text_file.close()	
    def subBackground(self, state):
        if state == QtCore.Qt.Checked:
            if self.bkgrndImageCheck==True:
                image.useBackground(True)
            else:
                self.textDisplay.setText("Please choose a background image first.\n"+self.textDisplay.toPlainText())
        else:
            image.useBackground(False)  			
    def saturatedPix(self, state):
        if state == QtCore.Qt.Checked:
            self.showSatPixCheck=True
			
        else:
            self.showSatPixCheck=False
		
        self.updateImage()
    def originalImage(self, state):
		#global crop
        if state == QtCore.Qt.Checked:
            self.showOrigImageCheck = True
            self.textDisplay.setText("Set to show original image.\n"+self.textDisplay.toPlainText())
        else:
            self.showOrigImageCheck = False
            self.textDisplay.setText("Set to show cropped and altered image.\n"+self.textDisplay.toPlainText())
    def manualCrop(self,state):  
        if state == QtCore.Qt.Checked:

            picture.addItem(roi)
            roi.setZValue(12)
            image.useManualCrop(True)
            self.textDisplay.setText("Set to use manual crop.\n"+self.textDisplay.toPlainText())

        else:
            picture.removeItem(roi)
            image.useManualCrop(False)
            self.textDisplay.setText("Not set to use manual crop.\n"+self.textDisplay.toPlainText())      
    def directFit(self, state):
        if state == QtCore.Qt.Checked:
            self.showDirectFitCheck=True
			
        else:
            self.showDirectFitCheck=False
		
        self.updateImage()
    def projFits(self, state):
        if state == QtCore.Qt.Checked:
            self.show1DFitsCheck=True
			
        else:
            self.show1DFitsCheck=False
		
        self.updateImage()		
    def units(self, state):
	
        if state == QtCore.Qt.Checked:
            self.showParamsInMMCheck=True
			
        else:
            self.showParamsInMMCheck=False
		
        self.updateParamLabel()			
    def getBeamParameters(self):
       
        image.setManualCrop(int(roi.pos()[0]),int(roi.pos()[1]),int(roi.size()[0]),int(roi.size()[1]))		
		#get parameters
        start = time.time()
        param = image.getBeamParameters() 
		#allow updateImage() to show crosshair and contours
        self.showCrosshairsAndContours=True 
        self.updateGraphImage = True 		
        self.ptmRatio=image.getPTMRatio()
		

        size = image.getImageDataSize()
        height = image.getImageHeight()
        width = image.getImageWidth()	

        def BVN((x,y),Bk,Amp,mx,my,sx,sy,sxy):
    	    Bk = float(Bk)
    	    Amp = float(Amp)
    	    mx = float(mx)
    	    my = float(my)
    	    sx = float(sx)
    	    sy = float(sy)
            sxy = float(sxy)		
            g = Bk + Amp*np.exp(-0.5*(sy*(x-mx)**2-2*sxy*(x-mx)*(y-my)+sx*(y-my)**2)/(sy*sx-sxy**2))
            return g.ravel()

	    
		
		####lmfit stuff if you want to use it####
        # model = lmfit.Model(BVN, independent_vars=["x", "y"],param_names=["Bk", "Amp", "mx", "my", "sx", "sy", "sxy"])
        # initial_guess = model.make_params(Bk=0,Amp=max(image.getPixIntensity()),mx=param[10],my=param[12],sx=param[11],sy=param[13],sxy=0) 
        # popt = model.fit(image.getPixIntensity(), x=image.getX(), y=image.getY(),params=initial_guess,fit_kws={'maxfev': 40})
        initial_guess = (0,max(image.getPixIntensity()),param[10],param[12],param[11],param[13],0)
        popt, pcov = opt.curve_fit(BVN, (image.getX(), image.getY()), image.getPixIntensity(), p0=initial_guess)
        end = time.time() 
		
		#set Text in OUT
        self.textDisplay.setText("Completed Beam Size Analysis in "+str(end-start)+" seconds\n"+self.textDisplay.toPlainText())
		
		###for displaying using scipy optimizeation####
        self.muX = round(popt[2]+image.getCroppedX(),2)
        self.muY = round(popt[3]+image.getCroppedY(),2)
        self.sX = round(m.sqrt(popt[4]),2)
        self.sY = round(m.sqrt(popt[5]),2)
        self.sXY = round(popt[6],2)
        self.rho = round(popt[6]/(m.sqrt(popt[4])*m.sqrt(popt[5])),3)
		
		
		#######For displaying lmfit fit############
        #print(popt.fit_report())
        #print(popt.params["mx"].value)
        # self.muX = round(popt.params["mx"].value+image.getCroppedX(),2)
        # self.muY = round(popt.params["my"].value+image.getCroppedY(),2)
        # self.sX = round(m.sqrt(popt.params["sx"].value),2)
        # self.sY = round(m.sqrt(popt.params["sy"].value),2)
        # self.sXY = round(popt.params["sxy"].value,2)
        # self.rho = round(popt.params["sxy"].value/(m.sqrt(popt.params["sx"].value)*m.sqrt(popt.params["sy"].value)),3)
		
		
		#######For displaying c++ fit############
        # self.muX = round(param[0],3)
        # self.muY = round(param[1],3)
        # self.sX = round(m.sqrt(param[2]),3)
        # self.sY = round(m.sqrt(param[3]),3)
        # self.sXY = round(param[4],3)
        # self.rho = round(param[4]/(m.sqrt(param[2])*m.sqrt(param[3])),3)
		
        self.muXD = round(param[5],2)
        self.muYD = round(param[6],2)
        self.sXD = round(m.sqrt(param[7]),2)
        self.sYD = round(m.sqrt(param[8]),2)
        self.sXYD = round(param[9],2)
        self.rhoD = round(param[9]/(m.sqrt(param[7])*m.sqrt(param[8])),3)
		
        self.muX1D = round(param[10],3)+image.getCroppedX()
        self.muY1D = round(param[12],3)+image.getCroppedY()
        self.sX1D = round(param[11],3)	
        self.sY1D = round(param[13],3)
        self.updateParamLabel()
        picture.removeItem(roi)
        self.updateImage()			
    def style_choice(self,text):
        if text=="Fire":
            STEPS = np.array([0.0, 0.2, 0.6, 1.0])
            CLRS =           ['k', 'r', 'y', 'w']
        elif text=="Ice":
            STEPS = np.array([0.0, 0.5, 0.8])
            CLRS =           ['k', 'b', 'w']
        elif text=="Grayscale":
            STEPS = np.array([0.0, 1.0])
            CLRS =           ['k', 'w']    
        elif text=="Rainbow":
            STEPS = np.array([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
            CLRS =           ['k', 'b', 'm', 'r', 'y', 'w']    			
        clrmp = pg.ColorMap(STEPS, np.array([pg.colorTuple(pg.Color(c)) for c in CLRS]))
		## Get the LookupTable
        lut = clrmp.getLookupTable()	
        img.setLookupTable(lut)
        bimg.setLookupTable(lut)
    def saveParamters(self): 
     	fileName = QtGui.QFileDialog.getSaveFileName()
        print(fileName)
		
        text_file = open(fileName, "w")
        text_file.write(self.statusInfo1.text()+"\n")
        text_file.write(self.statusInfo2.text()+"\n\n")
        if self.showParamsInMMCheck==True:
            text_file.write("Units are in millimetres.\n\n")
            text_file.write(
                 "\nBVN Fit:-------------------------------------------------------------"+
                 "\nPosition x: "+str(self.muX/self.ptmRatio)+
                 "\nPostion y: "+str(self.muY/self.ptmRatio)+
                 "\nSigma x: "+str(self.sX/self.ptmRatio)+
                 "\nSigma y: "+str(self.sY/self.ptmRatio)+
                 "\nCov(xy): "+str(self.sXY/(self.ptmRatio*self.ptmRatio))+
                 "\nrho: "+str(self.rho)+
                 "\nCovariance Matrix Fit:-------------------------------------------------------------"+
                 "\nPosition x: "+str(self.muXD/self.ptmRatio)+
                 "\nPostion y: "+str(self.muYD/self.ptmRatio)+
                 "\nSigma x: "+str(self.sXD/self.ptmRatio)+
                 "\nSigma y: "+str(self.sYD/self.ptmRatio)+
                 "\nCov(xy): "+str(self.sXYD/(self.ptmRatio*self.ptmRatio))+
                 "\nrho: "+str(self.rhoD)+		
                 "\n1D Estimates:-------------------------------------------------------------"+
                 "\nPosition x:"+str(self.muX1D/self.ptmRatio)+
                 "\nPosition y:"+str(self.muY1D/self.ptmRatio)+
                 "\nSigma x:"+str(self.sX1D/self.ptmRatio)+
                 "\nSigma y:"+str(self.sY1D/self.ptmRatio))
            text_file.close()	
        else:
            text_file.write("Units are in pixels.\n\n")
            text_file.write(
                 "\nBVN Fit:-------------------------------------------------------------"+
                 "\nPosition x: "+str(self.muX)+
                 "\nPostion y: "+str(self.muY)+
                 "\nSigma x: "+str(self.sX)+
                 "\nSigma y: "+str(self.sY)+
                 "\nCov(xy): "+str(self.sXY)+
                 "\nrho: "+str(self.rho)+
                 "\nCovariance Matrix Fit:-------------------------------------------------------------"+
                 "\nPosition x: "+str(self.muXD)+
                 "\nPostion y: "+str(self.muYD)+
                 "\nSigma x: "+str(self.sXD)+
                 "\nSigma y: "+str(self.sYD)+
                 "\nCov(xy): "+str(self.sXYD)+
                 "\nrho: "+str(self.rhoD)+		
                 "\n1D Estimates:-------------------------------------------------------------"+
                 "\nPosition x:"+str(self.muX1D)+
                 "\nPosition y:"+str(self.muY1D)+
                 "\nSigma x:"+str(self.sX1D)+
                 "\nSigma y:"+str(self.sY1D))
            text_file.close()			
	
#FUNCTIONS TO USE EXPERT SETTINGS(ES)
    def saveES(self):
     	fileName = QtGui.QFileDialog.getSaveFileName()
        print(fileName)
		
        text_file = open(fileName, "w")
        text_file.write("[ES-config]"+
            "\nMask_x = "+str(self.maskX_le.text())+
            "\nMask_y = "+str(self.maskY_le.text())+
            "\nMask_Rx = "+str(self.maskRX_le.text())+
            "\nMask_Ry = "+str(self.maskRY_le.text())+
            "\nPTM = "+str(self.pxtmm_le.text())+
            "\nRR_Threshold = "+str(self.RR_le.text())+
            "\nSatPixVal = "+str(self.satPixVal_le.text())+
            "\nSigma_Cut = "+str(self.sigmaCut_le.text())+
            "\nManual_Crop_x = "+str(self.manCropX_le.text())+
            "\nManual_Crop_y = "+str(self.manCropY_le.text())+
            "\nManual_Crop_w = "+str(self.manCropW_le.text())+
            "\nManual_Crop_h = "+str(self.manCropH_le.text())+
            "\nSpec_Filter = "+str(self.filter_le.text())+
            "\nDirect_Cut_Level = "+str(self.directCut_le.text()))
        text_file.close()		  
    def loadES(self):
        fileName = QtGui.QFileDialog.getOpenFileName()
        configParser = ConfigParser.RawConfigParser()   
        configFilePath = str(fileName)
        configParser.read(configFilePath)
        self.maskX_le.setText(configParser.get('ES-config', 'Mask_x'))
        self.maskY_le.setText(configParser.get('ES-config', 'Mask_y'))
        self.maskRX_le.setText(configParser.get('ES-config', 'Mask_Rx'))
        self.maskRY_le.setText(configParser.get('ES-config', 'Mask_Ry'))
        self.pxtmm_le.setText(configParser.get('ES-config', 'PTM'))
        self.RR_le.setText(configParser.get('ES-config', 'RR_Threshold'))
        self.satPixVal_le.setText(configParser.get('ES-config', 'SatPixVal'))
        self.sigmaCut_le.setText(configParser.get('ES-config', 'Sigma_Cut'))
        self.manCropX_le.setText(configParser.get('ES-config', 'Manual_Crop_x'))
        self.manCropY_le.setText(configParser.get('ES-config', 'Manual_Crop_y'))
        self.manCropW_le.setText(configParser.get('ES-config', 'Manual_Crop_w'))		
        self.manCropH_le.setText(configParser.get('ES-config', 'Manual_Crop_h'))	
        self.filter_le.setText(configParser.get('ES-config', 'Spec_Filter'))	
        self.directCut_le.setText(configParser.get('ES-config', 'Direct_Cut_Level'))			
    def useMaskES(self, state):
        if state == QtCore.Qt.Checked:
            image.useESMask(True)
            image.setESMask(int(self.maskX_le.text()),int(self.maskY_le.text()),int(self.maskRX_le.text()),int(self.maskRY_le.text()))

            self.textDisplay.setText("ES: Now using mask parameters"
			"\nX: "+str(self.maskX_le.text())+
			"\nY: "+str(self.maskY_le.text())+
			"\nRx: "+str(self.maskRX_le.text())+
			"\nRy: "+str(self.maskRY_le.text())+"\n"+self.textDisplay.toPlainText()) 

        else:
            image.useESMask(False)
            self.textDisplay.setText("ES: Stopped using mask parameters\n"+self.textDisplay.toPlainText())			
    def usePixToMmES(self, state):
        if state == QtCore.Qt.Checked:
            self.ptmRatio=float(self.pxtmm_le.text());
            self.textDisplay.setText("ES: Pixel to Millimetre ratio set to"
			"\n"+str(self.pxtmm_le.text())+"\n"+self.textDisplay.toPlainText()) 
        else:
            self.ptmRatio=image.getPTMRatio();
            self.textDisplay.setText("ES: Pixel to Millimetre ratio set to"
			"\nbe defined by YAG.config\n"+self.textDisplay.toPlainText())
    def useRRES(self, state):
        if state == QtCore.Qt.Checked:
            image.useESRRThreshold(True)
            image.setESRRThreshold(float(self.RR_le.text()))
            self.textDisplay.setText("ES: Now using users R^2 Threshold"
			"\nThreshold: "+str(self.RR_le.text())+"\n"+self.textDisplay.toPlainText()) 
        else:
            image.useESRRThreshold(False)
            self.textDisplay.setText("ES: Stopped using users R^2 Threshold\n"+self.textDisplay.toPlainText())  			
    def useSatValES(self, state):
        if state == QtCore.Qt.Checked:
            self.satValES=float(self.satPixVal_le.text())
            self.textDisplay.setText("ES: Set Saturation Value"
			"\nSaturation intensity: "+str(self.satPixVal_le.text())+"\n"+self.textDisplay.toPlainText()) 
        else:
            self.satValES=self.defaultSatVal	
            self.textDisplay.setText("ES: Set saturation value to default\n"+self.textDisplay.toPlainText())  			
    def useSigmaCutES(self, state):
        if state == QtCore.Qt.Checked:
            image.useESSigmaCut(True)
            image.setESSigmaCut(float(self.sigmaCut_le.text()))
            self.textDisplay.setText("ES: Now cutting image around beam with multiple of sigma"
			"\nMultiple: "+str(self.sigmaCut_le.text())+"\n"+self.textDisplay.toPlainText()) 
        else:
            image.useESSigmaCut(False)
            self.textDisplay.setText("ES: Using default multiple of sigma\n"+self.textDisplay.toPlainText()) 				
    def useManualCropES(self, state):
        if state == QtCore.Qt.Checked:
            picture.addItem(roi)
            roi.setZValue(12)
            roi.setPos([int(self.manCropX_le.text()),int(self.manCropY_le.text())])
            roi.setSize([int(self.manCropW_le.text()),int(self.manCropH_le.text())])
            image.useManualCrop(True)
            self.textDisplay.setText("ES: Set to use manual crop"
			"\nX: "+str(self.manCropX_le.text())+
			"\nY: "+str(self.manCropY_le.text())+
			"\nWidth: "+str(self.manCropW_le.text())+
			"\nHeight: "+str(self.manCropH_le.text())+"\n"+self.textDisplay.toPlainText()) 
        else:
            picture.removeItem(roi)
            image.useManualCrop(False)
            self.textDisplay.setText("ES: Not set to use manual crop.\n"+self.textDisplay.toPlainText()) 			
    def useFilterES(self, state):
        if state == QtCore.Qt.Checked:
            image.useESFilter(True)
            image.setESFilter(int(self.filter_le.text()))
            self.textDisplay.setText("ES: Filtering projections with a N point moving average"
			"\nN: "+str(self.filter_le.text())+"\n"+self.textDisplay.toPlainText()) 
        else:
            image.useESFilter(False)
            self.textDisplay.setText("ES: Filtering image with default settings\n"+self.textDisplay.toPlainText()) 			
    def useDirectCutES(self, state):
        if state == QtCore.Qt.Checked:
            image.useESDirectCut(True)
            image.setESDirectCut(float(self.directCut_le.text()))
            self.textDisplay.setText("ES: Direct Method is set to ignore below"
			"\n "+str(self.directCut_le.text())+"% of the maximum intensity\n"+self.textDisplay.toPlainText()) 
        else:
            image.useESDirectCut(False)
            self.textDisplay.setText("ES: No cut-off level for Direct Method\n"+self.textDisplay.toPlainText()) 		   
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "byscit", None))
        self.statusInfo1.setText(_translate("MainWindow", "LOADED IMAGE: ", None))
        #self.tabWidget.setToolTip(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>", None))
        self.findBeam.setText(_translate("MainWindow", "Find Beam", None))
        self.beamInfoDisplay.setText(_translate("MainWindow", "Parameters", None))
        self.subtractBackground.setText(_translate("MainWindow", "Subtract Background", None))
        self.showOriginalImage.setText(_translate("MainWindow", "Show Orginal Image", None))
        self.highlightSatPix.setText(_translate("MainWindow", "Highlight Saturated Pixels", None))
        self.useManualCrop.setText(_translate("MainWindow", "Use Manual Crop", None))
        self.comboBox.setItemText(0, _translate("MainWindow", "Grayscale", None))
        self.comboBox.setItemText(1, _translate("MainWindow", "Rainbow", None))
        self.comboBox.setItemText(2, _translate("MainWindow", "Ice", None))
        self.comboBox.setItemText(3, _translate("MainWindow", "Fire", None))
        self.Unitsmm.setText(_translate("MainWindow", "Units in millimetres", None))
        self.showProjFits.setText(_translate("MainWindow", "Show 1D Fits to Projections", None))
        self.showDirectFit.setText(_translate("MainWindow", "Show Direct Fit on Image", None))
        self.textDisplay.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
         "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
         "p, li { white-space: pre-wrap; }\n"
         "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
         "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.homeTab), _translate("MainWindow", "Main Page", None))
        self.batchMode_groupbox.setTitle(_translate("MainWindow", "Batch Mode", None))
        self.loadImagesBtn.setText(_translate("MainWindow", "Load Images", None))
        self.loadBkgrndImagesBtn.setText(_translate("MainWindow", "Load Background Images", None))
        self.runBatchBtn.setText(_translate("MainWindow", "Run", None))
        self.groupBox.setTitle(_translate("MainWindow", "Output Settings", None))
        self.centreMaskLabel_2.setText(_translate("MainWindow", "Name of Output File", None))
        self.centreMaskLabel_3.setText(_translate("MainWindow", "Contents in File", None))
        self.checkBox_SaveBVN.setText(_translate("MainWindow", "BVN Results", None))
        self.checkBox_SaveDirect.setText(_translate("MainWindow", "Direct Results", None))
        self.checkBox_Save1D.setText(_translate("MainWindow", "Fits to Projections", None))
        #self.checkBox_SaveErrors.setText(_translate("MainWindow", " Errors on Values", None))
        #self.checkBox_SaveGraphNames.setText(_translate("MainWindow", "Names of Saved Associated Graphs", None))
        self.centreMaskLabel_4.setText(_translate("MainWindow", "Graphs", None))
        self.checkBox_ImageSave.setText(_translate("MainWindow", "Image", None))
        self.checkBox_XProjSave.setText(_translate("MainWindow", " X Projection", None))
        self.checkBox_YProjSave.setText(_translate("MainWindow", " Y Projection", None))
        self.centreMaskLabel_5.setText(_translate("MainWindow", "Save as a...", None))
        self.checkBox_SaveAsPNG.setText(_translate("MainWindow", "png", None))
        self.checkBox_SaveAsSVG.setText(_translate("MainWindow", "svg", None))
        self.checkBox_SaveAsCSV.setText(_translate("MainWindow", "csv", None))
        self.ES_groupbox.setTitle(_translate("MainWindow", "Expert Settings", None))
        self.expertSetLoad_Btn.setText(_translate("MainWindow", "Load Saved Settings", None))
        self.expertSetSave_Btn.setText(_translate("MainWindow", "Save Current Settings", None))
        self.Mask.setText(_translate("MainWindow", "Mask", None))
        self.useMask_checkBox.setText(_translate("MainWindow", "Use these mask parameters", None))
        self.MaskInfo.setText(_translate("MainWindow", "These parameters are used to set the ellispse shaped mask that goes over the image to remove irrelavent pixel data.\n"
         "To custom build a mask you need the x and y pixel that correspond to the centre of the mask and the x and y maximun radial\n"
         "values (also in number of pixels) from the centre of the elliptical mask.", None))
        self.centreMaskLabel.setText(_translate("MainWindow", "Centre of Ellipse", None))
        self.label_36.setText(_translate("MainWindow", "X:", None))
        self.label_37.setText(_translate("MainWindow", "Y:", None))
        self.label_38.setText(_translate("MainWindow", "Rx:", None))
        self.RadiiMaskLabel.setText(_translate("MainWindow", "Radii of Ellipse", None))
        self.label_40.setText(_translate("MainWindow", "Ry:", None))
        self.ESVariables.setText(_translate("MainWindow", "Adjustable Variables used in Beam Anaylsis", None))
        self.labelPixToMm.setText(_translate("MainWindow", "Pixel : Millemeter", None))
        self.ManCropLabel.setText(_translate("MainWindow", "Manual Crop parameters", None))
        self.label_52.setText(_translate("MainWindow", "X:", None))
        self.label_53.setText(_translate("MainWindow", "Y:", None))
        self.label_54.setText(_translate("MainWindow", "Width:", None))
        self.label_55.setText(_translate("MainWindow", "Height:", None))
        self.SatPixValLabel.setText(_translate("MainWindow", "Saturated Pixel Value", None))
        self.ESVariableInfo.setText(_translate("MainWindow", "HIHI", None))
        self.specificFilterLabel.setText(_translate("MainWindow", "Specific Filter", None))
        self.specFilterText.setText(_translate("MainWindow", "Normally, the anaylsis finds the best filter to use on the X and Y projections. The filter removes noise using a moving averages and\n"
         " automatic the best filter is chosen from 5,10 or 20 point moving averages. Here you can set the number of data points you want\n"
         " the filter to average over in order to get 1D estimates for beam position and size.", None))
        self.RRLabel.setText(_translate("MainWindow", "R-squared Threshold", None))
        self.sigmCutLabel.setText(_translate("MainWindow", "Sigma Cut", None))
        self.directCutText.setText(_translate("MainWindow", "Used in Direct Method, this option sets a cut off level, below which pixels are ignored. Enter\n"+
         "the percentage of the maximum intensity you want as your cut off. For example, entering a vlaue of '10' would mean that the here\n"+
         "cut off level would be 0.1*(Max. Pixel Intensity).", None))
        self.batchModeText.setText(_translate("MainWindow", "This section is for loading and analysing multiple images in one run. The options (on the Main Page) and Expert Settings that are\n"+
         "selected in the GUI at time of running a batch of images will be the set up for all the images being analysed. Also, there are two\n"+
         "running methods with background images. The first is to have one background image for all the images being analysed. The\n"+
         "second is that each image has a corresponding background image. In the latter case make sure the positions the image and its\n"+
         "corresponding background image are the sae in thir respective lists.", None))
        self.directCutLabel.setText(_translate("MainWindow", "Cut level for Direct Method", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.expertTab), _translate("MainWindow", "Settings", None))
        self.statusInfo2.setText(_translate("MainWindow", "LOADED BACKGROUND IMAGE: ", None))
        #self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuOpen.setTitle(_translate("MainWindow", "Open", None))
        self.menuSave.setTitle(_translate("MainWindow", "Save", None))
        #self.actionOpen.setText(_translate("MainWindow", "Open", None))
       # self.actionSave.setText(_translate("MainWindow", "Save", None))
        self.actionImage.setText(_translate("MainWindow", "Image", None))
        self.actionIMages.setText(_translate("MainWindow", "Batch Images", None))
        self.actionBeam_Positions.setText(_translate("MainWindow", "Beam Positions", None))
        self.actionSet_Backgound.setText(_translate("MainWindow", "Set Backgound", None))
        self.actionSet_Backgounds.setText(_translate("MainWindow", "Set Batch Backgounds", None))
        self.actionSaveImage.setText(_translate("MainWindow", "Image", None))
        self.actionSaveXProj.setText(_translate("MainWindow", "X Projection", None))
        self.actionSaveYProj.setText(_translate("MainWindow", "Y Projection", None))



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

