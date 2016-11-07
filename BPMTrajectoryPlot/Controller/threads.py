from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QThreadPool, QObject, QRunnable, pyqtSignal, QThread
import pyqtgraph
import threading
import time
#import mainModel
#import mainController
#import mainView

class Worker(QRunnable):
	#self.signal = QtCore.Signal(list)#signal to broadcast name
	def __init__(self, view, pvList, numShots, sliderMin, sliderMax, model):#(self, view, pvName, numShots):
		super(Worker, self).__init__()
		self.view = view
		self.model = model
		#self.pvName = pvName
		self.pvList = pvList
		self.numShots = numShots
		self.sliderMin = sliderMin
		self.sliderMax = sliderMax
		self.signals = WorkerSignals()

	#def __del__(self):
	#	self.wait()

	def run(self):
		self.attVals = self.model.scanAttenuation(self.pvList, self.numShots, self.sliderMin, self.sliderMax)
		self.newAttVals = self.model.setAttenuation(self.pvList, self.attVals[ 0 ], self.attVals[ 1 ])
		self.signals.result.emit(self.attVals)

class WorkerSignals(QObject):
	result = pyqtSignal(object)
