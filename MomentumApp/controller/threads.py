from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QThread, pyqtSignal
import sys
sys.path.append('C:\\Users\\wln24624\\Documents\\SOFTWARE\\VELA-CLARA-Software\\Software\\MomentumApp\\model')
import model
import time
class momentumProcedure(QtCore.QThread):
	def __init__(self, view):
		QtCore.QThread.__init__(self)
		self.view = view
		#self.model = model
		self.model = model.Model(view)

	def __del__(self):
		self.wait()

	def run(self):
		self.view.pushButton.setText("RUNNING...")
		#time.sleep(10)
		self.model.measureMomentum()
		self.view.pushButton.setText("Get Momentum")
