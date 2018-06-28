import sys,os
import random as r
import numpy as np
import inspect

class Machine(object):

	def __init__(self, machineType, lineType, gunType):
		super(Machine, self).__init__()
		self.machineType = machineType
		if self.machineType == 'Virtual':
			self.virtualSetUp()
		self.lineType = lineType
		self.gunType = gunType
		self.setUpCtrls()

	def setUpCtrls(self):
		if self.machineType == 'None':
			print 'No controllers!'
			self.magnets = None
			self.scope = None
			self.bpms = None
			self.gunllrf = None
			self.linac1llrf = None
			self.cameras = None
		else:
			'''This is the place to get contollers'''
			sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\Release')
			os.environ["PATH"] = os.environ["PATH"]+";\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release\\root_v5.34.34\\bin\\"
			import VELA_CLARA_Magnet_Control as mag
			import VELA_CLARA_BPM_Control as bpm
			import VELA_CLARA_LLRF_Control as llrf
			import VELA_CLARA_Charge_Control as scope
			# import VELA_CLARA_Camera_IA_Control as camIA

			self.magInit = mag.init()
			self.magInit.setQuiet()
			self.bpmInit = bpm.init()
			self.bpmInit.setQuiet()
			self.llrfInit = llrf.init()
			self.llrfInit.setQuiet()
			self.scopeInit = scope.init()
			self.scopeInit.setQuiet()
			# self.camInit = camIA.init()
			# self.camInit.setQuiet()
			if self.machineType == 'Virtual':
				os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
				os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12"
				os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
				os.environ["EPICS_CA_SERVER_PORT"]="6000"
				sys.path.append('C:\\anaconda32\\Work\\OnlineModel')
				if self.lineType == 'VELA':
					self.magnets = self.magInit.virtual_VELA_INJ_Magnet_Controller()
					self.scope = self.scopeInit.virtual_VELA_INJ_Charge_Controller()
					self.bpms = self.bpmInit.virtual_VELA_INJ_BPM_Controller()
					self.gunllrf = self.llrfInit.virtual_VELA_LRRG_LLRF_Controller()
					self.linac1llrf = None
					self.cameras = None
				else:
					self.magnets = self.magInit.virtual_CLARA_PH1_Magnet_Controller()
					self.scope = self.scopeInit.virtual_CLARA_PH1_Charge_Controller()
					self.bpms = self.bpmInit.virtual_CLARA_PH1_BPM_Controller()
					self.gunllrf = self.llrfInit.virtual_CLARA_LRRG_LLRF_Controller()
					self.linac1llrf = self.llrfInit.virtual_L01_LLRF_Controller()
					self.cameras = None
			elif self.machineType == 'Physical':
				print 'PHYSICAL CONTROLLERS!'
				if self.lineType == 'VELA':
					self.magnets = self.magInit.physical_VELA_INJ_Magnet_Controller()
					self.scope = self.scopeInit.physical_VELA_INJ_Charge_Controller()
					self.bpms = self.bpmInit.physical_VELA_INJ_BPM_Controller()
					self.gunllrf = self.llrfInit.physical_VELA_LRRG_LLRF_Controller()
					self.linac1llrf = None
					self.cameras = None
				else:
					self.magnets = self.magInit.physical_CLARA_PH1_Magnet_Controller()
					self.scope = self.scopeInit.physical_CLARA_PH1_Charge_Controller()
					self.bpms = self.bpmInit.physical_CLARA_PH1_BPM_Controller()
					self.gunllrf = self.llrfInit.physical_CLARA_LRRG_LLRF_Controller()
					self.linac1llrf = self.llrfInit.physical_L01_LLRF_Controller()
					self.cameras = None

	def virtualSetUp(self):
		sys.path.append('C:\\anaconda32\\Work\\OnlineModel')
		import SAMPL.v2_developing.sampl as sampl
		self.magnets.switchONpsu('DIP01')
		self.cameras.setCamera('C2V-CAM-01')
		self.selectedCamera = self.cameras.getSelectedIARef()
		self.magnets.setSI('DIP01',-91.6)
		self.gunllrf.setAmpMVM(100)
		self.gunllrf.setPhiDEG(0)
		self.linac1llrf.setAmpMVM(0)
		self.linac1llrf.setPhiDEG(-9)
		self.SAMPL = sampl.Setup(V_MAG_Ctrl=None,
		                    C_S01_MAG_Ctrl=self.magnets,
		                    C_S02_MAG_Ctrl=self.magnets,
		                    C2V_MAG_Ctrl=self.magnets,
		                    LRRG_RF_Ctrl=None,
		                    HRRG_RF_Ctrl=self.gunllrf,
		                    L01_RF_Ctrl=self.linac1llrf,
		                    messages=True)

		self.SAMPL.startElement = 'CLA-HRG1-GUN-CAV'
		self.SAMPL.stopElement = 'CLA-C2V-DIA-SCR-01-W'
		self.SAMPL.initDistribFile = '4k-250pC.ini'

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

	def setGunPhase(self, phase):
		if self.machineType == 'None':
			self.gunPhiSp = phase
		else:
			self.gunllrf.setPhiSP(np.mod(180+phase,360)-180)

	def getGunPhase(self):
		if self.machineType == 'None':
			return self.gunPhiSp if hasattr(self, 'gunPhiSp') else 0
		else:
			return self.gunllrf.getPhiSP()

	def setGunAmplitude(self, amp):
		if self.machineType == 'None':
			self.gunAmpSp = amp
		else:
			self.gunllrf.setAmpSP(amp)

	def getGunAmplitude(self):
		if self.machineType == 'None':
			return self.gunAmpSp if hasattr(self, 'gunAmpSp') else 0
		else:
			return self.gunllrf.getAmpSP()

	def getGunKlystronForwardPower(self):
		return self.gunllrf.getKlyFwdPower()

	def getLinac1KlystronForwardPower(self):
		return self.linac1llrf.getKlyFwdPower()

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

	def getBPMPosition(self, bpm):
		if self.machineType == 'None':
			value = np.random.random_sample()
			return value
		else:
			# print 'BPM ', bpm, ' = ', self.bpm.getXFromPV(bpm)
			return self.bpms.getXFromPV(bpm)

	def getWCMCharge(self, scope):
		if self.machineType == 'None':
			value = 50*np.random.random_sample()
			return value
		else:
			return self.scope.getCharge(scope)

	def setDip(self, I):
		# print 'setting dip01 = ', I
		if self.machineType == 'None':
			self.dipoleSI = I
		elif self.machineType == 'Virtual':
			self.magnets.setSI('DIP01', -1*I)
		elif self.machineType == 'Physical':
			self.magnets.setSI('DIP01', I)

	def getDip(self):
		if self.machineType == 'None':
			return self.dipoleSI if hasattr(self, 'dipoleSI') else 0
		else:
			return self.magnets.getSI('DIP01')

	def degaussDIP(self):
		self.magnets.degauss(['DIP01'], True)

	def isDIPDegaussing(self):
		return self.magnets.isDegaussing('DIP01')
