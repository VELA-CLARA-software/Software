from epics import caget,caput
import scipy.constants as physics
import os,sys
import time
import math as m
import random as r
import numpy as np
from numpy.polynomial import polynomial as P


def stepCurrent(self,magCtrl,magnet,step):
	MAG = magCtrl.getMagObjConstRef(magnet)
	setI = MAG.siWithPol+step
	print('Stepping current to: 'setI)
	magCtrl.setSI(magnet,setI)
	ASTRA.go('V1-YAG01','SP-YAG04')

def getXBPM(self,bpmCtrl,bpm,n):
	x=[]
	for i in range(n):
		x.append(bpmCtrl.getXFromPV(bpm))
	return sum(x)/n

def getXScreen(self,camera,n):
	x=[]
	for i in range(n):
		x.append(caget(camera+':X'))
	return sum(x)/n

def getSigmaXScreen(self, camera,n):
	sX=[]
	for i in range(n):
		x.append(caget(camera+':SigmaX'))
	return sum(sX)/n

def isBeamOnScreen(self,screen):											#this does nothing at the moment
	return True

def align(self, bpmCtrl, magCtrl, hcor, bpm, tol):
	n=10
	COR = magCtrl.getMagObjConstRef(hcor)								#create a reference to the corrector
	#faux data
	x1= getXBPM(bpmCtrl,bpm,n)												#get the x position on the BPM
	I1=COR.siWithPol														#x1,x2,I1,I2 are point to determine a straight linear relationship (I=mx+c)
	x2=x1
	I2=0

	if (COR.riWithPol>0.0):													#determine intial step
		initialStep = -0.0001
	elif (COR.riWithPol<0.0001):
		initialStep = 0.0001
	else:
		initialStep = 0.0001
	stepCurrent(hcor, initialStep)										#take inital step
	x2=getXBPM(bpmCtrl,bpm,n)
	I2=COR.siWithPol
	while(x2>tol):															# Algorithm loops until the current position is < the tolerance 'tol'
		I_o = (I1*x2-I2*x1)/(x2-x1)											# find the zero-crossing of straight line mde from positions at currents I1 and I2
		print('Predicted current intercept at '+str(I_o))
		magCtrl.setSI(hcor,I_o)
		ASTRA.go('V1-YAG01','SP-YAG04')				# set magnet to intercept current
		x1=x2																#Get rid of first set of position and current
		I1=I2
		I2=I_o
		x2=getXBPM(bpmCtrl,bpm,n)
		print('Current at'+str(x2))
	print('Aligned beam using ' + hcor + ' and ' + bpm)

'''Function to bend the Beam'''
def bendBeam(self, magCtrl, bpmCtrl, dipole, bpm, screen, predictedI, tol):
	DIP = magCtrl.getMagObjConstRef(dipole)							#create a reference to the dipole

	step = predictedI/100													#1% of predicted current
	setI = 0.9*predictedI
	magCtrl.setSI(dipole,setI)						#set dipole current to 90% of predicted
	ASTRA.go('V1-YAG01','SP-YAG04')
	while(isBeamOnScreen(screen)==False):								#keep iterration of a 1% current step until beam is on screen
		stepCurrent(magCtrl,dipole,step)

	x_old=0															#fake start x position
	x=sgetXBPM(magCtrl,bpm,n)													#All BPM posiotn are fake and based of the previous position
																			#it wont stay this way for the real procedure
	while(x>tol):															#start loop that ramps up dipole current (conitines unitl x<tolerance)
		stepCurrent(dipole,step)
		x_old=x																# keep a note of teh last beam position to roughly predict the effect of the next step
		x=getXBPM(bpmCtrl,bpm,n)
		print(x)
		if x<(x_old-x):														#if the step size look like it is will over bend the beam, half it.
			step = step*0.5
	print('Centered beam in Spectrometer line using ' + dipole + ' and ' + bpm)
	return magCtrl.getSI(dipole)										#return the current at which beam has been centered

