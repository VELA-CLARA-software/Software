# from PyQt4.QtCore import QThread, QObject, pyqtSignal, QTimer
import sys,os
import time
import scipy.constants as physics
import numpy as np
from scipy.optimize import curve_fit
from scipy.interpolate import UnivariateSpline
import random as r
from functools import partial

degree = physics.pi/180.0

class dataArray(dict):

	def __init__(self):
		super(dataArray, self).__init__()

	def checkDataArray(self, cavity, actuator, type):
		cavity = str(cavity)
		actuator = str(actuator)
		type = str(type)
		if not cavity in self:
			self[cavity] = {}
		if not actuator in self[cavity]:
			self[cavity][actuator] = {}
		if not type in self[cavity][actuator]:
			self[cavity][actuator][type] = []

	def resetData(self, cavity, actuator, type):
		cavity = str(cavity)
		actuator = str(actuator)
		for t in type:
			self.checkDataArray(cavity, actuator, t)
			self[cavity][actuator][t] = []

	def setData(self, cavity, actuator, type, data):
		cavity = str(cavity)
		actuator = str(actuator)
		for t, d in zip(type, data):
			t = str(t)
			self.checkDataArray(cavity, actuator, t)
			self[cavity][actuator][t] = d

	def appendData(self, cavity, actuator, type, data):
		cavity = str(cavity)
		actuator = str(actuator)
		for t, d in zip(type, data):
			t = str(t)
			self.checkDataArray(cavity, actuator, t)
			self[cavity][actuator][t].append(d)

class emitter(object):

	def __init__(self, signal=None):
		super(emitter, self).__init__()
		self.signal = signal

	def emit(self, *args, **kwargs):
		if self.signal is not None:
			self.signal.emit(*args, **kwargs)

