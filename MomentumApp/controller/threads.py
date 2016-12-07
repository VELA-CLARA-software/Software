from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QThread

import time
class momentumProcedure(QThread):
	def __init__(self, view, model):
		QtCore.QThread.__init__(self)
		self.view = view
		self.model = model

	def __del__(self):
		self.wait()

	def run(self):
		self.view.pushButton.setText("RUNNING...")
		self.model.measureMomentum()
		self.view.pushButton.setText("Get Momentum")
