from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys,os
import time
from epics import caget,caput

class Controller():

	def __init__(self, view, model):
		'''define model and view'''
		self.view = view
		self.model = model

		self.view.pushButton.clicked.connect(self.model.function)