class Model(object):

	magnets = None
	scope = None
	bpms = None
	gunllrf = None
	linac1llrf = None
	cameras = None
	sleepTime = 0.0001
	sleepTimeDipole = 0.0001

	def __init__(self, machineType, lineType, gunType):
		super(Model, self).__init__()
		self.machineType = machineType
		if self.machineType == 'Virtual':
			self.virtualSetUp()
		self.lineType = lineType
		self.gunType = gunType
		self.newData = emitter()
		self.logger = emitter()
		self.setUpCtrls()
		self.crestingData = dataArray()
		self.parameters={}
		self.data = []
		self.calibrationPhase = {'Gun': None, 'Linac1': None}
		self.run()
		print("Model Initialized")

	def setRunning(self):
		self.running = True

	def setNotRunning(self):
		self.running = False

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
			self.sleepTime = 0.1
			self.sleepTimeDipole = 0.25
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

	def runSAMPLE(self):
		if self.machineType == 'Virtual':
			self.SAMPL.run()

	def run(self):
		if self.lineType=='VELA':
			self.velaMethod()
		elif self.lineType=='CLARA':
			self.claraMethod()

	def claraMethod(self):
		print('clara Method')
		self.parameters['magnets']=['S02-QUAD01', 'S02-QUAD02', 'S02-QUAD03', 'S02-QUAD04',
							'S01-HCOR1', 'S01-VCOR1', 'S01-HCOR2', 'S01-VCOR2',
							'S02-HCOR1', 'S02-VCOR1', 'S02-HCOR2', 'S02-VCOR2',
							'LRG-SOL', 'LRG-BSOL', 'DIP01']
		self.parameters['dispersive_bpm'] = 'C2V-BPM01'
		self.parameters['linac_rough_bpm'] = 'S02-BPM01'
		self.parameters['scope'] = 'WCM'

	def velaMethod(self):
		print('vela Method')
		self.parameters['magnets']=['QUAD01', 'QUAD02', 'QUAD03', 'QUAD04', 'QUAD05', 'QUAD06',
							'HCOR03', 'HCOR04', 'HCOR05', 'VCOR03', 'VCOR04', 'VCOR05',
							'SOL', 'BSOL', 'DIP01']
		self.parameters['bpm'] = 'C2V-BPM01'
		self.parameters['scope'] = 'WCM'

	def magnetDegausser(self):
		print('1. Setting up Magnets')
		self.setUpMagnets(self.parameters['magnets'])

	def gunWCMCrester(self, gunPhaseSet=0):
		self.cavity = 'Gun'
		self.actuator = 'approx'
		self.stepSize = 5
		self.nSamples = 3
		self.getDataFunction = partial(self.getWCMCharge, self.parameters['scope'])
		self.findingCrestGunQuick()

	def linac1CresterQuick(self, linac1PhaseSet=0):
		self.cavity = 'Linac1'
		self.actuator = 'approx'
		self.stepSize = 5
		self.nSamples = 3
		self.getDataFunction = partial(self.getBPMPosition, self.parameters['linac_rough_bpm'])
		self.findingCrestLinac1Quick()

	def gunCresterFine(self, phiRange, phiSteps, nSamples):
		self.cavity = 'Gun'
		self.actuator = 'fine'
		self.stepSize = 5
		self.nSamples = nSamples
		self.phiRange = phiRange
		self.phiSteps = phiSteps
		self.getDataFunction = partial(self.getBPMPosition, self.parameters['dispersive_bpm'])
		self.findingCrestFine()

	def linac1CresterFine(self, phiRange, phiSteps, nSamples):
		self.cavity = 'Linac1'
		self.actuator = 'fine'
		self.stepSize = 5
		self.nSamples = nSamples
		self.phiRange = phiRange
		self.phiSteps = phiSteps
		self.getDataFunction = partial(self.getBPMPosition, self.parameters['dispersive_bpm'])
		self.findingCrestFine()

	def gunDipoleSet(self):
		self.cavity = 'Gun'
		self.actuator = 'dipole'
		self.nSamples = 3
		self.start = 5
		self.stop = 10
		self.step = 0.1
		self.initialGuess = [0, 10, 0.3, 9]
		self.getDataFunction = partial(self.getBPMPosition, self.parameters['dispersive_bpm'])
		self.findDipoleCurrent()

	def linac1DipoleSet(self):
		self.cavity = 'Linac1'
		self.actuator = 'dipole'
		self.nSamples = 3
		self.start = 70
		self.stop = 100
		self.step = 1
		self.initialGuess = [0, 10, 0.3, 89]
		self.getDataFunction = partial(self.getBPMPosition, self.parameters['dispersive_bpm'])
		self.findDipoleCurrent()

	def gunPhaser(self, gunPhaseSet=0, offset=True):
		if isinstance(self.calibrationPhase['Gun'],(float, int)) and isinstance(gunPhaseSet, (float, int)):
			self.setGunPhase(self.calibrationPhase['Gun'] + (gunPhaseSet if offset else 0))

	def linac1Phaser(self, linac1PhaseSet=0, offset=True):
		if isinstance(self.calibrationPhase['Linac1'],(float, int)) and isinstance(linac1PhaseSet, (float, int)):
			self.setLinac1Phase(self.calibrationPhase['Linac1'] + (linac1PhaseSet if offset else 0))

	def setUpMagnets(self,magnets):
		deguassingList=[]
		print('Degaussing magnets...')
		for magnet in magnets:
			if self.view.checkBox_deguassQ.isChecked() and self.magnets.isAQuad(magnet):
				deguassingList.append(magnet)
			elif self.view.checkBox_deguassC.isChecked() and self.magnets.isACor(magnet):
				deguassingList.append(magnet)
			elif self.view.checkBox_deguassS.isChecked() and self.magnets.isASol(magnet):
				deguassingList.append(magnet)
			elif self.view.checkBox_deguassD.isChecked() and self.magnets.isADip(magnet):
				deguassingList.append(magnet)
		print('Magnet to be Degaussed: '+str(deguassingList))
		self.magnets.degauss(deguassingList, True)
		while(self.magnets.isDegaussing(dipole)):
			print('Waiting for '+dipole+' to degauss...')
			time.sleep(0.1)
			app.processEvents()
		print('Switching off magnets...')
		switchOfFList=[]
		for magnet in magnets:
			if self.view.checkBox_quadOff.isChecked() and self.magnets.isAQuad(magnet):
				switchOfFList.append(magnet)
			elif self.view.checkBox_corrOff.isChecked() and self.magnets.isACor(magnet):
				switchOfFList.append(magnet)
		print('Magnet to be Switched Off: '+str(switchOfFList))
		self.magnets.switchOFFpsu(switchOfFList)

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
		self.magnets.setSI(dipole,current)

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
			self.data.append(value)
		else:
			# print 'BPM ', bpm, ' = ', self.bpm.getXFromPV(bpm)
			self.data.append(self.bpm.getXFromPV(bpm))

	def getWCMCharge(self, scope):
		if self.machineType == 'None':
			value = 50*np.random.random_sample()
			self.data.append(value)
		else:
			self.data.append(self.scope.getCharge(scope))

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

	def printFinalPhase(self):
		print self.cavity+' '+self.actuator+' fit = '+str(self.crestingData[self.cavity]['calibrationPhase'])
		self.logger.emit(self.cavity+' '+self.actuator+' fit = '+str(self.crestingData[self.cavity]['calibrationPhase']))


	def resetDataArray(self):
		self.crestingData.resetData(self.cavity, self.actuator, ['xFit', 'yFit', 'xData', 'yData', 'yStd'])

	def setDataArray(self, x, y, yStd):
		self.crestingData[self.cavity][self.actuator]['xData'].append(x)
		self.crestingData[self.cavity][self.actuator]['yData'].append(y)
		self.crestingData[self.cavity][self.actuator]['yStd'].append(yStd)
		self.newData.emit()

	def setFitArray(self, x, y):
		self.crestingData[self.cavity][self.actuator]['xFit'] = x
		self.crestingData[self.cavity][self.actuator]['yFit'] = y
		self.newData.emit()

	def getDataArray(self, column=None, zipped=True, sortKey=None):
		if column is not None:
			return self.crestingData[self.cavity][self.actuator][column]
		else:
			data = [self.crestingData[self.cavity][self.actuator]['xData'],
				self.crestingData[self.cavity][self.actuator]['yData'],
				self.crestingData[self.cavity][self.actuator]['yStd']]
			if sortKey is not None:
				data = zip(*sorted(zip(*data), key=sortKey))
			if zipped:
				return zip(*data)
			else:
				return data

	def getFitArray(self, zipped=True):
		data = [self.crestingData[self.cavity][self.actuator]['xFit'],
			self.crestingData[self.cavity][self.actuator]['yFit']]
		if zipped:
			return zip(*data)
		else:
			return data

	def setFinalPhase(self, phase):
		phase = np.mod(180+phase,360)-180
		self.crestingData[self.cavity]['calibrationPhase'] = phase
		self.setPhase(self.cavity, phase)

	def getData(self):
		self.data = []
		while len(self.data) < 2:
			self.getDataFunction()
			time.sleep(self.sleepTime)
		self.data = []
		while len(self.data) < self.nSamples:
			self.getDataFunction()
			time.sleep(self.sleepTime)
		return [np.mean(self.data), np.std(self.data)] if np.std(self.data) > 0.001 else [20,0]

