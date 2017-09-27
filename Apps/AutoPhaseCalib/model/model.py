from PyQt4.QtCore import QThread
import sys,os
import time
import scipy.constants as physics
import numpy as np
from scipy.optimize import curve_fit
import random as r
os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12" #BE SPECIFIC.... YOUR I.P. FOR YOUR VM
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
os.environ["EPICS_CA_SERVER_PORT"]="6000"

sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\stagetim')
sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\OnlineModel')

import onlineModel

import VELA_CLARA_MagnetControl as mag
import VELA_CLARA_BPM_Control as bpm
import VELA_CLARA_LLRFControl as llrf
import VELA_CLARA_Scope_Control as scope

class Model(QThread):
	def __init__(self,view,machineType,lineType,gunType):
		QThread.__init__(self)
		self.view = view
		self.magInit = mag.init()
		self.bpmInit = bpm.init()
		self.llrfInit = llrf.init()
		self.scopeInit = scope.init()
		self.machineType = machineType
		self.lineType = lineType
		self.gunType = gunType
		self.view.label_MODE.setText('MODE: '+self.machineType+' '+self.lineType+' with '+self.gunType+' Hz gun')
		self.setUpCtrls()
		#self.beamlines = {"VELA":  mag.MACHINE_AREA.VELA_INJ, "CLARA": [mag.MACHINE_AREA.CLARA_INJ,mag.MACHINE_AREA.CLARA_S01,mag.MACHINE_AREA.CLARA_S02,mag.MACHINE_AREA.CLARA_2_VELA]}
		#self.modes = {"Physical": mag.MACHINE_MODE.PHYSICAL, "Virtual": mag.MACHINE_MODE.VIRTUAL}
		self.approxPhaseData=[]
		self.approxChargeData=[]
		self.approxPhaseFit=[]
		self.approxChargeFit=[]
		self.finePhaseFit=[]
		self.fineBPMFit=[]
		self.finePhaseData=[]
		self.fineBPMData=[]

		print("Model Initialized")
	#DESTRUCTOR
	def __del__(self):
		self.wait()
	def run(self):
		if self.lineType=='VELA':
			self.velaMethod()
		elif self.lineType=='CLARA':
			self.claraMethod()

	def setUpCtrls(self):
		if self.lineType=='VELA'and self.machineType=='Physical':
			self.magnets = self.magInit.physical_VELA_INJ_Magnet_Controller()
			self.scope = self.scopeInit.physical_VELA_INJ_Scope_Controller()
			self.bpms = self.bpmInit.physical_VELA_INJ_BPM_Controller()
			self.gun = self.llrfInit.physical_VELA_LRRG_LLRF_Controller()
		elif self.lineType=='CLARA'and self.machineType=='Physical':
			self.magnets = self.magInit.physical_CLARA_INJ_Magnet_Controller()
			self.scope = self.scopeInit.physical_CLARA_INJ_Scope_Controller()
			self.bpms = self.bpmInit.physical_CLARA_INJ_BPM_Controller()
			self.gun = self.llrfInit.physical_CLARA_LRRG_LLRF_Controller()
		elif self.lineType=='VELA'and self.machineType=='Virtual':
			self.magnets = self.magInit.virtual_VELA_INJ_Magnet_Controller()
			self.scope = self.scopeInit.virtual_VELA_INJ_Scope_Controller()
			self.bpms = self.bpmInit.virtual_VELA_INJ_BPM_Controller()
			self.gun = self.llrfInit.virtual_VELA_LRRG_LLRF_Controller()
		elif self.lineType=='CLARA'and self.machineType=='Virtual':
			self.magnets = self.magInit.virtual_CLARA_INJ_Magnet_Controller()
			self.scope = self.scopeInit.virtual_CLARA_INJ_Scope_Controller()
			self.bpms = self.bpmInit.virtual_CLARA_INJ_BPM_Controller()
			self.gun = self.llrfInit.virtual_CLARA_LRRG_LLRF_Controller()
		self.ASTRA = onlineModel.ASTRA(V_MAG_Ctrl=self.magnets, V_RF_Ctrl=self.gun,messages=False)

	def claraMethod(self):
		print('clara Method')
		self.method(magnets=[],bpm='',scope='')

	def velaMethod(self):
		print('vela Method')
		self.method(magnets=['QUAD01', 'QUAD02', 'QUAD03', 'QUAD04', 'QUAD05', 'QUAD06',
							'HCOR03', 'HCOR04', 'HCOR05', 'VCOR03', 'VCOR04', 'VCOR05',
							'SOL', 'BSOL', 'DIP01'], bpm='BPM03', scope='SCOP01')

	def method(self,magnets=None,bpm=None,scope=None):
		print('generic method')
		'''1. Setup Magnets'''
		if self.view.checkBox_1.isChecked()==True:
			print('1. Setting up Magnets')
			self.setUpMagnets(magnets)

		'''2. Approximately Find Crest with WCM'''
		if self.view.checkBox_2.isChecked()==True:
			print('2. Approximately Finding Crest')

		'''3. Find Crest using BPM'''
		if self.view.checkBox_3.isChecked()==True:
			print('3. Finding Crest')
			self.findingCrest(magnets,bpm,int(self.view.lineEdit_4.text()),int(self.view.lineEdit_5.text()))

		'''4. Convert Current to Momentum'''
		if self.view.checkBox_4.isChecked()==True:
			print('4. Set Momentum of Beam')
			self.setUpGun(int(self.view.lineEdit.text()),bpm)
	def setUpMagnets(self,magnets):
		deguassingList=[]
		print('Deguassing magnets...')
		for magnet in magnets:
			if self.view.checkBox_deguassQ.isChecked() and self.magnets.isAQuad(magnet):
				deguassingList.append(magnet)
			elif self.view.checkBox_deguassC.isChecked() and self.magnets.isACor(magnet):
				deguassingList.append(magnet)
			elif self.view.checkBox_deguassS.isChecked() and self.magnets.isASol(magnet):
				deguassingList.append(magnet)
			elif self.view.checkBox_deguassD.isChecked() and self.magnets.isADip(magnet):
				deguassingList.append(magnet)
			#else:
			#	print('Magnet '+magnet+' is off or not selected to be deguassed.')
		print('Magnet to be Deguassed: '+str(deguassingList))
		self.activeMags = mag.std_vector_string()
		self.activeMags.extend(deguassingList)
		self.magnets.degauss(self.activeMags,True)

		print('Switching off magnets...')
		switchOfFList=[]
		for magnet in magnets:
			if self.view.checkBox_quadOff.isChecked() and self.magnets.isAQuad(magnet):
				switchOfFList.append(magnet)
			elif self.view.checkBox_corrOff.isChecked() and self.magnets.isACor(magnet):
				switchOfFList.append(magnet)
			#else:
				#print('No magnets to be switched off.')
		print('Magnet to be Switched Off: '+str(switchOfFList))
		self.turnOffMags = mag.std_vector_string()
		self.turnOffMags.extend(switchOfFList)
		self.magnets.switchOFFpsu(self.turnOffMags)

		print('Setting Dipole for predicted momentum...')
		for magnet in magnets:
			if self.magnets.isADip(magnet):
				dipole=magnet
		D = self.magnets.getMagObjConstRef(dipole)
		coeffs = list(D.fieldIntegralCoefficients)
		mom = float(self.view.lineEdit_2.text())
		coeffs[-1] -= (1000000000*(mom*physics.pi*45)/(physics.c*180))
		roots = np.roots(coeffs)
		current = roots[-1].real
		while(self.magnets.isDegaussing(dipole)):
			print('Waiting for '+dipole+' to degauss...')
			time.sleep(10)
		self.magnets.setSI(dipole,-current)

	def findingCrest(self, magnets,bpm,phiRange,phiSteps):
		self.finePhaseFit=[]
		self.fineBPMFit=[]
		self.finePhaseData=[]
		self.fineBPMData=[]

		self.gun.setAmp(62.3)
		self.approxcrest=0
		for phase in np.linspace(self.approxcrest-phiRange/2, self.approxcrest+phiRange/2, phiSteps):
			self.gun.setPhi(phase)

			currphase = self.gun.getPhi()
			time.sleep(0)
			#while abs(phase - currphase) > abs(0.01*phase):
			#	currphase = self.gun.getPhi()
				#print(currphase)
			print 'set phase to',phase
			print 'phase got to', currphase
			self.ASTRA.go('V1-GUN','SP-YAG04','temp-start.ini')
			while self.ASTRA.isRunning()==True:
				time.sleep(1)
			data =1000*self.bpms.getXFromPV(bpm)
			print data
			self.fineBPMData.append(data)
			self.finePhaseData.append(currphase)
			#time.sleep(5)
		def func(list, a, b, c):
			x = np.array(list)
			return a*x**2 + b*x + c
		popt, pcov = curve_fit(func, self.finePhaseData, self.fineBPMData, p0=None)
		self.finePhaseFit = np.linspace(self.approxcrest-phiRange/2, self.approxcrest+phiRange/2, 200)
		self.fineBPMFit = func(self.finePhaseFit, *popt)

		self.calibrationPhase=-popt[1]/(2*popt[1])
		print 'calibration phase is', self.calibrationPhase

	def setUpGun(self,desiredPhase,bpm):
		self.calibrationPhase=-0.5
		self.gun.setPhi(desiredPhase+self.calibrationPhase)
		x=1000*self.bpms.getXFromPV(bpm)
		currentAmp=self.gun.getAmp()
		step=1 #(MV/m)
		time.sleep(1)
		print x
		while abs(x)>0.01:

			self.gun.setAmp(currentAmp+step)
			time.sleep(1)
			x_old=x
			self.ASTRA.go('V1-GUN','SP-YAG04','temp-start.ini')
			while self.ASTRA.isRunning()==True:
				time.sleep(1)
			x=1000*self.bpms.getXFromPV(bpm)
			print x
			if x>0:
				step=-abs(step)
			elif x<0:
				step=abs(step)
			if abs(x-x_old)>abs(x):
				step=0.5*step
