from epics import caget,caput
import scipy.constants as phyics
import os,sys
import time
import math as m
sys.path.append('C:\\Users\\wln24624\\Documents\\VELA-CLARA-Controllers\\Controllers\\VELA\INJECTOR\\velaINJMagnets\\bin\\Release')

import velaINJMagnetControl as vimc


class Functions():
	def __init__(self):
		print("Momentum Functions Initialized")
		self.n = 0 #number of shots to average over for a given measuremnet
		self.magnets =	vimc.velaINJMagnetController(False,False,False)
	def align(self, hcor, bpm, log):
		log.info('Aligned beam using ' + hcor + ' and ' + bpm)

	def stepCurrent(magnet,step):
		setI = self.magnets.getSI(magnet)+step
		self.magnets.setSI(magnet,setI,tol,10)#seet the current and it can wait her untill it reaches to within tolerance

	def getXBPM(self,bpm):
		x=[]
		for i in range(self.n):
			x.append(self.bpms.getX(bpm))
		return sum(x)/self.n

	def getXScreen(self, screen):
		x=[]
		for i in range(self.n):
			x.append(self.screens.getX(screen))
		return sum(x)/self.n

	def bendBeam(self, dipole, bpm, screen, predictedI, tol, log):
		#position of beam
		step = predictedI/100
		x=999
		#set dipole current to 90% of predicted
		setI = 0.9*predictedI
		self.magnets.setSI(dipole,setI)

		while(isBeamOnScreen(screen)==False):
			stepCurrent(dipole,step)
		#measure
		x_old=x
		x=getXBPM(bpm)
		#start iterative loop
		while(x>tol):
			stepCurrent(dipole,step)
			#measure
			x_old=x
			x=getXBPM(bpm)
			#shrink step size if step will be too big
			if x<(x_old-x):
				step = step*0.5

		log.info('Centered beam in Spectrometer line using ' + dipole + ' and ' + bpm)
		return self.magnets.getSI(dipole)

	def minimizeBeta(self,quad,screen,log):
		log.info('Minimizied Beta with '+quad+' on '+screen)

	def fixDispersion(self,quad,screen,log):
		log.info('Fixed Dispersion with '+quad+' on '+screen)

	def findDispersion(self,dipole,screen,log):
		log.info('Determinied Dispersion with '+dipole+' and '+screen)

	def calcMomSpread(self,log):
		log.info('Calculated Momentum Spread')

	def calcMom(self, dipole, I, log):
		log.info('Calculated Momentum')
		return dipole.L*physics.e*(dipole.m*I + dipole.c)/m.sin(0.5*physics.pi)

	def mom2I(self, dipole, mom):
		return ((mom*m.sin(0.5*physics.pi)/(dipole.L*physics.e) - dipole.c))/dipole.m