########### findingCrestGunQuick ###############

	def findingCrestGunQuick(self):
		self.resetDataArray()
		self.approxcrest = self.getPhase(self.cavity)
		for phase in np.arange(-180,180,self.stepSize):
			self.setPhase(self.cavity, phase)
			data, stddata = self.getData()
			self.setDataArray(phase, data, stddata)
		self.doFitGunQuick()

	def updateWCMCharge(self, value):
		self.data.append(value)

	def cutDataGunQuick(self):
		"""Return all data where the charge is >= 25% of the maximum and is at least 10pC"""
		allData = self.getDataArray()
		max_charge = max(self.getDataArray('yData'))

		cutData = [a for a in allData if a[1] > max_charge / 4 and a[1] > 10 and a[2] < 2]
		return cutData

	def doFitGunQuick(self):
		cutData = self.cutDataGunQuick()
		x, y, std = zip(*cutData)
		if max(x) - min(x) > 90:
			x = [a if a >= 0 else a+360 for a in x]
		crest_phase = (x[-1] + x[0]) / 2.0
		if crest_phase > 180:
			crest_phase -= 360
		x = [a if a <= 180 else a-360 for a in x]
		self.setFitArray(np.array(x), np.array(y))
		self.setFinalPhase(crest_phase)
		self.printFinalPhase()

########### findingCrestLinac1Quick ###############

	def findingCrestLinac1Quick(self):
		self.resetDataArray()
		self.approxcrest = self.getPhase(self.cavity)
		for phase in np.arange(-180,180,self.stepSize):
			self.setPhase(self.cavity, phase)
			data, stddata = self.getData()
			self.setDataArray(phase, data, stddata)
		self.doFitLinac1Quick()

	def cutDataLinac1Quick(self):
		allData = self.getDataArray()
		cutData = [a for a in allData if a[1] == 20]
		newlist = []
		for i, pt in enumerate(cutData):
			if i < (len(cutData)-1):
				if not cutData[i+1][0] - pt[0] > 2*self.stepSize:
					newlist.append(pt)
			elif i == (len(cutData)-1):
				newlist.append(pt)
		return newlist

	def doFitLinac1Quick(self):
		try:
			cutData = self.cutDataLinac1Quick()
			x, y, std = zip(*cutData)
			if max(x) - min(x) > 180:
				x = [a if a >= 0 else a+360 for a in x]
			crest_phase = np.mean(x)-180
			if crest_phase > 180:
				crest_phase -= 360
			if crest_phase < 180:
				crest_phase += 360
			x = [a if a <= 180 else a-360 for a in x]
			self.setFitArray(np.array(x), np.array(y))
			self.setFinalPhase(crest_phase)
			self.printFinalPhase()
		except Exception as e:
			print(e)

