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
		self.view.doubleSpinBox_2.valueChanged.connect(self.klychange)
		self.view.spinBox_3.valueChanged.connect(self.setchange)

	def klychange(self):
		self.view.spinBox_3.valueChanged.disconnect(self.setchange)
		self.model.klypower = self.view.doubleSpinBox_2.value()
		self.view.spinBox_3.setValue(int(self.model.newsetpoint()))
		self.view.spinBox_3.valueChanged.connect(self.setchange)

	def setchange(self):
		self.view.doubleSpinBox_2.valueChanged.disconnect(self.klychange)
		self.model.setpoint = self.view.spinBox_3.value()
		self.view.doubleSpinBox_2.setValue(round(self.model.newklypower(),5))
		self.view.doubleSpinBox_2.valueChanged.connect(self.klychange)
		
	def clicked_go(self):
		self.model.pulselength = self.view.doubleSpinBox.value()
		self.model.klypower = self.view.doubleSpinBox_2.value()
		self.view.label_4.setText(str(round(self.model.bestcase(),5)))
		self.view.label_5.setText(str(round(self.model.worstcase(),5)))