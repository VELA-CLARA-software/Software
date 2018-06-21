import sys,os
import random as r
import numpy as np
import inspect
import time

class Machine(object):

	def __init__(self, machineType, lineType, gunType):
		super(Machine, self).__init__()
		self.machineType = machineType
		if self.machineType == 'Virtual':
			self.virtualSetUp()
		self.lineType = lineType
		self.gunType = gunType
		self.setUpCtrls()
		self.corrSI = {}
		self.solSI = {}

	def setUpCtrls(self):
		if self.machineType == 'None':
			print 'No controllers!'
			self.magnets = None
			self.bpms = None
			self.linac1llrf = None
		else:
			'''This is the place to get contollers'''
			sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\Release')
			os.environ["PATH"] = os.environ["PATH"]+";\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release\\root_v5.34.34\\bin\\"
			import VELA_CLARA_Magnet_Control as mag
			import VELA_CLARA_BPM_Control as bpm
			import VELA_CLARA_LLRF_Control as llrf

			self.magInit = mag.init()
			self.magInit.setQuiet()
			self.bpmInit = bpm.init()
			self.bpmInit.setQuiet()
			self.llrfInit = llrf.init()
			self.llrfInit.setQuiet()
			print 'PHYSICAL CONTROLLERS!'
			self.magnets = self.magInit.physical_CLARA_PH1_Magnet_Controller()
			self.bpms = self.bpmInit.physical_CLARA_PH1_BPM_Controller()
			self.linac1llrf = self.llrfInit.physical_L01_LLRF_Controller()

	def setAmplitude(self, cavity, value):
		print cavity, value
		if cavity == 'Gun':
			self.setGunAmplitude(value)
		elif cavity == 'Linac1':
			self.setLinac1Amplitude(value)

	def getAmplitude(self, cavity):
		if cavity == 'Gun':
			return self.getGunAmplitude()
		elif cavity == 'Linac1':
			return self.getLinac1Amplitude()

	def setPhase(self, cavity, value):
		# print 'caller name:', inspect.stack(),'\n\n'
		if cavity == 'Gun':
			self.setGunPhase(value)
		elif cavity == 'Linac1':
			self.setLinac1Phase(value)

	def getPhase(self, cavity):
		if cavity == 'Gun':
			return self.getGunPhase()
		elif cavity == 'Linac1':
			return self.getLinac1Phase()

	def getKlystronForwardPower(self, cavity):
		if cavity == 'Gun':
			return self.getGunKlystronForwardPower()
		elif cavity == 'Linac1':
			return self.getLinac1KlystronForwardPower()

	def setLinac1Phase(self, phase):
		if self.machineType == 'None':
			self.linac1PhiSp = phase
		else:
			print 'setting L01 phase = ', np.mod(180+phase,360)-180
			self.linac1llrf.setPhiSP(np.mod(180+phase,360)-180)

	def getLinac1Phase(self):
		if self.machineType == 'None':
			return self.linac1PhiSp if hasattr(self, 'linac1PhiSp') else 0
		else:
			return self.linac1llrf.getPhiSP()

	def setLinac1Amplitude(self, amp):
		if self.machineType == 'None':
			self.linac1AmpSp = amp
		else:
			self.linac1llrf.setAmpFF(amp)

	def getLinac1Amplitude(self):
		if self.machineType == 'None':
			return self.linac1AmpSp if hasattr(self, 'linac1AmpSp') else 0
		else:
			return self.linac1llrf.getAmpSP()

	def getBPMPosition(self, bpm, plane='X'):
		if self.machineType == 'None':
			value = np.random.random_sample()
			return value
		else:
			if plane == 'Y':
				return self.bpms.getYFromPV(bpm)
			else:
				return self.bpms.getXFromPV(bpm)

	def setCorr(self, corr, I, tol=0.05):
		# print 'setting dip01 = ', I
		if self.machineType == 'None':
			self.corrSI[corr] = I
		elif self.machineType == 'Physical':
			self.magnets.setSI(corr, I)

	def getCorr(self, corr):
		if self.machineType == 'None':
			return self.corrSI[corr] if hasattr(self, 'corrSI') and corr in self.corrSI else 0
		else:
			return self.magnets.getRI(corr)

	def setSol(self, sol, I, tol=0.2):
		# print 'setting dip01 = ', I
		if self.machineType == 'None':
			self.solSI[sol] = I
		elif self.machineType == 'Physical':
			self.magnets.setSI(sol, I)

	def getSol(self, sol):
		if self.machineType == 'None':
			return self.solSI[sol] if hasattr(self, 'solSI') and sol in self.solSI else 0
		else:
			return self.magnets.getRI(sol)
