import sys,os
from PyQt4 import QtGui, QtCore

import model_CLARA_test2 as model

class App(QtCore.QObject):
	def __init__(self):
		self.model = model.Model()
		print 'Model done'

a = App()
