from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QThreadPool, QObject, QRunnable, pyqtSignal, QThread
import threading
import time

class attCalWorker(QRunnable):
	def __init__(self, view, pvList, numShots, sliderMin, sliderMax, model):
		super(attCalWorker, self).__init__()
		self.view = view
		self.model = model
		#self.pvName = pvName
		self.pvList = pvList
		self.numShots = numShots
		self.sliderMin = sliderMin
		self.sliderMax = sliderMax
		self.signals = attCalWorkerSignals()

	def run(self):
		self.attVals = self.model.scanAttenuation(self.pvList, self.numShots, self.sliderMin, self.sliderMax)
		self.newAttVals = self.model.setAttenuation(self.pvList, self.attVals[ 0 ], self.attVals[ 1 ])
		#Emits signal when the scanAttenuation and setAttenuation functions are complete
		self.signals.result.emit(self.attVals)

class attCalWorkerSignals(QObject):
	result = pyqtSignal(object)
