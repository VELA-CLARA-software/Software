from PyQt4.QtCore import QThread, QObject, pyqtSignal, QTimer
import sys,os
import time
import scipy.constants as physics
import numpy as np
from scipy.optimize import curve_fit
import random as r

class Model(QObject):

	bpmX = pyqtSignal(float)

	def __init__(self, app, view, machineType, lineType, gunType, mag, scope, bpm, gunllrf, linac1llrf):
		QThread.__init__(self)
		self.app = app
		self.view = view
		self.magnets = mag
		self.scope = scope
		self.bpm = bpm
		self.gunllrf = gunllrf
		self.linac1llrf = linac1llrf
		self.machineType = machineType
		self.lineType = lineType
		self.gunType = gunType
		self.view.label_MODE.setText('MODE: '+self.machineType+' '+self.lineType+' with '+self.gunType+' Hz gun')
		self.approxPhaseData=[]
		self.approxChargeData=[]
		self.approxPhaseFit=[]
		self.approxChargeFit=[]
		self.finePhaseFit=[]
		self.fineBPMFit=[]
		self.finePhaseData=[]
		self.fineBPMData=[]
		self.parameters={}
		self.calibrationPhase = {'Gun': 0, 'Linac1': 0}
		self.run()
		print("Model Initialized")
	#DESTRUCTOR

	def start(self):
		self.run()

	def run(self):
		if self.lineType=='VELA':
			self.velaMethod()
		elif self.lineType=='CLARA':
			self.claraMethod()

	def claraMethod(self):
		print('clara Method')
		self.parameters['magnets']=[]
		self.parameters['bpm'] = 'C2V-BPM01'
		self.parameters['scope'] = ''

	def velaMethod(self):
		print('vela Method')
		self.parameters['magnets']=['QUAD01', 'QUAD02', 'QUAD03', 'QUAD04', 'QUAD05', 'QUAD06',
							'HCOR03', 'HCOR04', 'HCOR05', 'VCOR03', 'VCOR04', 'VCOR05',
							'SOL', 'BSOL', 'DIP01']
		self.parameters['bpm'] = 'C2V-BPM01'
		self.parameters['scope'] = 'SCOP01'

	def magnetDegausser(self):
			print('1. Setting up Magnets')
			self.setUpMagnets(self.parameters['magnets'])

	def gunWCMCrester(self):
		if self.view.checkBox_2.isChecked()==True:
			print('2. Approximately Finding Crest')

	def gunBPMCrester(self):
			print('3. Finding Crest of Gun')
			self.crester = findingGunCrest(self, self.parameters['magnets'], self.parameters['bpm'], int(self.view.rangeSet.text()), int(self.view.nScanningSet.text()))
			self.bpmX.connect(self.crester.updateBPMPosition)
			self.timer = QTimer()
			self.timer.timeout.connect(lambda : self.getBPMPosition(self.parameters['bpm']))
			self.timer.start(100)
			self.thread = QThread()  # no parent!
			self.crester.moveToThread(self.thread)
			self.thread.started.connect(self.crester.findingCrest)
			self.crester.finished.connect(self.thread.quit)
			self.crester.finished.connect(self.timer.stop)
			self.crester.setPhase.connect(self.setPhase)
			self.thread.start()

	def linacBPMCrester(self):
			print('5. Finding Crest of Linac')
			self.crester = findingLinacCrest(self, self.parameters['magnets'], self.parameters['bpm'], int(self.view.rangeSet.text()), int(self.view.nScanningSet.text()))
			self.bpmX.connect(self.crester.updateBPMPosition)
			self.timer = QTimer()
			self.timer.timeout.connect(lambda : self.getBPMPosition(self.parameters['bpm']))
			self.timer.start(100)
			self.thread = QThread()  # no parent!
			self.crester.moveToThread(self.thread)
			self.thread.started.connect(self.crester.findingCrest)
			self.crester.finished.connect(self.thread.quit)
			self.crester.finished.connect(self.timer.stop)
			self.crester.setPhase.connect(self.setPhase)
			self.thread.start()

	def gunPhaser(self):
			print('6. Setting Linac 1 Phase to ', str(self.calibrationPhase['Gun'] + int(self.view.gunPhaseSet.text())), ' (',self.view.linac1PhaseSet.text()),')'
			self.setGunPhase(self.calibrationPhase['Gun'] + int(self.view.gunPhaseSet.text()))

	def linac1Phaser(self):
			print('6. Setting Linac 1 Phase to ', str(self.calibrationPhase['Linac1'] + int(self.view.linac1PhaseSet.text())), ' (', self.view.linac1PhaseSet.text()),')'
			self.setLinac1Phase(self.calibrationPhase['Linac1'] + int(self.view.linac1PhaseSet.text()))

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

	def setGunPhase(self, phase):
		print 'setting Gun phase = ', phase
		self.gunllrf.setPhiSP(phase)

	def getGunPhase(self):
		return self.gunllrf.getPhiSP()

	def setLinac1Phase(self, phase):
		print 'setting L01 phase = ', phase
		self.linac1llrf.setPhiSP(phase)

	def getLinac1Phase(self):
		return self.linac1llrf.getPhiSP()

	def getBPMPosition(self, bpm):
		self.bpmX.emit(1000*self.bpm.getXFromPV(bpm))