''''Function to minimize Beta (one Quad, one Screen)'''
def minimizeBeta(self, magCtrl, quad,screen,init_step):
	QUAD = magCtrl.getMagObjConstRef(quad)								#setup
	magCtrl.setSI(quad, 4)						#set a fake start current
	ASTRA.go('V1-YAG01','SP-YAG04')
	step  = init_step
	I3_1 = 0																#I3_1 is the first value that is 3 time the size of the inita current
	I3_2 = 0
	sX_initial =getSigmaXScreen(screen)
	I_initial = QUAD.siWithPol
	sX_1 = sX_initial
	I_1 = QUAD.siWithPol
	sX_2 = sX_initial
	I_2 = QUAD.siWithPol

	while (sX_2<3*sX_initial):												#step 'left', i.e reduce current
		sX_1 = sX_2
		I_1 = I_2
		stepCurrent(quad,-step)
		I_2 = QUAD.siWithPol
		sX_2 = getSigmaXScreen(screen)
		print('Left Step Screen Width: '+str(sX_2))							#At this pot we have gone higher than 3*initial_size. Assume straight line and find prediction for 3*
	I3_1 = (3*sX_initial*(I_2 - I_1) + (sX_2*I_1 - sX_1*I_2))/(sX_2 - sX_1)

	stepCurrent(quad,2*(I_initial - I3_1))								#predict where the the other location of the size being 3*the initial_size and go there
	I_1 = QUAD.siWithPol
	sX_1 = getSigmaXScreen(screen)
	if (sX_1<3*sX_initial):
		while (sX_2<3*sX_initial):
			sX_1 = sX_2
			I_1 = I_2
			stepCurrent(quad,step)
			I_2 = QUAD.siWithPol
			sX_2 = getSigmaXScreen(screen)
			print('Right Step Screen Width: '+str(sX_2))
	else:
		while (sX_2>3*sX_initial):
			sX_1 = sX_2
			I_1 = I_2
			stepCurrent(quad,-step)
			I_2 = QUAD.siWithPol
			sX_2 = getSigmaXScreen(screen)
			print('Left Step Screen Width: '+str(sX_2))

	I3_2 = (3*sX_initial*(I_2 - I_1) + (sX_2*I_1 - sX_1*I_2))/(sX_2 - sX_1)

	magCtrl.setSI(quad,0.5*(I3_1 + I3_2),QUAD.riTolerance,30)			#assume minimum is half way in between these places so set magnet current to that
	ASTRA.go('V1-YAG01','SP-YAG04')
	print('Minimizied Beta with '+quad+' on '+screen)

'''Fixes beam to a 0.3 times the size of the screen'''
def fixDispersion(self,magCtrl,quad,screen,step_size):								#assumes beam is on screen
	sX = getSigmaXScreen(screen)
	sX_old = sX
	MaximumBeamSigma = 5
	while (sX<MaximumBeamSigma):
		stepCurrent(quad,step_size)
		sX_old = sX
		sX = getSigmaXScreen(screen)
		if (sX>sX_old):
			step_size = -step_size

'''Find Dispersion by scanning dipole'''
def findDispersion(self,magCtrl,dipole,screen,centering_I,points,leveloff_threshold):
	currents = np.zeros(points)
	positions = np.zeros(points)
	DIP = magCtrl.getMagObjConstRef(dipole)
	#position of beam
	sX=0
	step = centering_I/100
	#set dipole current to 90% of centering current
	setI = 0.9*centering_I
	magCtrl.setSI(dipole,setI)
	ASTRA.go('V1-YAG01','SP-YAG04')
	I = totalIntensity(screen)
	I_old = I/2

	while(I/I_old-1>leveloff_threshold):
		stepCurrent(dipole,step)
	current[0] = DIP.siWithPol
	position[0] = getXScreen(screen)
	I_diff = 2*(centering_I-current[0])/(point-1)

	for i in range(1,points):
		stepCurrent(dipole,I_diff)
		current[i] = DIP.siWithPol
		positions[i] = getXScreen(screen)
		if i==(point-1)/2:
			sX = getSigmaXScreen(screen)

	c, stats = P.polyfit(currents,positions,1,full=True)
	return c[0],sX

	print('Determinied Dispersion with '+dipole+' and '+screen)


'''Conversion Calculations'''
def calcMomSpread(self,magCtrl,dipole, Is):
	D = getMagObjConstRef(dipole)
	return (np.polyval(D.fieldIntegralCoefficients, abs(Is))*physics.c*180)/(45*physics.pi*1000000000)

def calcMom(self, magCtrl, dipole, I):
	D = getMagObjConstRef(dipole)
	return (np.polyval(D.fieldIntegralCoefficients, abs(I))*physics.c*180)/(45*physics.pi*1000000000)

def mom2I(self, magCtrl, dipole, mom):
	D = getMagObjConstRef(dipole)
	coeffs = list(D.fieldIntegralCoefficients)
	print(1000000000*(mom*physics.pi*45)/(physics.c*180))
	coeffs[-1] -= (1000000000*(mom*physics.pi*45)/(physics.c*180))
	roots = np.roots(coeffs)
	current = roots[-1].real
	return -current
