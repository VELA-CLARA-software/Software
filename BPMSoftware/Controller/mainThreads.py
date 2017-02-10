from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QThreadPool, QObject, QRunnable, pyqtSignal, QThread
import sys,os
print os.path.abspath(__file__)
import randomPVs

class attCalWorkerSignals(QObject):
	result = pyqtSignal(object)

class ranPVs(QRunnable):
	def __init__(self, pvName, rangeSta, rangeEnd, numShots, repRate, pvType):
		#This is only used for the virtual machine, and uses the SetRandomPVs package to send random values to the bpms
		#to allow for software testing. The PV names are set automatically - they're simply the VELA injector BPMs because
		#it doesn't really matter which ones you test on the virtual machine. Feel free to add more in mainController.py
		#if that would be useful.
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
