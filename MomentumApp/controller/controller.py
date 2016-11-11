from PyQt4 import QtGui, QtCore
import sys
import time
import numpy as np
import pyqtgraph as pg
from epics import caget,caput
sys.path.append('C:\\Users\\wln24624\\Documents\\SOFTWARE\\VELA-CLARA-Software\\Software\\Striptool\\')
import striptool

class Controller():

	def __init__(self, view, model):
		self.view = view
		self.model = model
		print 'controller made'
		self.view.checkBox_all.stateChanged.connect(self.setChecks_mom)
		self.view.checkBox_all_s.stateChanged.connect(self.setChecks_mom_s)

	def setChecks_mom(self):
		if self.view.checkBox_all.isChecked()==True:
			self.view.checkBox_1.setChecked (True)
			self.view.checkBox_2.setChecked (True)
			self.view.checkBox_3.setChecked (True)
			self.view.checkBox_4.setChecked (True)
		elif self.view.checkBox_all.isChecked()==False:
			self.view.checkBox_1.setChecked (False)
			self.view.checkBox_2.setChecked (False)
			self.view.checkBox_3.setChecked (False)
			self.view.checkBox_4.setChecked (False)

	def setChecks_mom_s(self):
		if self.view.checkBox_all_s.isChecked()==True:
			self.view.checkBox_1_s.setChecked (True)
			self.view.checkBox_2_s.setChecked (True)
			self.view.checkBox_3_s.setChecked (True)
			self.view.checkBox_4_s.setChecked (True)
		elif self.view.checkBox_all_s.isChecked()==False:
			self.view.checkBox_1_s.setChecked (False)
			self.view.checkBox_2_s.setChecked (False)
			self.view.checkBox_3_s.setChecked (False)
			self.view.checkBox_4_s.setChecked (False)