class findingGunCrest(QObject):

	cavity = 'Gun'
	finished = pyqtSignal()
	setPhase = pyqtSignal(str, float)
	data = []

	def __init__(self, parent,  magnets, bpm, phiRange, phiSteps):
		super(findingGunCrest, self).__init__()
		self.parent = parent
		self.magnets = magnets
		self.bpm = bpm
		self.phiRange = phiRange
		self.phiSteps = phiSteps
		self.bpmX = None

	def updateBPMPosition(self, value):
		self.data.append(value)

	def findingCrest(self):
		self.parent.finePhaseFit=[]
		self.parent.fineBPMFit=[]
		self.parent.finePhaseData=[]
		self.parent.fineBPMData=[]

		self.approxcrest = self.parent.getPhase(self.cavity)
		for phase in np.linspace(self.approxcrest-self.phiRange, self.approxcrest+self.phiRange, self.phiSteps):
			self.setPhase.emit(self.cavity, phase)
			time.sleep(0.1)
			currphase = self.parent.getPhase(self.cavity)
			print 'set phase to',phase
			print 'phase got to', currphase
			self.data = []
			while len(self.data) < 10:
				time.sleep(0.1)
			data = np.mean(self.data)
			self.parent.fineBPMData.append(data)
			self.parent.finePhaseData.append(currphase)

		def func(list, a, b, c):
			x = np.array(list)
			return a*x**2 + b*x + c

		popt, pcov = curve_fit(func, self.parent.finePhaseData, self.parent.fineBPMData, p0=None)
		self.parent.finePhaseFit = np.linspace(self.approxcrest-self.phiRange, self.approxcrest+self.phiRange, 200)
		self.parent.fineBPMFit = func(self.parent.finePhaseFit, *popt)

		self.parent.calibrationPhase[self.cavity] = -popt[1]/(2*popt[0])
		print 'Calibration phase is', self.parent.calibrationPhase[self.cavity]
		self.finished.emit()

class findingLinacCrest(findingGunCrest):

	cavity = 'Linac1'
	setPhase = pyqtSignal(str, float)


class setUpGun(QObject):

	def setUpGun(self, desiredPhase, bpm):
		self.gun.setPhiSP(desiredPhase+self.calibrationPhase)
		x = 1000*self.bpm.getXFromPV(bpm)
		currentAmp = self.gun.getAmpSP()
		step = 50 #(MV/m)
		time.sleep(1)
		print x
		while abs(x)>0.01:
			currentAmp = self.gun.getAmpSP()
			print 'currentAmp = ', currentAmp
			self.gun.setAmpSP(currentAmp+step)
			print 'setting  = ', currentAmp+step
			time.sleep(0.1)
			self.app.processEvents()
			x_old = x
			x = 1000*self.bpm.getXFromPV(bpm)
			print bpm,' = ', x
			if x < 0:
				step = -abs(step)
			elif x > 0:
				step = abs(step)
			if abs(x - x_old) > abs(x):
				step = 0.5*step
