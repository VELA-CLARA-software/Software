from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QThreadPool, QObject, QRunnable, pyqtSignal, QThread
import threading
import time
import mainModel
import mainController
import mainView

class Worker(threading.Thread):
	def __init__(self, pvName, rangeSta, rangeEnd, numShots, repRate):
		self.allgo = threading.Condition()
		self.view = mainView.Ui_MainWindow()
		self.model = mainModel.Model(self.view)
		self.pvName = pvName
		self.rangeSta = rangeSta
		self.rangeEnd = rangeEnd
		self.numShots = numShots
		self.repRate = repRate

	def run(self):
		self.model.setRanPV(self.pvName, self.rangeSta, self.rangeEnd, self.numShots, self.repRate)
