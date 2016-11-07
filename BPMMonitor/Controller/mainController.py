from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QObject
import functools
import random
import threading
import sys
import time
import threads
import numpy
import epics
from epics import caget,caput
import collections
sys.path.append('D:\\VELA-CLARA_software\\VELA-CLARA-Controllers-New-Structure-With-Magnets\\bin\\Release')

import VELA_CLARA_BPM_Control as vbpmc

class Controller(QObject):

	def __init__(self, view, model, bpmCont, scopeCont):
		super(Controller, self).__init__()
		self.view = view
		self.model = model
		self.threads = threads
		self.threading = threading
		self.pvList = []
		self.view.trajectoryButton.clicked.connect(lambda: self.view.setComboBox(self.view.tab))
		#self.view.trajectoryButton.clicked.connect(lambda: self.getPVList())
		self.view.individualButton.clicked.connect(lambda: self.view.setComboBox(self.view.tab))
		self.view.pushButton_2.clicked.connect(lambda: self.appendToList())
		self.view.pushButton_3.clicked.connect(lambda: self.addPlotTabs())
		self.view.pushButton.clicked.connect(lambda: self.startPlots())

	def getPVList(self):
		if self.view.trajectoryButton.isChecked():
			self.trajectory = str(self.view.comboBox.currentText())
			if self.trajectory == "VELA INJ":
				self.pvList = self.model.velaInjList
			elif self.trajectory == "VELA Spectrometer":
				self.pvList = self.model.velaSP1List
		return self.pvList

	def addPlotTabs(self):
		self.pvList = []
		self.pvList = self.getPVList()
		for i in self.pvList:
			self.view.addPlotTab(self.view.TabWidget, i)

	def startPlots(self):
		self.plotUpdate = QtCore.QTimer()
		self.plotUpdate.timeout.connect(self.onTimer)
		self.plotUpdate.start(100)

	def onTimer(self):
		self.i = 0
		#self.numShots = int(self.view.getNumShots.toPlainText())
		self.numShots = 1
		self.bpmData = self.model.monitorBPMs(self.pvList, self.numShots)
		self.bpmXData = self.bpmData[0]
		self.bpmYData = self.bpmData[1]
		self.bpmQData = self.bpmData[2]
		self.bpmATT1Data = self.bpmData[3]
		self.bpmATT2Data = self.bpmData[4]
		for i in self.pvList:
			self.plotTitle = i + ": \nX = " + str(round(self.bpmXData[i],2)) + " \tY = " + str(round(self.bpmYData[i],2)) + " \tQ = " + str(round(self.bpmQData[i],2)) + " \nATT1 = " + str(self.bpmATT1Data[i]) + " \tATT2 = " + str(self.bpmATT2Data[i])
			self.view.plotList[i].animate(self.bpmXData[i], self.bpmYData[i], self.plotTitle)

	def appendToList(self):
		if self.view.individualButton.isChecked():
			self.pvName = str(self.view.comboBox.currentText())
			self.pvList.append(self.pvName)
			self.view.plainTextEdit.insertPlainText(self.pvName+"\n")
			self.view.addPlotTab(self.view.TabWidget, self.pvName)
		return self.pvList
