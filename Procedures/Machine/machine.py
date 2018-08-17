import sys,os
import random as r
import numpy as np
import inspect

class Machine(object):

	def __init__(self, machineType, lineType, gunType, controllers=['magnets', 'bpms', 'gunllrf', 'linac1llrf', 'charge', 'cameras']):
		super(Machine, self).__init__()
		self.machineType = machineType
		self.lineType = lineType
		self.gunType = gunType
		self.controllers = controllers
		self.setUpCtrls()
		if self.machineType == 'Virtual':
			self.virtualSetUp()
		self.corrSI = {}
		self.solSI = {}
		self.quadSI = {}
		self.parameters={}

	def initilise_parameters(self):
		if self.lineType=='VELA':
			self.velaMethod()
		elif self.lineType=='CLARA':
			self.claraMethod()
		return self.parameters

	def claraMethod(self):
		print('clara Method')
		self.parameters['magnets']=['S02-QUAD01', 'S02-QUAD02', 'S02-QUAD03', 'S02-QUAD04',
							'S01-HCOR1', 'S01-VCOR1', 'S01-HCOR2', 'S01-VCOR2',
							'S02-HCOR1', 'S02-VCOR1', 'S02-HCOR2', 'S02-VCOR2',
							'LRG-SOL', 'LRG-BSOL', 'DIP01']
		self.parameters['gun_dispersive_bpm'] = 'C2V-BPM01'
		self.parameters['linac_dispersive_bpm'] = {1: 'C2V-BPM01'}
		self.parameters['linac_rough_bpm'] = {1: 'S02-BPM01'}
		self.parameters['scope'] = 'WCM'

	def velaMethod(self):
		print('vela Method')
		self.parameters['magnets']=['QUAD01', 'QUAD02', 'QUAD03', 'QUAD04', 'QUAD05', 'QUAD06',
							'HCOR03', 'HCOR04', 'HCOR05', 'VCOR03', 'VCOR04', 'VCOR05',
							'SOL', 'BSOL', 'DIP01']
		self.parameters['bpm'] = 'C2V-BPM01'
		self.parameters['scope'] = 'WCM'

	def setUpCtrls(self):
		if self.machineType == 'None':
			print 'No controllers!'
			'''This is the place to get contollers'''
			sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\Release')
			os.environ["PATH"] = os.environ["PATH"]+";\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release\\root_v5.34.34\\bin\\"
			import VELA_CLARA_Magnet_Control as mag
			os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
			os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12"
			os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
			os.environ["EPICS_CA_SERVER_PORT"]="6000"
			# self.magInit = mag.init()
			# self.magInit.setQuiet()
			self.magnets = None
			self.bpms = None
			self.gunllrf = None
			self.linac1llrf = None
			self.cameras = None
			self.screens = None
		else:
			'''This is the place to get contollers'''
			sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\Release')
			os.environ["PATH"] = os.environ["PATH"]+";\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release\\root_v5.34.34\\bin\\"
			if 'magnets' in self.controllers:
				import VELA_CLARA_Magnet_Control as mag
				self.magInit = mag.init()
				self.magInit.setQuiet()
			if 'bpms' in self.controllers:
				import VELA_CLARA_BPM_Control as bpm
				self.bpmInit = bpm.init()
				self.bpmInit.setQuiet()
			if 'gunllrf' in self.controllers or 'linac1llrf' in self.controllers:
				import VELA_CLARA_LLRF_Control as llrf
				self.llrfInit = llrf.init()
				self.llrfInit.setQuiet()
			if 'charge' in self.controllers:
				import VELA_CLARA_Charge_Control as scope
				self.scopeInit = scope.init()
				self.scopeInit.setQuiet()
			if 'cameras' in self.controllers:
				import VELA_CLARA_Camera_Control as camIA
				self.camInit = camIA.init()
				self.camInit.setQuiet()
			if 'screens' in self.controllers:
				import VELA_CLARA_Screen_Control as screenIA
				self.screenInit = screenIA.init()
				self.screenInit.setQuiet()
			if self.machineType == 'Virtual':
				os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
				os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12"
				os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
				os.environ["EPICS_CA_SERVER_PORT"]="6000"
				sys.path.append('C:\\anaconda32\\Work\\OnlineModel')
				if self.lineType == 'VELA':
					if 'magnets' in self.controllers:
						self.magnets = self.magInit.virtual_VELA_INJ_Magnet_Controller()
					if 'charge' in self.controllers:
						self.scope = self.scopeInit.virtual_VELA_INJ_Charge_Controller()
					if 'bpms' in self.controllers:
						self.bpms = self.bpmInit.virtual_VELA_INJ_BPM_Controller()
					if 'gunllrf' in self.controllers:
						self.gunllrf = self.llrfInit.virtual_VELA_LRRG_LLRF_Controller()
					self.linac1llrf = None
					if 'cameras' in self.controllers:
						self.cameras = self.camInit.virtual_VELA_Camera_Controller()
					if 'screens' in self.controllers:
						self.screens = self.screenInit.virtual_VELA_INJ_Screen_Controller()
				else:
					if 'magnets' in self.controllers:
						self.magnets = self.magInit.virtual_CLARA_PH1_Magnet_Controller()
					if 'charge' in self.controllers:
						self.scope = self.scopeInit.virtual_CLARA_PH1_Charge_Controller()
					if 'bpms' in self.controllers:
						self.bpms = self.bpmInit.virtual_CLARA_PH1_BPM_Controller()
					if 'gunllrf' in self.controllers:
						self.gunllrf = self.llrfInit.virtual_CLARA_LRRG_LLRF_Controller()
					if 'linac1llrf' in self.controllers:
						self.linac1llrf = self.llrfInit.virtual_L01_LLRF_Controller()
					if 'cameras' in self.controllers:
						self.cameras = self.camInit.virtual_CLARA_Camera_Controller()
					if 'screens' in self.controllers:
						self.screens = self.screenInit.virtual_CLARA_PH1_Screen_Controller()
			elif self.machineType == 'Physical':
				print 'PHYSICAL CONTROLLERS!'
				if self.lineType == 'VELA':
					if 'magnets' in self.controllers:
						self.magnets = self.magInit.physical_VELA_INJ_Magnet_Controller()
					if 'charge' in self.controllers:
						self.scope = self.scopeInit.physical_VELA_INJ_Charge_Controller()
					if 'bpms' in self.controllers:
						self.bpms = self.bpmInit.physical_VELA_INJ_BPM_Controller()
					if 'gunllrf' in self.controllers:
						self.gunllrf = self.llrfInit.physical_VELA_LRRG_LLRF_Controller()
					self.linac1llrf = None
					if 'cameras' in self.controllers:
						self.cameras = self.camInit.physical_VELA_Camera_Controller()
					if 'screens' in self.controllers:
						self.screens = self.screenInit.physical_VELA_INJ_Screen_Controller()
				else:
					if 'magnets' in self.controllers:
						self.magnets = self.magInit.physical_CLARA_PH1_Magnet_Controller()
					if 'charge' in self.controllers:
						self.scope = self.scopeInit.physical_CLARA_PH1_Charge_Controller()
					if 'bpms' in self.controllers:
						self.bpms = self.bpmInit.physical_CLARA_PH1_BPM_Controller()
					if 'gunllrf' in self.controllers:
						self.gunllrf = self.llrfInit.physical_CLARA_LRRG_LLRF_Controller()
					if 'linac1llrf' in self.controllers:
						self.linac1llrf = self.llrfInit.physical_L01_LLRF_Controller()
					if 'cameras' in self.controllers:
						self.cameras = self.camInit.physical_CLARA_Camera_Controller()
					if 'screens' in self.controllers:
						self.screens = self.screenInit.physical_CLARA_PH1_Screen_Controller()

	def virtualSetUp(self):
		pass
		# sys.path.append('C:\\anaconda32\\Work\\OnlineModel')
		# import SAMPL.v2_developing.sampl as sampl
		# self.magnets.switchONpsu('DIP01')
		# self.gunllrf.setAmpMVM(100)
		# self.gunllrf.setPhiDEG(0)
		# self.linac1llrf.setAmpMVM(0)
		# self.linac1llrf.setPhiDEG(-9)
		# self.SAMPL = sampl.Setup(V_MAG_Ctrl=None,
		#                     C_S01_MAG_Ctrl=self.magnets,
		#                     C_S02_MAG_Ctrl=self.magnets,
		#                     C2V_MAG_Ctrl=self.magnets,
		#                     LRRG_RF_Ctrl=None,
		#                     HRRG_RF_Ctrl=self.gunllrf,
		#                     L01_RF_Ctrl=self.linac1llrf,
		#                     messages=True)
		#
		# self.SAMPL.startElement = 'CLA-HRG1-GUN-CAV'
		# self.SAMPL.stopElement = 'CLA-C2V-DIA-SCR-01-W'
		# self.SAMPL.initDistribFile = '4k-250pC.ini'

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
			# print 'setting L01 LLRF to ', amp
			self.linac1llrf.setAmpFF(amp)

	def getLinac1Amplitude(self):
		if self.machineType == 'None':
			return self.linac1AmpSp if hasattr(self, 'linac1AmpSp') else 0
		else:
			return self.linac1llrf.getAmpSP()

	def getBPMPosition(self, bpm, plane='X'):
		if self.machineType == 'None':
			value = 20*np.random.random_sample() - 10
			return value
		else:
			if plane == 'Y':
				return self.bpms.getYFromPV(bpm)
			else:
				return self.bpms.getXFromPV(bpm)

	def getScreenPosition(self, screen, plane='X'):
		if self.machineType == 'None':
			value = 20*np.random.random_sample() - 10
			return value
		else:
			# cam_control.startAcquiring(name)
			if plane == 'Y':
				yval = self.cameras.getY()
				print 'yval = ', yval
				return yval
			else:
				xval = self.cameras.getX()
				print 'xval = ', xval
				return xval

	def setCorr(self, corr, I, tol=0.05):
		# print 'setting dip01 = ', I
		if self.machineType == 'None':
			self.corrSI[corr] = I
		else:
			print 'setting ', corr, ' = ', I
			print self.magnets.setSI(corr, I)

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

	def setDegaussMagnet(self, name, degaussToZero=True):
		if not self.machineType == 'None':
			if isinstance(name, (list, tuple)):
				self.magnets.degauss(name, degaussToZero)
			else:
				self.magnets.degauss([name], degaussToZero)

	def isMagnetDegaussing(self, name):
		if not self.machineType == 'None':
			if isinstance(name, (list, tuple)):
				return all([self.magnets.isDegaussing(m) for m in name])
			else:
				return self.magnets.isDegaussing(name)
		else:
			return False

	def setDegaussDIP(self):
		self.setDegaussMagnet('DIP01')

	def isDIPDegaussing(self):
		return self.isMagnetDegaussing('DIP01')

	def setQuad(self, name, I):
		if self.machineType == 'None':
			self.quadSI[name] = I
		elif self.machineType == 'Virtual':
			self.magnets.setSI(name, I)
		elif self.machineType == 'Physical':
			self.magnets.setSI(name, I)

	def getQuad(self, name):
		if self.machineType == 'None':
			return self.quadSI[name] if hasattr(self, 'quadSI') and name in self.quadSI else 0
		else:
			return self.magnets.getSI(name)