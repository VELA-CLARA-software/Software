from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QThreadPool, QObject, QRunnable, pyqtSignal, QThread
import sys,os
print os.path.abspath(__file__)
sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'..\..\..\SetRandomPVs\Package')
import randomPVs

class attCalWorkerSignals(QObject):
	result = pyqtSignal(object)

class ranPVs(QRunnable):
	def __init__(self, pvName, rangeSta, rangeEnd, numShots, repRate, pvType):
		super(ranPVs, self).__init__()
		self.randomPVs = randomPVs
		self.setRanPVs = self.randomPVs.setRandomPV()
		self.pvName = pvName
		self.rangeSta = rangeSta
		self.rangeEnd = rangeEnd
		self.numShots = numShots
		self.repRate = repRate
		self.pvType = pvType

	def run(self):
		self.runRandomPVs = self.setRanPVs.caputRanPV(self.pvName, self.rangeSta, self.rangeEnd, self.numShots, self.repRate, self.pvType)
		#self.signals.result.emit(self.runRandomPVs)
