from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QThreadPool, QObject, QRunnable, pyqtSignal, QThread
import pyqtgraph
import threading
import time
import collections

class dlyWorker(QRunnable):
	def __init__(self, view, pvList, numShots, sliderMin, sliderMax, model):
		super(dlyWorker, self).__init__()
		self.view = view
		self.model = model
		self.pvList = pvList
		self.numShots = numShots
		self.sliderMin = sliderMin
		self.sliderMax = sliderMax
		self.signals = dlyWorkerSignals()
		self.dlyVals = {name:[[] for i in range(4)] for name in self.pvList}

	def run(self):
		self.dly1Vals = self.model.scanDLY1(self.pvList, self.numShots, self.sliderMin, self.sliderMax)
		self.newDLY1 = self.model.setMinDLY1(self.pvList, self.dly1Vals[9])
		self.dly2Vals = self.model.scanDLY2(self.pvList, self.numShots, self.dly1Vals[9])
		self.newDLY2 = self.model.setMinDLY2(self.pvList, self.dly2Vals[9])

		print 'finished'
		self.dlyVals[0] = self.dly1Vals[6]
		self.dlyVals[1] = self.dly1Vals[9]
		self.dlyVals[2] = self.dly2Vals[6]
		self.dlyVals[3] = self.dly2Vals[9]
		#Emits signal when the scanDLY and setMinDLY functions are complete
		self.signals.result.emit(self.dlyVals)

class dlyWorkerSignals(QObject):
	result = pyqtSignal(object)
