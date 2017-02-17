from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QObject
import functools
import random
import threading
import sys
import time
import numpy
import epics
from epics import caget,caput
import collections
#sys.path.append('D:\\VELA-CLARA_software\\VELA-CLARA-Controllers-New-Structure-With-Magnets\\bin\\Release')

#import VELA_CLARA_BPM_Control as vbpmc

class monController(QObject):

	def __init__(self, view, model, bpmCont, scopeCont):
		super(monController, self).__init__()
		self.view = view
		self.model = model
		self.threading = threading
		self.pvList = []
		#The user can choose to get all BPMs for a given trajectory, or plot individual BPMs
		self.view.trajectoryButton.clicked.connect(lambda: self.view.setComboBox(self.view.tab))
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
		#Numshots is set automatically - this can be changed if people want
		self.numShots = 1
		#BPM data is acquired in monmainModel.py and sent here
		self.bpmData = self.model.monitorBPMs(self.pvList, self.numShots)
		self.bpmXData = self.bpmData[0]
		self.bpmYData = self.bpmData[1]
		self.bpmQData = self.bpmData[2]
		self.bpmATT1Data = self.bpmData[3]
		self.bpmATT2Data = self.bpmData[4]
		self.bpmResData = self.bpmData[5]
		#Plots are generated using the animate function in monmainView.py
		for i in self.pvList:
			self.plotTitle = i + ": \nX = " + str(round(self.bpmXData[i],2)) + " mm   Y = " + str(round(self.bpmYData[i],2)) + " mm   Q = " + str(round(self.bpmQData[i],2))
			self.plotTitle1 = self.plotTitle+" \nATT1 = " + str(self.bpmATT1Data[i]) + "   ATT2 = " + str(self.bpmATT2Data[i]) + "   Res = " + str(round(self.bpmResData[i],2)) + " mm"
			self.view.plotList[i].animate(self.bpmXData[i], self.bpmYData[i], self.plotTitle1)

	def appendToList(self):
		if self.view.individualButton.isChecked():
			self.pvName = str(self.view.comboBox.currentText())
			self.pvList.append(self.pvName)
			self.view.plainTextEdit.insertPlainText(self.pvName+"\n")
			self.view.addPlotTab(self.view.TabWidget, self.pvName)
		return self.pvList
