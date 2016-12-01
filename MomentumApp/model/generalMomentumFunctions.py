from epics import caget,caput
import scipy.constants as phyics
import os,sys
import time
import math as m
sys.path.append('C:\\Users\\wln24624\\Documents\\VELA-CLARA-Controllers\\Controllers\\VELA\INJECTOR\\velaINJMagnets\\bin\\Release')

#import velaINJMagnetControl as vimc


class Functions():
	def __init__(self):

		#self.p = 0
		#self.ps = 0
		#self.pI = 0
		#self.I = 0
		#self.predictedMomentum = 0
		#self.magnets =	vimc.velaINJMagnetController(False,False,False)print("Momentum Functions Initialized")

	def align(self, hcor, bpm, log):
		log.info('Aligned beam using ' + hcor + ' and ' + bpm)

	def bendBeam(self, dipole, bpm, log):
		log.info('Centered beam in Spectrometer line using ' + dipole + ' and ' + bpm)

	def minimizeBeta(self,quad,screen,log):
		log.info('Minimizied Beta with '+quad+' on '+screen)

	def fixDispersion(self,quad,screen,log):
		log.info('Fixed Dispersion with '+quad+' on '+screen)

	def findDispersion(self,dipole,screen,log):
		log.info('Determinied Dispersion with '+dipole+' and '+screen)

	def calcMomSpread(self,log):
		log.info('Calculated Momentum Spread')

	def calcMom(self, dipole, log, I):
		log.info('Calculated Momentum')
		return dipole.L*physics.e*(dipole.m*I + dipole.c)/m.sin(0.5*physics.pi)

	def mom2I(self, dipole, mom):
		return ((mom*m.sin(0.5*physics.pi)/(dipole.L*physics.e) - dipole.c))/dipole.m
