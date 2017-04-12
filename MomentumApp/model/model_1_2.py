from epics import caget,caput
import os,sys
import time
import scipy.constants as physics
import math as m
import random as r
import numpy as np
from numpy.polynomial import polynomial as P

sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\ASTeC\\Projects\\VELA\\Software\\OnlineModel')
import onlineModel

sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\Release')
import VELA_CLARA_MagnetControl as mag
import VELA_CLARA_BPM_Control as bpm
import VELA_CLARA_LLRFControl as llrf
import VELA_CLARA_PILaserControl as pil

class Model():
	def __init__(self,view):
		self.view = view
		'''vairiables to hold important values'''
		self.p = 0												#momentum
		self.I = 0						#current to bend momentum 45 degrees
		self.pSpread = 0				# momentum spread
		self.ISpread = 0				#current corrensponding to momentum spread
		self.predictedMomentum = 0		# value determined by user in GUI
		self.predictedI = 0				#current corresponding to predicted momentum
		self.n=10
		self.dCurrents =[]
		self.dPositions=[]
		self.fCurrents =[]
		self.fPositions=[]
		self.Dispersion=0

		self.magInit = mag.init()
		self.bpmInit = bpm.init()
		self.pilInit = pil.init()
		self.llrfInit = llrf.init()
		self.magnets = self.magInit.virtual_VELA_INJ_Magnet_Controller()
		self.laser = self.pilInit.virtual_PILaser_Controller()
		self.bpms = self.bpmInit.virtual_VELA_INJ_BPM_Controller()
		self.gun = self.llrfInit.virtual_VELA_LRRG_LLRF_Controller()
		caput('VM-EBT-INJ-MAG-DIP-01:RIRAN', 0)		#This is a fudge: Turning on removing the noise of the magnets being used on the virtual machine
		caput('VM-EBT-INJ-MAG-QUAD-01:RIRAN', 0)
		caput('VM-EBT-INJ-MAG-HCOR-01:RIRAN', 0)
		caput('VM-EBT-INJ-MAG-HCOR-02:RIRAN', 0)
		self.magnets.switchONpsu('DIP01')
		self.magnets.switchONpsu('HCOR01')
		self.magnets.switchONpsu('HCOR02')
		self.magnets.switchONpsu('QUAD01')
		self.magnets.switchONpsu('QUAD06')
		self.ASTRA = onlineModel.ASTRA(self.magnets,None,None,self.magnets,self.gun,None)
		print("Model Initialized")

	#Outline of Momentum Measurement Procedure
	def measureMomentum(self):
		'''1. Preliminaries'''
		if self.view.checkBox_1.isChecked()==True:
			self.predictedMomentum = float(self.view.lineEdit_predictMom.text())
			self.predictedI = self.mom2I('DIP01',self.predictedMomentum)
			print('Predicted Current: '+str(self.predictedI))
			print('Predicted Momentum: '+str(self.predictedMomentum))

		'''2. Align Beam through Dipole'''
		if self.view.checkBox_2.isChecked()==True:
			'''for i in range(3):
				self.func.align('HCOR01','BPM01',0.000001)
				self.func.align('HCOR02','BPM02',0.000001)'''
			print('Doing nout here')

		'''3. Centre in Spec. Line'''
		if self.view.checkBox_3.isChecked()==True:
			self.I = self.bendBeam('DIP01','BPM03','YAG04', self.predictedI, 0.0001) # tol=0.0001 (metres)

		'''4. Convert Current to Momentum'''
		if self.view.checkBox_4.isChecked()==True:
			#self.PL.info('4. Calculate Momentum')
			self.p = self.calcMom('DIP01',self.I)
			print self.p
	#Outline of Momentum Spread Measurement Procedure
	def measureMomentumSpread(self):
		if self.view.checkBox_done_mom.isChecked()==True:
			"""2. Set Disperaion"""
			if self.view.checkBox_1_s.isChecked()==True:
				"""1. Checks"""
				print('hi')#self.PSL.info('1. Run Checks')
				#self.func.minimizeBeta('QUAD01','YAG03',0.01)
				#self.func.minimizeBeta('QUAD03','YAG03',0.01)

			"""2. Set Disperaion"""
			if self.view.checkBox_2_s.isChecked()==True:
				"""2.1 Minimize Beta"""
				#self.PSL.info('2.1 Minimize Beta')
				#self.func.minimizeBeta('QUAD01','YAG03',0.05)
				self.minimizeBeta('QUAD01', 'VM-EBT-INJ-DIA-CAM-04:CAM', 0.05)
				"""2.2 Set Dispersion Size on Spec Line"""
				#self.PSL.info('2.2 Set Dipersion size')
				#self.pySetSI('DIP01',self.I,0.01,30)
				#self.fixDispersion('QUAD06','VM-EBT-INJ-DIA-CAM-05:CAM',-0.05)
				#ONLY in REAL LIFE
				#self.func.magnets.degauss('DIP01')

			"""3. Calculate Dispersion """
			if self.view.checkBox_3_s.isChecked()==True:
				#self.PSL.info('3. Dertermine Dispersion')
				self.Dispersion,beamSigma = self.findDispersion('DIP01','VM-EBT-INJ-DIA-CAM-05:CAM',self.predictedI,5,0.1)
				self.Is = beamSigma/self.Dispersion
				print(self.Is)
				#Haven't done errors yet

			"""4. Calculate Momenum Spread """
			if self.view.checkBox_4_s.isChecked()==True:
				#self.PSL.info('4. Get Momentum Spread')
				self.pSpread = self.calcMomSpread('DIP01',self.Is,self.predictedI)
		else:
			#self.PSL.error('Not confirmed momentum measurement')
			print 'Not confirmed momentum measurement'

	def stepCurrent(self,magnet,step):
		MAG = self.magnets.getMagObjConstRef(magnet)
		setI = MAG.siWithPol+step
		print('Stepping current to: '+str(setI))
		self.magnets.setSI(magnet,setI)
		self.ASTRA.go('V1-YAG01','SP-YAG04')
	def getXBPM(self,bpm):
		x=[]
		for i in range(self.n):
			x.append(self.bpms.getXFromPV(bpm))
		return sum(x)/self.n
	def getXScreen(self,camera):
		x=[]
		for i in range(self.n):
			x.append(caget(camera+':X'))
		return sum(x)/self.n
	def getSigmaXScreen(self,camera):
		sX=[]
		for i in range(self.n):
			sX.append(caget(camera+':SigmaX'))
		return sum(sX)/self.n
	def getSigmaYScreen(self,camera):
		sY=[]
		for i in range(self.n):
			sY.append(caget(camera+':SigmaY'))
		return sum(sX)/self.n
	def isBeamOnScreen(self,screen):											#this does nothing at the moment
		return True
	def align(self, hcor, bpm, tol):
		COR = self.magnets.getMagObjConstRef(hcor)		#create a reference to the corrector
		x1= self.getXBPM(bpm)							#get the x position on the BPM
		I1=COR.siWithPol		#x1,x2,I1,I2 are point to determine a straight linear relationship (I=mx+c)
		x2=x1
		I2=0
		if (COR.riWithPol>0.0):							#determine intial step
			initialStep = -0.0001
		else:
			initialStep = 0.0001
		self.stepCurrent(hcor, initialStep)
		self.ASTRA.go('V1-YAG01','SP-YAG04')										#take inital step
		x2=self.getXBPM(bpm)
		I2=COR.siWithPol
		while(x2>tol):															# Algorithm loops until the current position is < the tolerance 'tol'
			I_o = (I1*x2-I2*x1)/(x2-x1)											# find the zero-crossing of straight line mde from positions at currents I1 and I2
			print('Predicted current intercept at '+str(I_o))
			self.magnets.setSI(hcor,I_o)
			self.ASTRA.go('V1-YAG01','SP-YAG04')				# set magnet to intercept current
			x1=x2																#Get rid of first set of position and current
			I1=I2
			I2=I_o
			x2=self.getXBPM(bpm)
			print('Current at'+str(x2))
		print('Aligned beam using ' + hcor + ' and ' + bpm)
	def bendBeam(self, dipole, bpm, screen, predictedI, tol):
		DIP = self.magnets.getMagObjConstRef(dipole)		#create a reference to the dipole
		step = predictedI/100								#1% of predicted current
		setI = 0.9*predictedI
		self.magnets.setSI(dipole,setI)						#set dipole current to 90% of predicted
		self.ASTRA.go('V1-YAG01','SP-YAG04')
		while(self.isBeamOnScreen(screen)==False):		#keep iterration of a 1% current step until beam is on screen
			self.stepCurrent(magCtrl,dipole,step)
		x_old=0												#fake start x position
		x=self.getXBPM(bpm)							#All BPM posiotn are fake and based of the previous position
																				#it wont stay this way for the real procedure
		while(x>tol):								#start loop that ramps up dipole current (conitines unitl x<tolerance)
			self.stepCurrent(dipole,step)
			x_old=x																# keep a note of teh last beam position to roughly predict the effect of the next step
			x=self.getXBPM(bpm)
			print(x)
			if x<(x_old-x):					#if the step size look like it is will over bend the beam, half it.
				step = step*0.5
		print('Centered beam in Spectrometer line using ' + dipole + ' and ' + bpm)
		return self.magnets.getSI(dipole)			#return the current at which beam has been centered
	def minimizeBeta(self,quad,screen,init_step):
		QUAD = self.magnets.getMagObjConstRef(quad)								#setup
		self.magnets.setSI(quad, 0.3)	#depends if +tine or -tive					#set a fake start current
		self.ASTRA.go('V1-YAG01','SP-YAG04')
		step  = init_step
		I3_1 = 0																#I3_1 is the first value that is 3 time the size of the inita current
		I3_2 = 0
		sX_initial =self.getSigmaXScreen(screen)
		I_initial = QUAD.siWithPol
		sX_1 = sX_initial
		I_1 = QUAD.siWithPol
		sX_2 = sX_initial
		I_2 = QUAD.siWithPol

		while (sX_2<3*sX_initial):												#step 'left', i.e reduce current
			sX_1 = sX_2
			I_1 = I_2
			self.stepCurrent(quad,-step)
			I_2 = QUAD.siWithPol
			sX_2 = self.getSigmaXScreen(screen)
			print('Left Step Screen Width: '+str(sX_2))							#At this pot we have gone higher than 3*initial_size. Assume straight line and find prediction for 3*
		I3_1 = (3*sX_initial*(I_2 - I_1) + (sX_2*I_1 - sX_1*I_2))/(sX_2 - sX_1)

		self.stepCurrent(quad,2*(I_initial - I3_1))								#predict where the the other location of the size being 3*the initial_size and go there
		I_1 = QUAD.siWithPol
		sX_1 = self.getSigmaXScreen(screen)
		if (sX_1<3*sX_initial):
			while (sX_2<3*sX_initial):
				sX_1 = sX_2
				I_1 = I_2
				self.stepCurrent(quad,step)
				I_2 = QUAD.siWithPol
				sX_2 = self.getSigmaXScreen(screen)
				print('Right Step Screen Width: '+str(sX_2))
		else:
			while (sX_2>3*sX_initial):
				sX_1 = sX_2
				I_1 = I_2
				self.stepCurrent(quad,-step)
				I_2 = QUAD.siWithPol
				sX_2 = self.getSigmaXScreen(screen)
				print('Left Step Screen Width: '+str(sX_2))

		I3_2 = (3*sX_initial*(I_2 - I_1) + (sX_2*I_1 - sX_1*I_2))/(sX_2 - sX_1)

		self.magnets.setSI(quad,0.5*(I3_1 + I3_2),QUAD.riTolerance,30)			#assume minimum is half way in between these places so set magnet current to that
		self.ASTRA.go('V1-YAG01','SP-YAG04')
		print('Minimizied Beta with '+quad+' on '+screen)
	def fixDispersion(self,quad,screen,step_size):#THis needs work!!!!
		self.magnets.setSI(quad, -0.1)	#depends if +tine or -tive					#set a fake start current
		self.ASTRA.go('V1-YAG01','SP-YAG04')				#assumes beam is on screen
		sX = self.getSigmaXScreen(screen)
		sX_old = sX
		MaximumBeamSigma = 0.0005
		while (sX>MaximumBeamSigma):
			self.stepCurrent(quad,step_size)
			sX_old = sX
			sX = self.getSigmaXScreen(screen)
			print('Sigma of Beam: '+str(sX))
			if (abs(sX-MaximumBeamSigma)>abs(sX_old-MaximumBeamSigma)):
				step_size = -step_size
	def findDispersion(self,dipole,screen,centering_I,points,leveloff_threshold):
		currents = np.zeros(points)
		positions = np.zeros(points)
		DIP = self.magnets.getMagObjConstRef(dipole)
		#position of beam
		sX=0
		step = centering_I/100
		self.magnets.setSI(dipole,centering_I)						#set dipole current to 90% of predicted
		self.ASTRA.go('V1-YAG01','SP-YAG04')

		#set dipole current to 90% of centering current
		setI = 0.95*centering_I
		self.magnets.setSI(dipole,setI)
		self.ASTRA.go('V1-YAG01','SP-YAG04')
		#I = totalIntensity(screen)
		#I_old = I/2
		#while(I/I_old-1>leveloff_threshold):
		#self.stepCurrent(dipole,step)
		currents[0] = DIP.siWithPol
		positions[0] = self.getXScreen(screen)
		I_diff = 2*(centering_I-currents[0])/(points-1)

		for i in range(1,points):
			self.stepCurrent(dipole,I_diff)
			currents[i] = DIP.siWithPol
			positions[i] = self.getXScreen(screen)
			self.dCurrents=currents
			self.dPositions= positions
			if i==(points-1)/2:
				sX = self.getSigmaXScreen(screen)

		c, stats = P.polyfit(currents,positions,1,full=True)
		self.fCurrents=[0.90*centering_I,1.1*centering_I]
		self.fPositions=[(c[1]*0.90*centering_I)+c[0],(c[1]*1.10*centering_I)+c[0]]
		print(c)
		print('Determinied Dispersion with '+dipole+' and '+screen)
		print('dispersion'+str(c[1])+' and  beamsigma is'+str(sX))
		return c[1],sX



	def calcMomSpread(self,dipole, Is, I):
		D = self.magnets.getMagObjConstRef(dipole)
		mom1= (400.0033/D.magneticLength)*(np.polyval(D.fieldIntegralCoefficients, abs(I-Is))*physics.c*180)/(45*physics.pi*1000000000)
		mom2= (400.0033/D.magneticLength)*(np.polyval(D.fieldIntegralCoefficients, abs(Is+I))*physics.c*180)/(45*physics.pi*1000000000)
		print(mom1-mom2)/2
		return abs(mom1-mom2)/2
	def calcMom(self, dipole, I):
		D = self.magnets.getMagObjConstRef(dipole)
		return (400.0033/D.magneticLength)*(np.polyval(D.fieldIntegralCoefficients, abs(I))*physics.c*180)/(45*physics.pi*1000000000)
	def mom2I(self,dipole,mom):
		D = self.magnets.getMagObjConstRef(dipole)
		coeffs = list(D.fieldIntegralCoefficients)
		print(1000000000*(mom*physics.pi*45)/(physics.c*180))
		coeffs[-1] -= (D.magneticLength/400.0033)*(1000000000*(mom*physics.pi*45)/(physics.c*180))
		roots = np.roots(coeffs)
		current = roots[-1].real
		return -current
