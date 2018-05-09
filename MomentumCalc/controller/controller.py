from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys,os
import time

class controllerer():

	def __init__(self, view, model):
		'''define model and ui'''
		self.view = view
		self.model = model
		self.view.pushButton.clicked.connect(self.clicked_go)

	def clicked_go(self):
		self.model.pulselength = self.view.doubleSpinBox.value()
		self.model.klypower = self.view.doubleSpinBox_2.value()
		self.view.label_4.setText(str(round(self.model.bestcase(),2)))
		self.view.label_5.setText(str(round(self.model.worstcase(),2)))
	
