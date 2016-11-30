from epics import caget,caput
import os,sys
import time
import generalMomentumFunctions as general
sys.path.append('C:\\Users\\wln24624\\Documents\\VELA-CLARA-Controllers\\Controllers\\VELA\INJECTOR\\velaINJMagnets\\bin\\Release')

#import velaINJMagnetControl as vimc


class Model():
	def __init__(self, view):
		#self.magnets =	vimc.velaINJMagnetController(False,False,False)
		self.view = view
		print("Model Made")

	def hello(self):
		print 'hello'

	def measureMomentum(self):
		"""1. Align Beam through Dipole"""

		"""2. Centre in Spectrometer Line"""

		"""3. Convert Current to Momentum"""

	def measureMomentumSpread(self):
		"""1. Minimize Beta"""

		"""2. Set Dispersion Size"""

		"""3. Find """
