from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QObject
import threading
import Queue
import sys
import time
import threads
import numpy
import pyqtgraph as pg
import epics
from epics import caget,caput


class Controller(QObject):

	def __init__(self, view, model):
		super(Controller, self).__init__()
		self.view = view
		self.model = model
		self.threads = threads
		self.thread = QtCore.QThread()
		self.queue = Queue.Queue()
		self.threading = threading
		#self.MainWindow = QtGui.QTabWidget()
		#self.pool = QtCore.QThreadPool()
		self.pvList = []
		self.lowerList = []
		self.upperList = []

		self.view.pushButton_2.clicked.connect(lambda: self.appendToList())
		self.view.pushButton.clicked.connect(lambda: self.runATTCalibration())

	def runATTCalibration(self):
		self.numShots = int(self.view.plainTextEdit_4.toPlainText())
		self.sliderMin = int(self.view.plainTextEdit_6.toPlainText())
		self.sliderMax = int(self.view.plainTextEdit_7.toPlainText())
		self.dlyValues = [[]] * len(self.pvList)
		self.meanDLY1Values = [[]] * len(self.pvList)
		self.meanDLY2Values = [[]] * len(self.pvList)
		self.pool = QtCore.QThreadPool()
		self.attVals = []
		self.att1Values = [[[] for i in range(self.numShots)] for i in range(self.sliderMin, self.sliderMax)]
		self.att2Values = [[[] for i in range(self.numShots)] for i in range(self.sliderMin, self.sliderMax)]
		self.attVals.append(self.att1Values)
		self.attVals.append(self.att2Values)
		self.attVals.append([])
		self.attVals.append([])

		print self.pvList
		for i in self.pvList:
			self.attVals = self.model.scanAttenuation(i, self.numShots, self.sliderMin, self.sliderMax)
			self.newAttVals = self.model.setAttenuation(i, self.attVals[ 0 ], self.attVals[ 1 ])
			print 'finished'
			self.getValues(self.attVals, i)
		#for i in self.pvList:
		#	print "thread " + i + " started"
		#	self.thread = self.threads.Worker(self.view, i, self.numShots)
		#	self.pool.start(self.thread)
		#	self.dlyValue = self.thread.signals.result.connect(self.getValues)
		#	self.dlyValues.append(self.dlyValue)
		#self.pool.waitForDone()

	def getValues(self, sigList, pvName):
		self.numShots = int(self.view.plainTextEdit_4.toPlainText())
		self.pvName = pvName
		self.att1Vals = []
		self.att2Vals = []
		self.RA1Vals = []
		self.RA2Vals = []
		self.sigList = sigList

		self.makestr = ""
		for i in range(len(self.pvList)):
			if self.pvName == self.pvList[i]:
				self.view.glayoutOutputs[i].clear()
				self.view.glayoutOutputs_2[i].clear()
				self.plotatt1 = self.view.glayoutOutputs[i].addPlot(title="ATT1")
				self.plotatt1Distrib = self.plotatt1.plot(pen=None,symbol='o')
				self.plotatt1Distrib.setData(self.sigList[0].keys(), self.sigList[0].values())
				self.plotatt2 = self.view.glayoutOutputs_2[i].addPlot(title="ATT2")
				self.plotatt2Distrib = self.plotatt2.plot(pen=None,symbol='o')
				self.plotatt2Distrib.setData(self.sigList[1].keys(), self.sigList[1].values())
				self.makestr = self.makestr+("New BPM ATT1 for "+self.pvName+" = "+str(self.model.getBPMReadAttenuation(str(i))[0])+"\n\nNew BPM ATT2 for "+self.pvName+" = "+str(self.model.getBPMReadAttenuation(str(i))[1]))
		self.view.label_4.setText(self.view.label_4.text()+"\n\n"+self.makestr)
		#return sigList

	def appendToList(self):
		#del self.pvList[:]
		self.pvName = str(self.view.comboBox.currentText())
		self.pvList.append(self.pvName)
		self.view.plainTextEdit.insertPlainText(self.pvName+"\n")
		#self.view.plainTextEdit.setPlainText(self.pvName)
		self.view.addPlotTab(self.view.TabWidget, self.pvName)
		return self.pvList
		#self.tab = QtGui.QWidget()
		#self.tab.setObjectName(str(self.pvName))
		#self.newTab = self.view.Ui_TabWidget.addPlotTab(self.tab, self.pvName)
		#self.newTab.setObjectName(_fromUtf8(str(self.pvName)))
