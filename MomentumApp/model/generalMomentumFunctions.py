from epics import caget,caput
import scipy.constants as physics
import os,sys
import time
import math as m
import random as r
import numpy as np
from numpy.polynomial import polynomial as P

sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\Release')
import VELA_CLARA_MagnetControl as mag



class Functions():
	def __init__(self):
		self.n = 10 #number of shots to average over for a given measuremnet
		self.magInit = mag.init()
		self.magnets = self.magInit.virtual_VELA_INJ_Magnet_Controller()
		caput('VM-EBT-INJ-MAG-DIP-01:RIRAN', 0)
		caput('VM-EBT-INJ-MAG-QUAD-01:RIRAN', 0)
		caput('VM-EBT-INJ-MAG-HCOR-01:RIRAN', 0)
		caput('VM-EBT-INJ-MAG-HCOR-02:RIRAN', 0)
		#for virtual machine
		self.magnets.switchONpsu('DIP01')
		self.magnets.switchONpsu('HCOR01')
		self.magnets.switchONpsu('HCOR02')
		self.magnets.switchONpsu('QUAD01')
		print("Momentum Functions Initialized")




	def pySetSI(self,magnet,ss,tol,maxWait):
		MAG = self.magnets.getMagObjConstRef(magnet)
		self.magnets.setSI(magnet,ss)
		#self.magnets.setSI(magnet,ss,tol,maxWait)
		t_start = time.time()
		time_diff = 0
		while (abs(MAG.riWithPol-ss)>tol and time_diff<maxWait):
			time.sleep(0.1)
			time_diff = time.time()-t_start

	def stepCurrent(self,magnet,step):
		MAG = self.magnets.getMagObjConstRef(magnet)
		setI = self.magnets.getSI(magnet)+step
		self.pySetSI(magnet,setI,MAG.riTolerance,10)#seet the current and it can wait her untill it reaches to within tolerance
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
	def align(self, hcor, bpm, tol):
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
				self.pySetSI(hcor,I_o,COR.riTolerance,10)
				x1=x2
				I1=I2
				I2=I_o
				x2=x2*self.getXBPM(bpm)
				#print(x2)
		print('Aligned beam using ' + hcor + ' and ' + bpm)
	def bendBeam(self, dipole, bpm, screen, predictedI, tol):
		DIP = self.magnets.getMagObjConstRef(dipole)
		#position of beam
		step = predictedI/100
		x=500 #fake start x position

		#set dipole current to 90% of predicted
		setI = 0.9*predictedI
		self.pySetSI(dipole,setI,DIP.riTolerance,10)

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

		print('Centered beam in Spectrometer line using ' + dipole + ' and ' + bpm)
		return self.magnets.getSI(dipole)
	def minimizeBeta(self,quad,screen,init_step):
		step  = init_step
		I3_1 = 0
		I3_2 = 0
		QUAD = self.magnets.getMagObjConstRef(quad)
		sX_initial =self.getSigmaXScreen(screen)
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
			sX_2 = self.getSigmaXScreen(screen)
		#At this pot we have gone higher than 3*initial_size. Assume straight line and find prediction for 3*
		I3_1 = (3*sX_initial*(I_2 - I_1) + (sX_2*I_1 - sX_1*I_2))/(sX_2 - sX_1)

		#predict where the the other location of the size being 3*the initial_size and go there
		self.stepCurrent(quad,2*(I_initial - I3_1))
		I_1 = QUAD.siWithPol
		sX_1 = self.getSigmaXScreen(screen)
		if (sX_1<3*sX_initial):
			while (sX_2<3*sX_initial):
				sX_1 = sX_2
				I_1 = I_2
				self.stepCurrent(quad,step)
				I_2 = QUAD.siWithPol
				sX_2 = self.getSigmaXScreen(screen)
		else:
			while (sX_2>3*sX_initial):
				sX_1 = sX_2
				I_1 = I_2
				self.stepCurrent(quad,-step)
				I_2 = QUAD.siWithPol
				sX_2 = self.getSigmaXScreen(screen)

		I3_2 = (3*sX_initial*(I_2 - I_1) + (sX_2*I_1 - sX_1*I_2))/(sX_2 - sX_1)
		self.pySetSI(quad,0.5*(I3_1 + I3_2),QUAD.riTolerance,30)
		print('Minimizied Beta with '+quad+' on '+screen)
	def fixDispersion(self,quad,screen,step_size):

		sX = self.getSigmaXScreen(screen)
		sX_old = sX
		image_width = 1920 #To be used for now...
		MaximumBeamSize = 0.3*image_width
		while (sX<MaximumBeamSize):
			self.stepCurrent(quad,step_size)
			sX_old = sX
			sX = self.getSigmaXScreen(screen)
			if (sX>sX_old):
				step_size = -step_size

		#log.info('Fixed Dispersion with '+quad+' on '+screen)
	def findDispersion(self,dipole,screen,centering_I,points,leveloff_threshold):
		currents = np.zeros(points)
		positions = np.zeros(points)
		DIP = self.magnets.getMagObjConstRef(dipole)
		#position of beam
		sX=0
		step = centering_I/100
		#set dipole current to 90% of centering current
		setI = 0.9*centering_I
		self.pySetSI(dipole,setI,DIP.riTolerance,10)
		I = self.screens.totalIntensity(screen)
		I_old = I/2

		while(I/I_old-1>leveloff_threshold):
			self.stepCurrent(dipole,step)
		current[0] = DIP.siWithPol
		position[0] = self.getXScreen(screen)
		I_diff = 2*(centering_I-current[0])/(point-1)

		for i in range(1,points):
			self.stepCurrent(dipole,I_diff)
			current[i] = DIP.siWithPol
			positions[i] = self.getXScreen(screen)
			if i==(point-1)/2:
				sX = self.getSigmaXScreen(screen)

		c, stats = P.polyfit(currents,positions,1,full=True)
		return c[0],sX

		print('Determinied Dispersion with '+dipole+' and '+screen)




	def calcMomSpread(self, dipole, Is):
		DIP = self.magnets.getMagObjConstRef( dipole )
		return (physics.c/(1000000000))*(DIP.slope*I + DIP.intercept)/m.sin(0.25*physics.pi)

	def calcMom(self, dipole, I):
		DIP = self.magnets.getMagObjConstRef( dipole )
		return (physics.c/(1000000000))*(DIP.slope*I + DIP.intercept)/m.sin(0.25*physics.pi)
	def mom2I(self, dipole, mom):
		#log.info('Converting Momentim to Current for '+ dipole)
		DIP = self.magnets.getMagObjConstRef( dipole )
		return(1000000000/physics.c)*((mom*m.sin(0.25*physics.pi) - DIP.intercept))/DIP.slope
