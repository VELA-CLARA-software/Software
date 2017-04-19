from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QThreadPool, QObject, QRunnable, pyqtSignal, QThread
import threading
import time
import collections

class scopeWriterArea(QRunnable):
	def __init__(self, view, scopeName, channelName, baselineStart, baselineEnd, signalStart, signalEnd, epicsPV, model):
		super(scopeWriterArea, self).__init__()
		self.view = view
		self.model = model
		self.scopeName = scopeName
		self.channelName = channelName
		self.epicsPV = epicsPV
		self.baselineStart = baselineStart
		self.baselineEnd = baselineEnd
		self.signalStart = signalStart
		self.signalEnd = signalEnd
		self.running = False

	def run(self):
		if self.running == True:
			self.model.readTracesAndWriteAreaToEPICS(self.scopeName, self.channelName, self.baselineStart, self.baselineEnd, self.signalStart, self.signalEnd, self.epicsPV)

class scopeWriterMax(QRunnable):
	def __init__(self, view, scopeName, channelName, epicsPV, model):
		super(scopeWriterMax, self).__init__()
		self.view = view
		self.model = model
		self.scopeName = scopeName
		self.channelName = channelName
		self.epicsPV = epicsPV
		self.running = False

	def run(self):
		if self.running == True:
			self.model.readTracesAndWriteMaxToEPICS(self.scopeName, self.channelName, self.epicsPV)

class scopeWriterMin(QRunnable):
	def __init__(self, view, scopeName, channelName, epicsPV, model):
		super(scopeWriterMin, self).__init__()
		self.view = view
		self.model = model
		self.scopeName = scopeName
		self.channelName = channelName
		self.epicsPV = epicsPV
		self.running = False

	def run(self):
		if self.running == True:
			self.model.readTracesAndWriteMinToEPICS(self.scopeName, self.channelName, self.epicsPV)

class scopeWriterP2P(QRunnable):
	def __init__(self, view, scopeName, channelName, epicsPV, model):
		super(scopeWriterP2P, self).__init__()
		self.view = view
		self.model = model
		self.scopeName = scopeName
		self.channelName = channelName
		self.epicsPV = epicsPV
		self.running = False

	def run(self):
		if self.running == True:
			self.model.readTracesAndWriteP2PToEPICS(self.scopeName, self.channelName, self.epicsPV)

class scopeWriterWorkerSignals(QObject):
	result = pyqtSignal(object)
