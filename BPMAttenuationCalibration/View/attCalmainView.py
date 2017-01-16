# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled1.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import pyqtgraph

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

class attCalUi_TabWidget(object):
    def setupUi(self, TabWidget, bpmCont, beamline, machine):
        self.TabWidget = TabWidget
        self.bpmCont = bpmCont
        self.beamline = beamline
        self.machine = machine
        self.TabWidget.setObjectName(_fromUtf8("BPM Attenuation Calibrator"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.mainBox = QtGui.QHBoxLayout(self.tab)
        self.labelBox = QtGui.QVBoxLayout()
        self.midVBox = QtGui.QVBoxLayout()
        self.bpmListVBox = QtGui.QVBoxLayout()
        self.numShotsHBox = QtGui.QHBoxLayout()
        self.addToListButton = QtGui.QPushButton()
        self.addToListButton.setObjectName(_fromUtf8("addToListButton"))
        self.addToListButton.setMinimumSize(QtCore.QSize(100,100))
        self.bpmPVList = QtGui.QPlainTextEdit()
        self.bpmPVList.setObjectName(_fromUtf8("bpmPVList"))
        self.bpmListLabel = QtGui.QLabel()
        self.clearPVListButton = QtGui.QPushButton(self.tab)
        self.clearPVListButton.setObjectName(("clearPVListButton"))
        self.bpmListLabel.setObjectName(_fromUtf8("bpmListLabel"))
        self.bpmListVBox.addWidget(self.addToListButton)
        self.bpmListVBox.addWidget(self.bpmListLabel)
        self.bpmListVBox.addWidget(self.bpmPVList)
        self.bpmListVBox.addWidget(self.clearPVListButton)
        self.calibrateButton = QtGui.QPushButton()
        self.calibrateButton.setObjectName(_fromUtf8("calibrateButton"))
        self.calibrateButton.setMinimumSize(QtCore.QSize(100,100))
        self.comboBox = QtGui.QComboBox()
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
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
        self.numShots = QtGui.QPlainTextEdit()
        self.numShots.setObjectName(_fromUtf8("numShots"))
        self.numShots.setMinimumSize(QtCore.QSize(30,30))
        self.numShots.setMaximumSize(QtCore.QSize(30,30))
        self.numShotsHBox.addWidget(self.numShotsLabel)
        self.numShotsHBox.addWidget(self.numShots)
        self.numShotsHBox.addSpacing(300)
        self.scanRangeHBox = QtGui.QHBoxLayout()
        self.rangeLabelVBox = QtGui.QVBoxLayout()
        self.lowerBoundVBox = QtGui.QVBoxLayout()
        self.upperBoundVBox = QtGui.QVBoxLayout()
        self.lowerATTBound = QtGui.QPlainTextEdit()
        self.lowerATTBound.setObjectName(_fromUtf8("lowerATTBound"))
        self.upperATTBound = QtGui.QPlainTextEdit()
        self.upperATTBound.setObjectName(_fromUtf8("upperATTBound"))
        self.scanRangeSpacer = QtGui.QLabel()
        self.scanRangeSpacer.setObjectName(_fromUtf8("scanRangeSpacer"))
        self.scanRangeLabel = QtGui.QLabel()
        self.scanRangeLabel.setObjectName(_fromUtf8("scanRangeLabel"))
        self.lowerBoundLabel = QtGui.QLabel()
        self.lowerBoundLabel.setObjectName(_fromUtf8("lowerBoundLabel"))
        self.upperBoundLabel = QtGui.QLabel()
        self.upperBoundLabel.setObjectName(_fromUtf8("upperBoundLabel"))
        self.lowerATTBound.setMinimumSize(QtCore.QSize(30,30))
        self.lowerATTBound.setMaximumSize(QtCore.QSize(30,30))
        self.upperATTBound.setMinimumSize(QtCore.QSize(30,30))
        self.upperATTBound.setMaximumSize(QtCore.QSize(30,30))
        self.rangeLabelVBox.addWidget(self.scanRangeSpacer)
        self.rangeLabelVBox.addWidget(self.scanRangeLabel)
        self.lowerBoundVBox.addWidget(self.lowerBoundLabel)
        self.lowerBoundVBox.addWidget(self.lowerATTBound)
        self.upperBoundVBox.addWidget(self.upperBoundLabel)
        self.upperBoundVBox.addWidget(self.upperATTBound)
        self.rangeLabelVBox.addStretch()
        self.lowerBoundVBox.addStretch()
        self.upperBoundVBox.addStretch()
        self.scanRangeHBox.addLayout(self.rangeLabelVBox)
        self.scanRangeHBox.addLayout(self.lowerBoundVBox)
        self.scanRangeHBox.addLayout(self.upperBoundVBox)
        self.scanRangeHBox.addStretch()
        self.midVBox.addWidget(self.comboBox)
        self.midVBox.addLayout(self.numShotsHBox)
        self.midVBox.addWidget(self.calibrateButton)
        self.midVBox.addWidget(self.groupBox)
        self.midVBox.addLayout(self.scanRangeHBox)
        self.titleLabel = QtGui.QLabel()
        self.titleLabel.setObjectName(_fromUtf8("titleLabel"))
        self.infoLabel = QtGui.QLabel()
        self.infoLabel.setObjectName(_fromUtf8("infoLabel"))
        self.labelBox.addWidget(self.titleLabel)
        self.labelBox.addWidget(self.infoLabel)
        self.mainBox.addLayout(self.labelBox)
        self.mainBox.addLayout(self.midVBox)
        self.mainBox.addLayout(self.bpmListVBox)
        self.TabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab1 = QtGui.QWidget()
        self.tab1.setObjectName(_fromUtf8("tab1"))
        self.tabList = []
        self.graphicsViews = []
        self.graphicsViews_2 = []
        self.glayoutOutputs = []
        self.glayoutOutputs_2 = []

        self.retranslateUi(self.TabWidget, self.beamline, self.machine)
        QtCore.QMetaObject.connectSlotsByName(self.TabWidget)

    def retranslateUi(self, TabWidget, beamline, machine):
        self.beamline = beamline
        self.machine = machine
        self.TabWidget.setWindowTitle(_translate("TabWidget", "BPM Attenuation Calibrator", None))
        self.addToListButton.setText(_translate("TabWidget", "Add BPM To List", None))
        self.calibrateButton.setText(_translate("TabWidget", "Calibrate Attenuations", None))
        self.clearPVListButton.setText(_translate("TabWidget", "Clear PV List", None))
        self.bpmATTPVList = self.bpmCont.getBPMNames()
        self.i = 0
        while self.i < len(self.bpmATTPVList):
            self.comboBox.setItemText(self.i, _translate("TabWidget", str(self.bpmATTPVList[self.i]), None))
            self.i = self.i + 1
        #self.bpmList.setText(_translate("TabWidget", "BPM List", None))
        self.groupBox.setTitle(_translate("TabWidget", "New BPM Attenuation Values", None))
        self.numShots.setPlainText(_translate("TabWidget", "2", None))
        self.numShotsLabel.setText(_translate("TabWidget", "# Shots", None))
        self.scanRangeLabel.setText(_translate("TabWidget", "ATT Scan Range", None))
        self.newATTVals.setText(_translate("TabWidget", "", None))
        self.lowerBoundLabel.setText(_translate("TabWidget", "Lower Bound", None))
        self.upperBoundLabel.setText(_translate("TabWidget", "Upper Bound", None))
        self.lowerATTBound.setPlainText(_translate("TabWidget", "2", None))
        self.upperATTBound.setPlainText(_translate("TabWidget", "10", None))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.tab), _translate("TabWidget", "Settings", None))
        self.newFont = QtGui.QFont("Comic Sans", 20, QtGui.QFont.Bold)
        self.titleLabel.setFont(self.newFont)
        self.titleLabel.setText(_translate("TabWidget", "VELA/CLARA Beam \nPosition Monitor \nAttenuation \nCalibrator", None))
        self.infoText = "Beamline = "+str(self.beamline)+"     Machine type = "+str(self.machine)+"\n\n"
        self.infoText1 = self.infoText+"Please select the BPMs to calibrate from the list using \nthe drop-down menu and the 'Calibrate BPM' button."
        self.infoText2 = self.infoText1+"\nThe number of shots for each attenuation setting,\n and the range to scan over (from 1 - 20),\n can also be set."
        self.infoText3 = self.infoText2+" Click 'Calibrate attenuations' when \nready. The tabs generated will show the results."
        self.infoLabel.setText(_translate("TabWidget", self.infoText3, None))
        #self.TabWidget.setTabText(self.TabWidget.indexOf(self.tab1), _translate("TabWidget", "Tab 2", None))

    def addPlotTab(self, TabWidget, pvName):
        self.pvName = pvName
        self.TabWidget = TabWidget
        self.TabWidget.setObjectName(_fromUtf8("TabWidget"))
        self.TabWidget.resize(699, 602)
        self.tab1 = QtGui.QWidget()
        self.tab1.setObjectName(_fromUtf8("tab"))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.tab1), _translate("TabWidget", self.pvName, None))
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
        self.tabList.append(self.tab1)
        self.glayoutOutputs.append(self.glayoutOutput)
        self.glayoutOutputs_2.append(self.glayoutOutput_2)
        self.TabWidget.addTab(self.tab1, _fromUtf8(self.pvName))
        self.TabWidget.setObjectName(_fromUtf8(self.pvName))
