from PyQt4.QtCore import *
from PyQt4.QtGui import *
from  functools import partial
import time

class machineReciever(QObject):

	fromMachine = pyqtSignal(int, 'PyQt_PyObject')

	def __init__(self, machine):
		super(machineReciever, self).__init__()
		self.machine = machine

	def toMachine(self, id, function, args, kwargs):
		ans = getattr(self.machine,str(function))(*args, **kwargs)
		self.fromMachine.emit(id, ans)

class machineSignaller(QObject):

	toMachine = pyqtSignal(int, str, tuple, dict)

	def __init__(self, machine):
		super(machineSignaller, self).__init__()
		self.machine = machine
		self.recievedSignal = {}
		self.signalRecieved = {}
		self.id = -1

	def get(self, id, function, *args, **kwargs):
		self.toMachine.emit(id, function, args, kwargs)
		while self.signalRecieved[id] == False:
			time.sleep(0.001)
		return self.recievedSignal[id]

	def fromMachine(self, id, response):
		self.signalRecieved[id] = True
		self.recievedSignal[id] = response

	def __getattr__(self, attr):
		if 'set' in attr:
			id = int(self.id) + 1
			self.signalRecieved[id] = False
			self.id += 1
			return partial(self.get, id, attr)
		else:
			return getattr(self.machine, attr)
