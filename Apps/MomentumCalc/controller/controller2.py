from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys,os
import time

class controllerer():

	def __init__(self, view, model):
		'''define model and view'''
		self.view = view
		self.model = model
		self.view.pushButton.clicked.connect(self.clicked_go)
		self.view.doubleSpinBox_2.valueChanged(self.klychange)
		self.view.doubleSpinBox_3.valueChanged(self.setchange)

	def klychange(self):
		self.model.klypower = self.view.doubleSpinBox_2.value()
		self.view.doubleSpinBox_3.setValue(round(self.model.newsetpoint(),0))

	def setchange(self):
		self.model.setpoint = self.view.doubleSpinBox_3.value()
		self.view.doubleSpinBox_2.setValue(round(self.model.newklypower(),2))

	def clicked_go(self):
		self.model.pulselength = self.view.doubleSpinBox.value()
		self.model.klypower = self.view.doubleSpinBox_2.value()
		self.view.label_4.setText(str(round(self.model.bestcase(),2)))
		self.view.label_5.setText(str(round(self.model.worstcase(),2)))