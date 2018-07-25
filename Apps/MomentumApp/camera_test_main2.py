import sys,os
from PyQt4 import QtGui, QtCore

import camera_test_class as camera

class App(QtCore.QObject):
	def __init__(self):
		self.model = camera.Model()
		print 'Model done'

a = App()
