from epics import caget,caput
import os,sys
import time
sys.path.append('C:\\Users\\wln24624\\Documents\\VELA-CLARA-Controllers\\Controllers\\VELA\INJECTOR\\velaINJMagnets\\bin\\Release')

#import velaINJMagnetControl as vimc


class Functions():
	def __init__(self):
		self.momentum = 0
		self.momentumSpread = 0
		self.predictedMomentum = 0
		#self.magnets =	vimc.velaINJMagnetController(False,False,False)print("Momentum Functions Initialized")

	def align(self, corrector, effector, log):
		log.info('Aligned beam using ' + corrector + ' and ' + effector)

	def bendBeam(self, dipole, observer, log):
		log.info('Centered beam in Spectrometer line using ' + dipole + ' and ' + observer)
