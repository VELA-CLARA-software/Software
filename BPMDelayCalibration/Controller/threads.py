from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QThreadPool, QObject, QRunnable, pyqtSignal, QThread
import pyqtgraph
import threading
import time
import mainModel
import mainController
import mainView

class Worker(QRunnable):
	#self.signal = QtCore.Signal(list)#signal to broadcast name
	def __init__(self, view, pvName, numShots):#(self, view, pvName, numShots):
		super(Worker, self).__init__()
		self.view = view
		self.model = mainModel.Model()
		self.pvName = pvName
		self.numShots = numShots
		self.signals = WorkerSignals()
		self.dlyVals = [[[[] for i in range(5)] for i in range(int(self.numShots))] for i in range(2)]
		self.dlyVals.append([])
		self.dlyVals.append([])

	#def __del__(self):
	#	self.wait()

	def run(self):
		self.dly1Vals = self.model.scanDLY1(self.pvName, self.numShots)
		self.newDLY1 = self.model.setMinDLY1(self.pvName, self.dly1Vals[4], self.dly1Vals[5])
		self.dly2Vals = self.model.scanDLY2(self.pvName, self.numShots)
		self.newDLY2 = self.model.setMinDLY2(self.pvName, self.dly2Vals[4], self.dly2Vals[5])


		print 'finished'
		self.dlyVals[0] = self.dly1Vals[4]
		self.dlyVals[1] = self.dly2Vals[4]
		print self.dly2Vals[6]
		print self.dly1Vals[6]
		self.dlyVals[2] = self.dly1Vals[6]
		self.dlyVals[3] = self.dly2Vals[6]
		self.signals.result.emit(self.dlyVals)

class WorkerSignals(QObject):
	result = pyqtSignal(list)