########### findingCrestGunFine ###############

	def findingCrestFine(self):
		self.resetDataArray()
		if self.calibrationPhase[self.cavity] is None:
			self.approxcrest = self.getPhase(self.cavity)
		else:
			self.approxcrest = self.calibrationPhase[self.cavity]
		self.approxcrest = self.getPhase(self.cavity)
		self.minPhase = self.approxcrest-self.phiRange
		self.maxPhase = self.approxcrest+self.phiRange
		for phase in np.linspace(self.minPhase, self.maxPhase, self.phiSteps):
			self.setPhase(self.cavity, phase)
			time.sleep(self.sleepTime)
			currphase = self.getPhase(self.cavity)
			data, stddata = self.getData()
			if stddata > 0.0005:
				self.setDataArray(currphase, data, stddata)
		self.fittingFunc()

	def fittingFunc(self):
		if self.cavity == 'Gun':
			self.fittingGunFine()
		elif self.cavity == 'Linac1':
			self.fittingLinac1Fine()

	def fittingGunFine(self):
		x, y, std = self.getDataArray(zipped=False, sortKey=lambda x: x[0])
		if (max(x) - min(x)) > (self.maxPhase - self.minPhase):
			x = [a if a >= 0 else a+360 for a in x]
		f = UnivariateSpline(x, y, w=std, k=5)
		xnew = np.linspace(np.min(x), np.max(x), num=100, endpoint=True)
		ynew = f(xnew)
		crest_phase = xnew[np.argmin(ynew)]
		xnew = [a if a <= 180 else a-360 for a in xnew]
		if crest_phase > 180:
			crest_phase -= 360
		if crest_phase < 180:
			crest_phase += 360
		self.setFitArray(xnew, ynew)
		self.setFinalPhase(crest_phase)
		self.printFinalPhase()

	def fitting_equation_Linac1Fine(self, x, a, b, crest):
		return a + b * (np.sin((crest - (x + 180)) * degree)**2)

	def fittingLinac1Fine(self):
		x, y, std = self.getDataArray(zipped=False)
		popt, pcov = curve_fit(self.fitting_equation_Linac1Fine, x, y, \
			sigma=std,	p0=[0,10,self.approxcrest], bounds=[[-np.inf, -np.inf, min(x)], [np.inf, np.inf, max(x)]])

		phase = np.array(x)
		data = self.fitting_equation_Linac1Fine(phase, *popt)
		self.setFitArray(phase, data)
		self.setFinalPhase(((180 + popt[2]) % 360) - 180)
		self.printFinalPhase()

########### findingCrestGunFine ###############

	def findDipoleCurrent(self):
		self.setDip(self.start)
		while (self.getDip() / self.start) < 0.95 or (self.getDip() / self.start) > 1.05:
			time.sleep(self.sleepTime)
		self.resetDataArray()
		for dipI in np.arange(self.start, self.stop, self.step):
			self.setDip(dipI)
			time.sleep(self.sleepTimeDipole)
			data, stddata = self.getData()
			self.setDataArray(dipI, data, stddata)
		self.doFitDipoleCurrent()
		time.sleep(self.sleepTimeDipole)
		self.setDip(self.finalDipoleI)

	def cutDataDipoleCurrent(self):
		allData = self.getDataArray()
		cutData = [a for a in allData if not a[1] == 20]
		newlist = []
		for i, pt in enumerate(cutData):
			if i < (len(cutData)-1):
				if not cutData[i+1][0] - pt[0] > 2*self.step:
					newlist.append(pt)
			elif i == (len(cutData)-1):
				newlist.append(pt)
		return newlist

	def fitting_equation_DipoleCurrent(self, x, a, b, c, crest):
		return a + b * (np.sin(c * (x - crest)))

	def doFitDipoleCurrent(self):
		cutData = self.cutDataDipoleCurrent()
		x, y, std = zip(*cutData)
		xnew = np.linspace(np.min(x), np.max(x), num=100, endpoint=True)

		if max(x) < self.initialGuess[-1]:
			self.initialGuess[-1] = max(x)

		popt, pcov = curve_fit(self.fitting_equation_DipoleCurrent, x, y, sigma=std, \
		p0=self.initialGuess, bounds=([-np.inf, -np.inf, -np.inf, min(x)], [np.inf, np.inf, np.inf, max(x)]))

		self.setFinalPhase(popt[3])
		self.setFitArray(np.array(xnew), self.fitting_equation_DipoleCurrent(xnew, *popt))
		self.finalDipoleI = popt[3]
		self.printFinalPhase()
