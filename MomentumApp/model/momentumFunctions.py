










from epics import caget,caput
import scipy.constants as physics
import os,sys
import time
import math as m
import random as r
import numpy as np
from numpy.polynomial import polynomial as P



class dummyOM():
		def __init__(self):
			print 'made a dummy OM'
		def run():
			print 'running NO simulation'

'''This Class contain function to use in a momentum procdure independant '''
class Functions():
	def __init__(self, OM = dummyOM() ):
		self.simulate = OM

	def stepCurrent(self,ctrl,magnet,step):
		MAG = ctrl.getMagObjConstRef(magnet)
		setI = MAG.siWithPol + step
		print('Stepping current to: '+str(setI))
		ctrl.setSI(magnet,setI)
		self.simulate.run()
	def getXBPM(self,ctrl,bpm,N):
		x=[]
		for i in range(N):
			x.append(ctrl.getXFromPV(bpm))
		return sum(x)/N
	def getXScreen(self,ctrl,camera,N):
		x=[]
		for i in range(N):
			x.append(caget(camera+':X'))
		return sum(x)/N
	def getSigmaXScreen(self,ctrl,camera,N):
		sX=[]
		for i in range(N):
			sX.append(caget(camera+':SigmaX'))
		return sum(sX)/N
	def getSigmaYScreen(self,ctrl,camera,N):
		sY=[]
		for i in range(N):
			sY.append(caget(camera+':SigmaY'))
		return sum(sX)/N
	def isBeamOnScreen(self,screen):
		#this does nothing at the moment
		return True											#Add a controller to input
	def align(self,hctrl,hcor, bctrl, bpm, tol, N):
		COR = hctrl.getMagObjConstRef(hcor)										#create a reference to the corrector
		x1= self.getXBPM(bctrl, bpm, N)											#get the x position on the BPM
		I1 = COR.siWithPol														#x1,x2,I1,I2 are point to determine a straight linear relationship (I=mx+c)
		x2=x1
		I2=0
		if (COR.riWithPol>0.0):													#determine intial step
			initialStep = -0.0001
		else:
			initialStep = 0.0001
		self.stepCurrent(hctrl, hcor, initialStep)
		self.simulate.run()														#take inital step
		x2=self.getXBPM(bctrl, bpm, N)
		I2=COR.siWithPol
		while(x2>tol):															# Algorithm loops until the current position is < the tolerance 'tol'
			I_o = (I1*x2-I2*x1)/(x2-x1)											# find the zero-crossing of straight line mde from positions at currents I1 and I2
			print('Predicted current intercept at '+str(I_o))
			hctrl.setSI(hcor,I_o)
			self.simulate.run()													# set magnet to intercept current
			x1=x2																#Get rid of first set of position and current
			I1=I2
			I2=I_o
			x2=self.getXBPM(bctrl, bpm, N)
			print('Current at'+str(x2))
		print('Aligned beam using ' + hcor + ' and ' + bpm)
	def bendBeam(self,dctrl,dipole,bctrl,bpm,screen, predictedI, tol, N=1):
		DIP = dctrl.getMagObjConstRef(dipole)									#create a reference to the dipole
		step = predictedI/100													#1% of predicted current
		setI = 0.9*predictedI
		print ('90% of predicticted current is: ',setI)
		dctrl.setSI(dipole,setI)												#set dipole current to 90% of predicted
		self.simulate.run()
		while(self.isBeamOnScreen(screen)==False):								#keep iterration of a 1% current step until beam is on screen
			self.stepCurrent(magCtrl,dipole,step)
		x_old=0																	#fake start x position
		x=self.getXBPM(bctrl, bpm, N)											#All BPM posiotn are fake and based of the previous position
																				#it wont stay this way for the real procedure
		while(x>tol):															#start loop that ramps up dipole current (conitines unitl x<tolerance)
			self.stepCurrent(dctrl, dipole, step)
			x_old=x																# keep a note of teh last beam position to roughly predict the effect of the next step
			x=self.getXBPM(bctrl, bpm, N)
			print(x)
			if x<(x_old-x):														#if the step size look like it is will over bend the beam, half it.
				step = step*0.5
		print('Centered beam in Spectrometer line using ' + dipole + ' and ' + bpm)
		return dctrl.getSI(dipole)										#return the current at which beam has been centered
	def minimizeBeta(self,qctrl,quad,sctrl,screen,init_step,N=1):
		QUAD = qctrl.getMagObjConstRef(quad)								#setup
		qctrl.setSI(quad, 0.3)	#depends if +tine or -tive				#set a fake start current
		self.simulate.run()
		step  = init_step
		I3_1 = 0																#I3_1 is the first value that is 3 time the size of the inita current
		I3_2 = 0
		sX_initial =self.getSigmaXScreen(sctrl,screen,N)
		I_initial = QUAD.siWithPol
		sX_1 = sX_initial
		I_1 = QUAD.siWithPol
		sX_2 = sX_initial
		I_2 = QUAD.siWithPol

		while (sX_2<3*sX_initial):												#step 'left', i.e reduce current
			sX_1 = sX_2
			I_1 = I_2
			self.stepCurrent(qctrl, quad, -step)
			I_2 = QUAD.siWithPol
			sX_2 = self.getSigmaXScreen(sctrl,screen,N)
			print('Left Step Screen Width: '+str(sX_2))							#At this pot we have gone higher than 3*initial_size. Assume straight line and find prediction for 3*
		I3_1 = (3*sX_initial*(I_2 - I_1) + (sX_2*I_1 - sX_1*I_2))/(sX_2 - sX_1)

		self.stepCurrent(qctrl, quad, 2*(I_initial - I3_1))						#predict where the the other location of the size being 3*the initial_size and go there
		I_1 = QUAD.siWithPol
		sX_1 = self.getSigmaXScreen(sctrl,screen,N)
		if (sX_1<3*sX_initial):
			while (sX_2<3*sX_initial):
				sX_1 = sX_2
				I_1 = I_2
				self.stepCurrent(qctrl, quad, step)
				I_2 = QUAD.siWithPol
				sX_2 = self.getSigmaXScreen(sctrl,screen,N)
				print('Right Step Screen Width: '+str(sX_2))
		else:
			while (sX_2>3*sX_initial):
				sX_1 = sX_2
				I_1 = I_2
				self.stepCurrent(qctrl, quad, -step)
				I_2 = QUAD.siWithPol
				sX_2 = self.getSigmaXScreen(sctrl,screen,N)
				print('Left Step Screen Width: '+str(sX_2))

		I3_2 = (3*sX_initial*(I_2 - I_1) + (sX_2*I_1 - sX_1*I_2))/(sX_2 - sX_1)

		self.magnets.setSI(quad,0.5*(I3_1 + I3_2),QUAD.riTolerance,30)			#assume minimum is half way in between these places so set magnet current to that
		self.simulate.run()
		print('Minimizied Beta with '+quad+' on '+screen)
	def fixDispersion(self,qctrl,quad,sctrl,screen,step_size,N=1):
		#THis needs work!!!!
		qctrl.setSI(quad, -0.1)	#depends if +tine or -tive				#set a fake start current
		self.simulate.run()														#assumes beam is on screen
		sX = self.getSigmaXScreen(sctrl, screen, N)
		sX_old = sX
		MaximumBeamSigma = 0.0005
		while (sX>MaximumBeamSigma):
			self.stepCurrent(qctrl, quad, step_size)
			sX_old = sX
			sX = self.getSigmaXScreen(sctrl, screen, N)
			print('Sigma of Beam: '+str(sX))
			if (abs(sX-MaximumBeamSigma)>abs(sX_old-MaximumBeamSigma)):
				step_size = -step_size
	def findDispersion(self,dctrl,dipole,sctrl,screen,centering_I,points,leveloff_threshold,N=1):
		currents = np.zeros(points)
		positions = np.zeros(points)
		DIP = dctrl.getMagObjConstRef(dipole)
		#position of beam
		sX=0
		dctrl.setSI(dipole,centering_I)									#set dipole current to 90% of predicted
		self.simulate.run()

		#set dipole current to 95% of centering current
		setI = 0.95*centering_I
		print setI
		dctrl.setSI(dipole,setI)
		self.simulate.run()
		#I = totalIntensity(screen)
		#I_old = I/2
		#while(I/I_old-1>leveloff_threshold):
		#self.stepCurrent(dipole,step)
		currents[0] = DIP.siWithPol
		positions[0] = self.getXScreen(sctrl,screen,N)
		I_diff = 2*(centering_I-currents[0])/(points-1)

		for i in range(1,points):
			self.stepCurrent(dctrl, dipole, I_diff)
			currents[i] = DIP.siWithPol
			positions[i] = self.getXScreen(sctrl,screen,N)
			self.dCurrents=currents
			self.dPositions= positions
			if i==(points-1)/2:
				sX = self.getSigmaXScreen(sctrl,screen,N)

		c, stats = P.polyfit(currents,positions,1,full=True)
		self.fCurrents=[0.90*centering_I,1.1*centering_I]
		self.fPositions=[(c[1]*0.90*centering_I)+c[0],(c[1]*1.10*centering_I)+c[0]]
		print(c)
		print('Determinied Dispersion with '+dipole+' and '+screen)
		print('dispersion'+str(c[1])+' and  beamsigma is'+str(sX))
		return c[1],sX

	'''The Follwing have been altered to waork with the online model (400.0033)'''
	def calcMomSpread(self,dctrl,dipole, Is, I):
		D = dctrl.getMagObjConstRef(dipole)
		mom1= (400.0033/D.magneticLength)*(np.polyval(D.fieldIntegralCoefficients, abs(I-Is))*physics.c*180)/(45*physics.pi*1000000000)
		mom2= (400.0033/D.magneticLength)*(np.polyval(D.fieldIntegralCoefficients, abs(Is+I))*physics.c*180)/(45*physics.pi*1000000000)
		print(mom1-mom2)/2
		return abs(mom1-mom2)/2
	def calcMom(self, dctrl,dipole, I):
		D = dctrl.getMagObjConstRef(dipole)
		return (400.0033/D.magneticLength)*(np.polyval(D.fieldIntegralCoefficients, abs(I))*physics.c*180)/(45*physics.pi*1000000000)
	def mom2I(self,dctrl,dipole,mom):
		D = dctrl.getMagObjConstRef(dipole)
		coeffs = list(D.fieldIntegralCoefficients)
		print coeffs
		print(1000000000*(mom*physics.pi*45)/(physics.c*180))
		coeffs[-1] -= (D.magneticLength/400.0033)*(1000000000*(mom*physics.pi*45)/(physics.c*180))
		roots = np.roots(coeffs)
		current = roots[-1].real
		return -current
