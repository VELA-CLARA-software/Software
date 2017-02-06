from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QThread, pyqtSignal

import time

class runASTRAThread(QThread):
	#signal = pyqtSignal()#signal to broadcast name
	def __init__(self, view, model):
		QtCore.QThread.__init__(self)
		self.view = view
		self.model = model

	def __del__(self):
		self.wait()

	def run(self):
		self.view.runASTRA_Btn.setText("RUNNING...")
		self.model.runASTRA()
		self.view.runASTRA_Btn.setText("Run Machine")
