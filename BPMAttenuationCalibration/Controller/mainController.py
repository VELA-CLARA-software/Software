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
sys.path.append('D:\\VELA-CLARA_software\\VELA-CLARA-Controllers-New-Structure-With-Magnets\\bin\\Release')

import VELA_CLARA_BPM_Control as vbpmc


class Controller(QObject):

	def __init__(self, view, model, bpmCont, scopeCont):
		super(Controller, self).__init__()
		self.view = view
		self.model = model
		self.threads = threads
		#self.thread = QtCore.QThread()
		#self.queue = Queue.Queue()
		self.threading = threading
		#self.MainWindow = QtGui.QTabWidget()
		#self.pool = QtCore.QThreadPool()
		self.pvList = vbpmc.std_vector_string()
		self.lowerList = []
		self.upperList = []

		self.view.addToListButton.clicked.connect(lambda: self.appendToList())
		self.view.clearPVListButton.clicked.connect(lambda: self.clearPVList())
		self.view.calibrateButton.clicked.connect(lambda: self.runATTCalibration())

	def runATTCalibration(self):
		self.numShots = int(self.view.numShots.toPlainText())
		self.sliderMin = int(self.view.lowerATTBound.toPlainText())
		self.sliderMax = int(self.view.upperATTBound.toPlainText())
		self.attValues = [[]] * len(self.pvList)
		self.pool = QtCore.QThreadPool()
		self.pool.setMaxThreadCount(len(self.pvList))

		print self.pvList
		#for i in self.pvList:
		#	self.attVals = self.model.scanAttenuation(i, self.numShots, self.sliderMin, self.sliderMax)
		#	self.newAttVals = self.model.setAttenuation(i, self.attVals[ 0 ], self.attVals[ 1 ])
		#	print 'finished'
		#	self.getValues(self.attVals, i)
		#for i in self.pvList:
			#print "thread " + i + " started"
			#self.thread = self.threads.Worker(self.view, i, self.numShots, self.sliderMin, self.sliderMax, self.model)

			#self.attValue = self.thread.signals.result.connect(self.getValues)
			#self.pool.start(self.thread)
			#self.attValues.append(self.attValue)
		self.thread = self.threads.Worker(self.view, self.pvList, self.numShots, self.sliderMin, self.sliderMax, self.model)
		self.attValue = self.thread.signals.result.connect(self.getValues)
		self.pool.start(self.thread)
		self.pool.waitForDone()

	def clearPVList(self):
		self.view.bpmPVList.clear()
		self.i = 1
		while self.i <= len(self.pvList) + 1:
			self.view.TabWidget.removeTab(self.i)
			self.i = self.i + 1
		self.pvList = []

	def getValues(self, sigList):
		self.numShots = int(self.view.numShots.toPlainText())
		self.att1Vals = []
		self.att2Vals = []
		self.RA1Vals = []
		self.RA2Vals = []
		self.sigList = sigList
		print self.sigList[1]
		self.makestr = ""
		for i in range(len(self.pvList)):
			self.view.glayoutOutputs[i].clear()
			self.view.glayoutOutputs_2[i].clear()
			self.plotatt1 = self.view.glayoutOutputs[i].addPlot(title="ATT1")
			self.plotatt1Distrib = self.plotatt1.plot(pen=None,symbol='o')
			self.plotatt1Distrib.setData(self.sigList[0].values()[i].keys(), self.sigList[0].values()[i].values())
			self.plotatt2 = self.view.glayoutOutputs_2[i].addPlot(title="ATT2")
			self.plotatt2Distrib = self.plotatt2.plot(pen=None,symbol='o')
			self.plotatt2Distrib.setData(self.sigList[1].values()[i].keys(), self.sigList[1].values()[i].values())
			self.makestr = self.makestr+("\nNew BPM ATT1 for "+self.pvList[i]+" = "+str(self.model.getBPMReadAttenuation(str(self.pvList[i]))[0]))
			self.makestr = self.makestr+("\nNew BPM ATT2 for "+self.pvList[i]+" = "+str(self.model.getBPMReadAttenuation(str(self.pvList[i]))[1]))
		self.view.newATTVals.setText(self.view.newATTVals.text()+"\n\n"+self.makestr)
		#return sigList

	def appendToList(self):
		#del self.pvList[:]
		self.pvName = str(self.view.comboBox.currentText())
		self.pvList.append(self.pvName)
		self.view.bpmPVList.insertPlainText(self.pvName+"\n")
		#self.view.plainTextEdit.setPlainText(self.pvName)
		self.view.addPlotTab(self.view.TabWidget, self.pvName)
		return self.pvList
		#self.tab = QtGui.QWidget()
		#self.tab.setObjectName(str(self.pvName))
		#self.newTab = self.view.Ui_TabWidget.addPlotTab(self.tab, self.pvName)
		#self.newTab.setObjectName(_fromUtf8(str(self.pvName)))
