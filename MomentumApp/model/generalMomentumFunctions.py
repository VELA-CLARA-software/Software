from epics import caget,caput
import scipy.constants as physics
import os,sys
import time
import math as m
import random as r

sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\Release')
import VELA_CLARA_MagnetControl as mag



class Functions():
	def __init__(self):
		print("Momentum Functions Initialized")
		self.n = 10 #number of shots to average over for a given measuremnet
		self.magInit = mag.init()
		self.magnets = 	self.magInit.virtual_VELA_INJ_Magnet_Controller()


	def stepCurrent(self,magnet,step):
		caput('VM-EBT-INJ-MAG-DIP-01:RIRAN', 0)#for virtual machine
		self.magnets.switchONpsu(magnet)
		DIP = self.magnets.getMagObjConstRef(magnet)
		setI = self.magnets.getSI(magnet)+step
		self.magnets.setSI(magnet,setI,DIP.riTolerance,30)#seet the current and it can wait her untill it reaches to within tolerance
	def getXBPM(self,bpm):
		x=[]
		for i in range(self.n):
			#x.append(self.bpms.getX(bpm))
			x.append(r.gauss(0.5,0.1))# added to fake a step
		return sum(x)/self.n
	def getXScreen(self, screen):
		x=[]
		for i in range(self.n):
			#x.append(self.screens.getX(screen))
			x.append(r.gauss(0.5,0.1))# added to fake a step
		return sum(x)/self.n

		def getSigmaXScreen(self, screen):
			sX=[]
			for i in range(self.n):
				#x.append(self.screens.getSigmaX(screen))
				sX.append(r.gauss(0.5,0.1))# added to fake a step
			return sum(sX)/self.n
	def isBeamOnScreen(self,screen):#this does nothing at the moment
		return True
	def align(self, hcor, bpm,tol, log):
		log.info('Aligned beam using ' + hcor + ' and ' + bpm)
		COR = self.magnets.getMagObjConstRef(hcor)

		#faux data
		x1=300*self.getXBPM(bpm)
		I1=COR.siWithPol
		x2=x1
		I2=0
		while(x2>tol):
			if (COR.riWithPol>0.0):
				initialStep = -0.5
			elif (COR.riWithPol<0.0):
				initialStep = 0.5
			else:
				initialStep = 0.5
			self.stepCurrent(hcor, initialStep)#step
			x2=x1*self.getXBPM(bpm)
			I2=COR.siWithPol
			while(x2>tol):
				I_o = (I1*x2-I2*x1)/(x2-x1)
				self.magnets.setSI(hcor,I_o,COR.riTolerance,10)
				x1=x2
				I1=I2
				I2=I_o
				x2=x2*self.getXBPM(bpm)
				print(x2)
	def bendBeam(self, dipole, bpm, screen, predictedI, tol, log):
		#position of beam
		step = predictedI/100
		x=500 #fake start x position

		#set dipole current to 90% of predicted
		setI = 0.9*predictedI
		self.magnets.setSI(dipole,setI)

		#keep itterration until beam is on screen
		while(self.isBeamOnScreen(screen)==False):
			stepCurrent(dipole,step)
		#measure
		x_old=x
		x=x*self.getXBPM(bpm)
		#start iterative loop
		while(x>tol):
			self.stepCurrent(dipole,step)
			#measure
			x_old=x
			x=self.getXBPM(bpm)*x
			print x
			#shrink step size if step will be too big
			if x<(x_old-x):
				step = step*0.5

		log.info('Centered beam in Spectrometer line using ' + dipole + ' and ' + bpm)
		return self.magnets.getSI(dipole)
	def minimizeBeta(self,quad,screen,step,log):
		I3_1 = 0
		I3_2 = 0
		QUAD = self.magnets.getMagObjConstRef(quad)
		sX_initial =getSigmaXScreen(screen)
		I_initial = QUAD.siWithPol
		sX_1 = sX_initial
		I_1 = QUAD.siWithPol
		sX_2 = sX_initial
		I_2 = QUAD.siWithPol
		#step to left
		while (sX_2<3*sX_initial):
			sX_1 = sX_2
			I_1 = I_2
			self.stepCurrent(quad,-step)
			I_2 = QUAD.siWithPol
			sX_2 = getSigmaXScreen(screen)
		 #At this pot we have gone higher than 3*initial_size. Assume straight line and find prediction for 3*
		  I3_1 = (3*sX_initial*(I_2 - I_1) + (sX_2*I_1 - sX_1*I_2))/(sX_2 - sX_1)

		  #predict where the the other location of the size being 3*the initial_size and go there
		  self.stepCurrent(quad,2*(I_initial - I3_1))
		  I_1 = QUAD.siWithPol
		  sX_1 = getSigmaXScreen(screen)
		  if (sX_1<3*sX_initial):
			  while (sX_2<3*sX_initial):
				  sX_1 = sX_2
				  I_1 = I_2
				  self.stepCurrent(quad,step)
				  I_2 = QUAD.siWithPol
				  sX_2 = getSigmaXScreen(screen)
		else:
			  while (sX_2>3*sX_initial):
				  sX_1 = sX_2
				  I_1 = I_2
				  self.stepCurrent(quad,-step)
				  I_2 = QUAD.siWithPol
				  sX_2 = getSigmaXScreen(screen)

		I3_2 = (3*sX_initial*(I_2 - I_1) + (sX_2*I_1 - sX_1*I_2))/(sX_2 - sX_1)
		self.magnets.setSI(quad,0.5*(I3_1 + I3_2),QUAD.riTolerance,30)

		log.info('Minimizied Beta with '+quad+' on '+screen)
	def fixDispersion(self,quad,screen,log):
		log.info('Fixed Dispersion with '+quad+' on '+screen)
	def findDispersion(self,dipole,screen,log):
		log.info('Determinied Dispersion with '+dipole+' and '+screen)
	def calcMomSpread(self,log):
		log.info('Calculated Momentum Spread')
	def calcMom(self, dipole, I, log):
		log.info('Calculated Momentum')
		DIP = self.magnets.getMagObjConstRef( dipole )
		return (physics.c/1000000000)*DIP.magneticLength*(DIP.slope*I + DIP.intercept)/m.sin(0.25*physics.pi)
	def mom2I(self, dipole, mom):
		#log.info('Converting Momentim to Current for '+ dipole)
		DIP = self.magnets.getMagObjConstRef( dipole )
		#print DIP.magneticLength
		#print mom*m.sin(0.25*physics.pi)
		return (1000000000/physics.c)*((mom*m.sin(0.25*physics.pi)/(DIP.magneticLength) - DIP.intercept))/DIP.slope
		#return ((mom*m.sin(0.25*physics.pi)/(402.9*physics.e) - DIP.intercept))/DIP.slope
