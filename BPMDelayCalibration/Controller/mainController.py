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

		self.view.addToListButton.clicked.connect(lambda: self.appendToList())
		self.view.calibrateButton.clicked.connect(lambda: self.runDLYCalibration())

	def runDLYCalibration(self):
		self.numShots = int(self.view.numShots.toPlainText())
		self.sliderMin = int(self.view.lowerDLYBound.toPlainText())
		self.sliderMax = int(self.view.lowerDLYBound.toPlainText())
		self.dlyValues = [[]] * len(self.pvList)
		self.meanDLY1Values = [[]] * len(self.pvList)
		self.meanDLY2Values = [[]] * len(self.pvList)
		self.pool = QtCore.QThreadPool()
		self.dlyVals = []
		self.dly1Values = [[[] for i in range(self.numShots)] for i in range(self.sliderMin, self.sliderMax)]
		self.dly2Values = [[[] for i in range(self.numShots)] for i in range(self.sliderMin, self.sliderMax)]
		self.dlyVals.append(self.dly1Values)
		self.dlyVals.append(self.dly2Values)
		self.dlyVals.append([])
		self.dlyVals.append([])

		print self.pvList
		for i in self.pvList:
			self.dly1Vals = self.model.scanDLY1(i, self.numShots, self.sliderMin, self.sliderMax)
			self.newDLY1 = self.model.setMinDLY1(i, self.dly1Vals[4], self.dly1Vals[5])
			self.dly2Vals = self.model.scanDLY2(i, self.numShots)
			self.newDLY2 = self.model.setMinDLY2(i, self.dly2Vals[4], self.dly2Vals[5])
			print 'finished'
			self.dlyVals[0] = self.dly1Vals[4]
			self.dlyVals[1] = self.dly2Vals[4]
			self.dlyVals[2] = self.dly1Vals[6]
			self.dlyVals[3] = self.dly2Vals[6]
			self.getValues(self.dlyVals, i)
		#for i in self.pvList:
		#	print "thread " + i + " started"
		#	self.thread = self.threads.Worker(self.view, i, self.numShots)
		#	self.pool.start(self.thread)
		#	self.dlyValue = self.thread.signals.result.connect(self.getValues)
		#	self.dlyValues.append(self.dlyValue)
		#self.pool.waitForDone()

	def getValues(self, sigList, pvName):
		self.numShots = int(self.view.numShots.toPlainText())
		self.pvName = pvName
		self.DLY1Vals = []
		self.DLY2Vals = []
		self.RD1Vals = []
		self.RD2Vals = []
		self.sigList = sigList
		print len(sigList[0][0])

		#for a, b in zip(range(0, len(sigList[0])), range(0, len(sigList[1]))):
		#	self.DLY1Vals.append(numpy.mean(self.sigList[0][a]))
		#	self.DLY2Vals.append(numpy.mean(self.sigList[1][a]))
		#	self.RD1Vals.append(self.sigList[2])
		#	self.RD2Vals.append(self.sigList[3])
		for a in range(0, len(sigList[0])):
			self.DLY1Vals.append(numpy.mean(self.sigList[0][a]))
			self.RD1Vals.append(self.sigList[2])
		for b in range(0, len(sigList[1])):
			self.DLY2Vals.append(numpy.mean(self.sigList[1][b]))
			self.RD2Vals.append(self.sigList[3])
		print self.DLY1Vals, "        ", self.DLY2Vals


		self.makestr = ""
		for i in range(len(self.pvList)):
			if self.pvName == self.pvList[i]:
				self.view.glayoutOutputs[i].clear()
				self.view.glayoutOutputs_2[i].clear()
				self.plotDLY1 = self.view.glayoutOutputs[i].addPlot(title="DLY1")
				self.plotDLY1Distrib = self.plotDLY1.plot(pen=None,symbol='o')
				self.plotDLY1Distrib.setData(self.RD1Vals[i][0:len(self.RD1Vals)], self.DLY1Vals)
				self.plotDLY2 = self.view.glayoutOutputs_2[i].addPlot(title="DLY2")
				self.plotDLY2Distrib = self.plotDLY2.plot(pen=None,symbol='o')
				self.plotDLY2Distrib.setData(self.RD2Vals[i][0:len(self.RD2Vals)], self.DLY2Vals)
				self.makestr = self.makestr+("New BPM DLY1 for "+self.pvName+" = "+str(self.model.getBPMReadDLY(str(i))[0])+"\n\nNew BPM DLY2 for "+self.pvName+" = "+str(self.model.getBPMReadDLY(str(i))[1]))
		self.view.newDLYVals.setText(self.view.label_4.text()+"\n\n"+self.makestr)
		#return sigList

	def appendToList(self):
		self.pvName = str(self.view.comboBox.currentText())
		self.pvList.append(self.pvName)
		self.view.bpmPVList.insertPlainText(self.pvName+"\n")
		self.view.addPlotTab(self.view.TabWidget, self.pvName)
		return self.pvList
