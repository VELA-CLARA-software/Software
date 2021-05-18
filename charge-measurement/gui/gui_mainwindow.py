# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled1.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
#import pyqtgraph
#from pyqtgraph import GraphicsView, GraphicsLayout
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("Charge measurement"))
        MainWindow.resize(1151, 759)
        self.mainWidget = QtWidgets.QWidget(MainWindow)
        self.mainWidget.resize(1140, 750)
        self.mainBox = QtWidgets.QHBoxLayout(self.mainWidget)
        self.labelBox = QtWidgets.QVBoxLayout()
        self.midVBox = QtWidgets.QVBoxLayout()
        self.plotVBox = QtWidgets.QVBoxLayout()
        self.numShotsHBox = QtWidgets.QHBoxLayout()
        self.titleLabel = QtWidgets.QLabel()
        self.infoLabel = QtWidgets.QLabel()
        self.labelBox.addWidget(self.titleLabel)
        self.labelBox.addWidget(self.infoLabel)
        self.labelBox.addStretch()
        self.scanButton = QtWidgets.QPushButton()
        self.scanButton.setObjectName(_fromUtf8("scanButton"))
        self.scanButton.setMinimumSize(QtCore.QSize(100, 100))
        self.saveButton = QtWidgets.QPushButton()
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.saveButton.setMinimumSize(QtCore.QSize(100, 100))
        self.saveButton.setEnabled(False)
        self.groupBox = QtWidgets.QGroupBox()
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.groupBox.setMinimumSize(QtCore.QSize(200,200))
        self.newValsVBox = QtWidgets.QVBoxLayout()
        self.newVals = QtWidgets.QTextEdit()
        self.newVals.setText(_fromUtf8(""))
        self.newVals.setObjectName(_fromUtf8("newVals"))
        self.newValsVBox.addWidget(self.newVals)
        self.groupBox.setLayout(self.newValsVBox)
        self.numShotsLabel = QtWidgets.QLabel()
        self.numShotsLabel.setObjectName(_fromUtf8("numShotsLabel"))
        self.numShotsOutputWidget = QtWidgets.QDoubleSpinBox()
        self.numShotsOutputWidget.setSuffix(_fromUtf8(""))
        self.numShotsOutputWidget.setDecimals(0)
        self.numShotsOutputWidget.setMinimum(1)
        self.numShotsOutputWidget.setMaximum(1000)
        self.numShotsOutputWidget.setSingleStep(1)
        self.numShotsOutputWidget.setProperty("value", 100)
        self.numShotsOutputWidget.setObjectName(_fromUtf8("numShotsOutputWidget"))
        # self.numShotsOutputWidget = QtGui.QPlainTextEdit()
        # self.numShotsOutputWidget.setObjectName(_fromUtf8("numShotsOutputWidget"))
        self.numShotsOutputWidget.setMinimumSize(QtCore.QSize(50,50))
        self.numShotsOutputWidget.setMaximumSize(QtCore.QSize(50,50))
        self.numShotsHBox.addWidget(self.numShotsLabel)
        self.numShotsHBox.addWidget(self.numShotsOutputWidget)
        self.numShotsHBox.addSpacing(300)
        self.scanRangeHBox = QtWidgets.QHBoxLayout()
        self.rangeLabelVBox = QtWidgets.QVBoxLayout()
        self.lowerBoundVBox = QtWidgets.QVBoxLayout()
        self.upperBoundVBox = QtWidgets.QVBoxLayout()
        self.numStepsVBox = QtWidgets.QVBoxLayout()
        self.offCrestPhaseVBox = QtWidgets.QVBoxLayout()
        self.lowerBoundOutputWidget = QtWidgets.QDoubleSpinBox()
        self.lowerBoundOutputWidget.setSuffix(_fromUtf8(""))
        self.lowerBoundOutputWidget.setDecimals(3)
        self.lowerBoundOutputWidget.setMinimum(-20)
        self.lowerBoundOutputWidget.setMaximum(20)
        self.lowerBoundOutputWidget.setSingleStep(0.1)
        self.lowerBoundOutputWidget.setProperty("value", -9)
        self.lowerBoundOutputWidget.setObjectName(_fromUtf8("lowerBoundOutputWidget"))
        # self.numShotsOutputWidget = QtGui.QPlainTextEdit()
        # self.numShotsOutputWidget.setObjectName(_fromUtf8("numShotsOutputWidget"))
        self.lowerBoundOutputWidget.setMinimumSize(QtCore.QSize(70, 30))
        self.lowerBoundOutputWidget.setMaximumSize(QtCore.QSize(70, 30))
        self.upperBoundOutputWidget = QtWidgets.QDoubleSpinBox()
        self.upperBoundOutputWidget.setSuffix(_fromUtf8(""))
        self.upperBoundOutputWidget.setDecimals(3)
        self.upperBoundOutputWidget.setMinimum(-20)
        self.upperBoundOutputWidget.setMaximum(20)
        self.upperBoundOutputWidget.setSingleStep(0.1)
        self.upperBoundOutputWidget.setProperty("value", -1)
        self.upperBoundOutputWidget.setObjectName(_fromUtf8("upperBoundOutputWidget"))
        self.upperBoundOutputWidget.setMinimumSize(QtCore.QSize(70, 30))
        self.upperBoundOutputWidget.setMaximumSize(QtCore.QSize(70, 30))
        self.numStepsOutputWidget = QtWidgets.QDoubleSpinBox()
        self.numStepsOutputWidget.setSuffix(_fromUtf8(""))
        self.numStepsOutputWidget.setDecimals(0)
        self.numStepsOutputWidget.setMinimum(1)
        self.numStepsOutputWidget.setMaximum(1000)
        self.numStepsOutputWidget.setSingleStep(1)
        self.numStepsOutputWidget.setProperty("value", 10)
        self.numStepsOutputWidget.setObjectName(_fromUtf8("numStepsOutputWidget"))
        self.numStepsOutputWidget.setMinimumSize(QtCore.QSize(70, 30))
        self.numStepsOutputWidget.setMaximumSize(QtCore.QSize(70, 30))
        self.offCrestPhaseOutputWidget = QtWidgets.QDoubleSpinBox()
        self.offCrestPhaseOutputWidget.setSuffix(_fromUtf8(""))
        self.offCrestPhaseOutputWidget.setDecimals(3)
        self.offCrestPhaseOutputWidget.setMinimum(-180)
        self.offCrestPhaseOutputWidget.setMaximum(180)
        self.offCrestPhaseOutputWidget.setSingleStep(0.01)
        self.offCrestPhaseOutputWidget.setProperty("value", 0)
        self.offCrestPhaseOutputWidget.setObjectName(_fromUtf8("offCrestPhaseOutputWidget"))
        self.offCrestPhaseOutputWidget.setMinimumSize(QtCore.QSize(70, 30))
        self.offCrestPhaseOutputWidget.setMaximumSize(QtCore.QSize(70, 30))
        self.scanRangeSpacer = QtWidgets.QLabel()
        self.scanRangeSpacer.setObjectName(_fromUtf8("scanRangeSpacer"))
        self.scanRangeLabel = QtWidgets.QLabel()
        self.scanRangeLabel.setObjectName(_fromUtf8("scanRangeLabel"))
        self.lowerBoundLabel = QtWidgets.QLabel()
        self.lowerBoundLabel.setObjectName(_fromUtf8("lowerBoundLabel"))
        self.upperBoundLabel = QtWidgets.QLabel()
        self.upperBoundLabel.setObjectName(_fromUtf8("upperBoundLabel"))
        self.numStepsLabel = QtWidgets.QLabel()
        self.numStepsLabel.setObjectName(_fromUtf8("numStepsLabel"))
        self.offCrestPhaseLabel = QtWidgets.QLabel()
        self.offCrestPhaseLabel.setObjectName(_fromUtf8("offCrestPhaseLabel"))
        self.rangeLabelVBox.addWidget(self.scanRangeSpacer)
        self.rangeLabelVBox.addWidget(self.scanRangeLabel)
        self.lowerBoundVBox.addWidget(self.lowerBoundLabel)
        self.lowerBoundVBox.addWidget(self.lowerBoundOutputWidget)
        self.upperBoundVBox.addWidget(self.upperBoundLabel)
        self.upperBoundVBox.addWidget(self.upperBoundOutputWidget)
        self.numStepsVBox.addWidget(self.numStepsLabel)
        self.numStepsVBox.addWidget(self.numStepsOutputWidget)
        self.offCrestPhaseVBox.addWidget(self.offCrestPhaseLabel)
        self.offCrestPhaseVBox.addWidget(self.offCrestPhaseOutputWidget)
        self.rangeLabelVBox.addStretch()
        self.lowerBoundVBox.addStretch()
        self.upperBoundVBox.addStretch()
        self.numStepsVBox.addStretch()
        self.offCrestPhaseVBox.addStretch()
        self.scanRangeHBox.addLayout(self.rangeLabelVBox)
        self.scanRangeHBox.addLayout(self.lowerBoundVBox)
        self.scanRangeHBox.addLayout(self.upperBoundVBox)
        self.scanRangeHBox.addLayout(self.numStepsVBox)
        self.scanRangeHBox.addLayout(self.offCrestPhaseVBox)
        self.scanRangeHBox.addStretch()
        self.resultsHBox = QtWidgets.QHBoxLayout()
        self.resultsLabel = QtWidgets.QLabel()
        self.resultsLabel.setObjectName(_fromUtf8("resultsLabel"))
        self.resultsLabel.setMinimumSize(QtCore.QSize(200, 100))
        self.resultsLabel.setMaximumSize(QtCore.QSize(200, 100))
        self.resultsHBox.addWidget(self.resultsLabel)
        self.messageHBox = QtWidgets.QHBoxLayout()
        self.messageLabel = QtWidgets.QLabel()
        self.messageLabel.setObjectName(_fromUtf8("messageHBox"))
        self.messageHBox.addWidget(self.messageLabel)
        self.progressBar = QtWidgets.QProgressBar()
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.messageHBox.addWidget(self.progressBar)
        self.messageHBox.addStretch()
        self.bunchChargeHBox = QtWidgets.QHBoxLayout()
        self.bunchChargeLabel = QtWidgets.QLabel()
        self.bunchChargeLabel.setObjectName(_fromUtf8("bunchChargeLabel"))
        self.bunchChargeChannelLabel = QtWidgets.QLabel()
        self.bunchChargeChannelLabel.setObjectName(_fromUtf8("bunchChargeChannelLabel"))
        self.bunchChargeDiagTypeLabel = QtWidgets.QLabel()
        self.bunchChargeDiagTypeLabel.setObjectName(_fromUtf8("bunchChargeDiagTypeLabel"))
        self.bunchChargeOutputWidget = QtWidgets.QLabel()
        self.bunchChargeOutputWidget.setObjectName(_fromUtf8("bunchChargeOutputWidget"))
        self.bunchChargeHBox.addWidget(self.bunchChargeLabel)
        self.bunchChargeHBox.addWidget(self.bunchChargeDiagTypeLabel)
        self.bunchChargeHBox.addWidget(self.bunchChargeOutputWidget)
        # self.midVBox.addWidget(self.measureTypeGroupBox)
        self.midVBox.addLayout(self.scanRangeHBox)
        self.midVBox.addLayout(self.numShotsHBox)
        self.midVBox.addWidget(self.groupBox)
        self.midVBox.addLayout(self.resultsHBox)
        self.midVBox.addLayout(self.messageHBox)
        self.midVBox.addWidget(self.scanButton)
        self.midVBox.addWidget(self.saveButton)
        self.midVBox.addLayout(self.bunchChargeHBox)
        # self.chargePlotWidget = QWidget()
        self.chargePlotLayout = QtWidgets.QVBoxLayout()
        self.plotCanvas = MplCanvas(self)
        self.plotCanvas.axes.grid()
        self.plotCanvas.axes.set_title('wcm vs laser energy')
        self.plotCanvas.axes.set_xlabel('laser energy (uJ)')
        self.plotCanvas.axes.set_ylabel('bunch charge (pC)')
        self.chargePlotLayout.addWidget(self.plotCanvas)
        # self.chargePlotWidget.setLayout(self.chargePlotLayout)
        # pyqtgraph.setConfigOption('background', 'w')
        # self.graphicsView = GraphicsView()
        # self.graphicsLayout = GraphicsLayout()
        # self.chargePlotView = GraphicsView(self.chargePlot, useOpenGL=True)
        # self.chargePlotView.addItem(self.chargePlot)
        # self.chargePlotView.setCentralItem(self.chargePlotWidgetGraphicsLayout)
        # self.chargePlotPlot = pyqtgraph.PlotItem()
        # self.graphicsView.setCentralItem(self.graphicsLayout)
        # self.chargePlotPlot = self.graphicsLayout.addPlot(title="wcm vs ophir")
        # self.chargePlotPlot.setLabel('bottom', text='laser energy', units='uJ')
        # self.chargePlotPlot.setLabel('left', text='wcm charge', units='pC')
        # self.chargeSubPlot = self.chargePlotPlot.plot(symbolPen = 'b', symbol='o', width=0, symbolSize=1, pen=None)
        # self.chargePlot = pyqtgraph.ErrorBarItem(x=np.array([]), y=np.array([]), height=np.array([]), beam=None, pen={'color':'b', 'width':2})
        # self.chargePlotPlot.addItem(self.chargePlot)
        # self.chargePlotLayout.addWidget(self.graphicsView)
        # # self.chargePlotLayout.addWidget(self.chargePlot)
        # # self.plotItem = pyqtgraph.ErrorBarItem(x=np.array([]), y=np.array([]), beam=None,
        # #                                        pen={'color': 'b', 'width': 2})
        # # self.chargePlot = self.chargePlotWidgetGraphicsLayout.ErrorBarItem(title='wcm vs ophir', x=np.array([]),
        # #                                                               y=np.array([]), beam=None,
        # #                                                               pen={'color': 'b', 'width': 2})
        # self.chargePlotPlot.showGrid(x=True, y=True)
        # self.plotVBox.addWidget(self.chargePlotWidget)
        self.mainBox.addLayout(self.midVBox)
        self.mainBox.addLayout(self.chargePlotLayout)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Charge measurement", None))
        self.scanButton.setText(_translate("MainWindow", "Scan laser attenuator", None))
        self.saveButton.setText(_translate("MainWindow", "Save data", None))
        self.groupBox.setTitle(_translate("MainWindow", "Comments", None))
        self.numShotsLabel.setText(_translate("MainWindow", "# Shots", None))
        self.scanRangeLabel.setText(_translate("MainWindow", "Scan Range", None))
        self.newVals.setText(_translate("MainWindow", "", None))
        self.lowerBoundLabel.setText(_translate("MainWindow", "Lower Bound", None))
        self.upperBoundLabel.setText(_translate("MainWindow", "Upper Bound", None))
        self.numStepsLabel.setText(_translate("MainWindow", "# steps", None))
        self.offCrestPhaseLabel.setText(_translate("MainWindow", "Off-crest phase", None))
        # self.MainWindow.setTabText(self.MainWindow.indexOf(self.tab), _translate("MainWindow", "Settings", None))
        self.newFont = QtWidgets.QFont("Comic Sans", 20, QtGui.QFont.Bold)
        self.titleLabel.setFont(self.newFont)
        self.titleLabel.setText(_translate("MainWindow", "VELA/CLARA Beam \nPosition Monitor \nCalibrator", None))

    def closeEvent(self, event):
        self.closing.emit()

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)