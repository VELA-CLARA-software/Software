from epics import caget,caput
import os,sys
import time
import generalMomentumFunctions as general



class Model():
	def __init__(self,view):
		self.func = general.Functions()
		self.view = view
		'''vairiables to hold important values'''
		self.p = 0																#momentum
		self.I = 0																#current to bend momentum 45 degrees
		self.ps = 0																# momentum spread
		self.Is = 0																#current corrensponding to momentum spread
		self.predictedMomentum = 0												# value determined by user in GUI
		self.predictedI = 0														#current corresponding to predicted momentum

		'''self.n = 10 															#number of shots to average over for a given measuremnet
		self.magInit = mag.init()
		self.bpmInit = bpm.init()
		self.pilInit = pil.init()
		self.llrfInit = llrf.init()
		self.magnets = self.magInit.virtual_VELA_INJ_Magnet_Controller()
		self.laser = self.pilInit.virtual_PILaser_Controller()
		self.bpms = self.bpmInit.virtual_VELA_INJ_BPM_Controller()
		self.gun = self.llrfInit.virtual_VELA_LRRG_LLRF_Controller()
		caput('VM-EBT-INJ-MAG-DIP-01:RIRAN', 0)									#This is a fudge: Turning on removing the noise of the magnets being used on the virtual machine
		caput('VM-EBT-INJ-MAG-QUAD-01:RIRAN', 0)
		caput('VM-EBT-INJ-MAG-HCOR-01:RIRAN', 0)
		caput('VM-EBT-INJ-MAG-HCOR-02:RIRAN', 0)
		self.magnets.switchONpsu('DIP01')
		self.magnets.switchONpsu('HCOR01')
		self.magnets.switchONpsu('HCOR02')
		self.magnets.switchONpsu('QUAD01')
		self.ASTRA = onlineModel.ASTRA(self.magnets,None,None,self.magnets,self.gun,None)'''
		print("Model Initialized")

	#Outline of Momentum Measurement Procedure
	def measureMomentum(self):
		'''1. Preliminaries'''
		if self.view.checkBox_1.isChecked()==True:
			#self.PL.info('1. Preliminaries')
			self.predictedMomentum = float(self.view.lineEdit_predictMom.text())
			self.predictedI = self.func.mom2I('DIP01',self.predictedMomentum)
			print(self.predictedI)
			print(self.predictedMomentum)
			#self.predictedI=-1.5

		'''2. Align Beam through Dipole'''
		if self.view.checkBox_2.isChecked()==True:
			#self.PL.info('2. Aligning Beam through Dipole')
			for i in range(3):
				#self.func.align('HCOR01','BPM01',0.001)
				self.func.align('HCOR02','BPM02',0.000001)

		'''3. Centre in Spec. Line'''
		if self.view.checkBox_3.isChecked()==True:
			#self.PL.info('3. Center Down Spec. Line')
			self.I = self.func.bendBeam('DIP01','BPM03','YAG04', self.predictedI, 0.0001) # tol=1 (pixel)

		'''4. Convert Current to Momentum'''
		if self.view.checkBox_4.isChecked()==True:
			#self.PL.info('4. Calculate Momentum')
			self.p = self.func.calcMom('DIP01',self.I)
			print self.p
	#Outline of Momentum Spread Measurement Procedure
	def measureMomentumSpread(self):
		if self.view.checkBox_done_mom.isChecked()==True:
			"""2. Set Disperaion"""
			if self.view.checkBox_1_s.isChecked()==True:
				"""1. Checks"""
				#self.PSL.info('1. Run Checks')
				#self.func.minimizeBeta('QUAD01','YAG03',0.01)
				#self.func.minimizeBeta('QUAD03','YAG03',0.01)
				print('HI')

			"""2. Set Disperaion"""
			if self.view.checkBox_2_s.isChecked()==True:
				"""2.1 Minimize Beta"""
				#self.PSL.info('2.1 Minimize Beta')
				self.func.minimizeBeta('QUAD01','YAG03',0.05)

				"""2.2 Set Dispersion Size on Spec Line"""
				#self.PSL.info('2.2 Set Dipersion size')
				#self.pySetSI('DIP01',self.I,0.01,30)
				self.func.fixDispersion('QUAD06','YAG04',0.05)
				self.func.magnets.degauss('DIP01')

			"""3. Calculate Dispersion """
			if self.view.checkBox_3_s.isChecked()==True:
				#self.PSL.info('3. Dertermine Dispersion')
				Dispersion,beamWidth = self.func.findDispersion('DIP01','YAG04',self.J,11,0.1)
				self.Is = Dispersion*beamWidth
				#Haven't done errors yet

			"""4. Calculate Momenum Spread """
			if self.view.checkBox_4_s.isChecked()==True:
				#self.PSL.info('4. Get Momentum Spread')
				self.func.calcMomSpread(self.Is)
		else:
			#self.PSL.error('Not confirmed momentum measurement')
			print 'Not confirmed momentum measurement'
