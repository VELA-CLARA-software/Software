""""Momentum Measurement Procedures for CLARA  PH1"""

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""Ingredients"""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from epics import caget,caput
import os,sys
import time
import scipy.constants as physics
import math as m
import random as r
import numpy as np
from numpy.polynomial import polynomial as P
os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12"
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
os.environ["EPICS_CA_SERVER_PORT"]="6000"
sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\ASTeC\\Projects\\VELA\\Software\\OnlineModel')
sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\stagetim')
import onlineModel
import VELA_CLARA_Magnet_Control as mag
import VELA_CLARA_BPM_Control as bpm
import VELA_CLARA_LLRF_Control as llrf
import VELA_CLARA_PILaser_Control as pil

import momentumFunctions

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class Model():
	def __init__(self,view):
		self.view = view
		'''vairiables to hold important values'''
		self.p = 0						#momentum
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
		self.Vmagnets = self.magInit.virtual_VELA_INJ_Magnet_Controller()
		self.Cmagnets = self.magInit.virtual_CLARA_PH1_Magnet_Controller()
		self.laser = self.pilInit.virtual_PILaser_Controller()
		self.Cbpms = self.bpmInit.virtual_CLARA_INJ_BPM_Controller()
		self.C2Vbpms = self.bpmInit.virtual_CLARA_2_VELA_BPM_Controller()
		self.gun = self.llrfInit.virtual_CLARA_LRRG_LLRF_Controller()
		self.LINAC01 = 	self.llrfInit.virtual_L01_LLRF_Controller()
		self.Cmagnets.switchONpsu('DIP01')
		self.Cmagnets.switchONpsu('S01-HCOR1')
		self.Cmagnets.switchONpsu('S01-HCOR2')
		self.Cmagnets.switchONpsu('S02-HCOR01')
		self.Cmagnets.switchONpsu('S02-HCOR02')
		self.Cmagnets.switchONpsu('S02-QUAD1')
		self.Cmagnets.switchONpsu('S02-QUAD2')
		self.ASTRA = onlineModel.ASTRA(V_MAG_Ctrl=self.Vmagnets,
											C_S01_MAG_Ctrl=self.Cmagnets,
											C_S02_MAG_Ctrl=self.Cmagnets,
											C2V_MAG_Ctrl=self.Cmagnets,
											V_RF_Ctrl=None,
											C_RF_Ctrl=self.gun,
											L01_RF_Ctrl=self.LINAC01,
											messages=False)
		self.ASTRA.startElement = 'C1-GUN'
		self.ASTRA.stopElement = 'CV-YAG01'
		self.ASTRA.initDistrib = 'temp-start.ini'
		self.ASTRA.initCharge = 0.25
		self.gun.setAmpMVM(65)
		self.LINAC01.setAmpMVM(20)
		self.func = momentumFunctions.Functions(OM=self.ASTRA)
		print("Model Initialized")

	#Outline of Momentum Measurement Procedure
	def measureMomentum(self):
		'''1. Preliminaries'''
		if self.view.checkBox_1.isChecked()==True:
			self.predictedMomentum = float(self.view.lineEdit_predictMom.text())
			self.predictedI = self.func.mom2I(self.Cmagnets,
											'DIP01',
											self.predictedMomentum)
			print('Predicted Current: '+str(self.predictedI))
			print('Predicted Momentum: '+str(self.predictedMomentum))

		'''2. Align Beam through Dipole'''
		if self.view.checkBox_2.isChecked()==True:
			#for i in range(3):
				#self.func.align('HCOR01','BPM01',0.000001)
				#self.func.align('HCOR02','BPM02',0.000001)'''
			print('No allignment here')

		'''3. Centre in Spec. Line'''
		if self.view.checkBox_3.isChecked()==True:
			self.I = self.func.bendBeam(self.Cmagnets,'DIP01',
										self.C2Vbpms,'CV-BPM01',
										'YAG01',
						 				self.predictedI, 0.0001) 				# tol=0.0001 (metres)

		'''4. Convert Current to Momentum'''
		if self.view.checkBox_4.isChecked()==True:
			#self.PL.info('4. Calculate Momentum')
			self.p = self.func.calcMom(self.Cmagnets,'DIP01',self.I)
			print self.p
	#Outline of Momentum Spread Measurement Procedure
	def measureMomentumSpread(self):
		if self.view.checkBox_done_mom.isChecked()==True:
			#1. Checks
			if self.view.checkBox_1_s.isChecked()==True:
				"""1. Checks"""
				self.p=34.41
				self.I=self.func.mom2I(self.Cmagnets,'DIP01',self.p)
				self.Cmagnets.setSI('DIP01',self.I)
			"""2. Set Disperaion"""
			if self.view.checkBox_2_s.isChecked()==True:
				#2.1 Minimize Beta
				self.func.minimizeBeta(self.Cmagnets,'S02-QUAD3',
										None,'VM-CLA-C2V-DIA-CAM-01',1)
				self.func.minimizeBeta(self.Cmagnets,'S02-QUAD4',
										None,'VM-CLA-C2V-DIA-CAM-01',-1)
				#2.2 Set Dispersion Size on Spec Line
				self.Cmagnets.setSI('DIP01',self.I)
				self.fixDispersion('QUAD0','VM-EBT-INJ-DIA-CAM-05:CAM',-0.05)
				#ONLY in REAL LIFE
				#self.func.magnets.degauss('DIP01')

			"""3. Calculate Dispersion """
			if self.view.checkBox_3_s.isChecked()==True:
				self.Dispersion,beamSigma,
				self.dCurrents,self.dPositions,
				self.fCurrents,
				self.fPositions = self.func.findDispersion(self.Cmagnets,
														'DIP01',
														None,
														'VM-CLA-C2V-DIA-CAM-01',
														self.I,5,0.1)
				self.Is = beamSigma/self.Dispersion
				print(self.Is)
				#Haven't done errors yet

			"""4. Calculate Momenum Spread """
			if self.view.checkBox_4_s.isChecked()==True:
				self.pSpread = self.func.calcMomSpread(self.Cmagnets,'DIP01',self.Is,self.I)
		else:
			print 'Not confirmed momentum measurement'
