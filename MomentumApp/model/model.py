from epics import caget,caput
import os,sys
import time
sys.path.append('C:\\Users\\wln24624\\Documents\\VELA-CLARA-Controllers\\Controllers\\VELA\INJECTOR\\velaINJMagnets\\bin\\Release')

#import velaINJMagnetControl as vimc


class Model():
	def __init__(self, view):
		#self.magnets =	vimc.velaINJMagnetController(False,False,False)
		self.view = view
		print("Model Made")
	def hello(self):
		print 'hello'
