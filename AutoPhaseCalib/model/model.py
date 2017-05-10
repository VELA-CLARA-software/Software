
import sys,os
import time
os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12" #BE SPECIFIC.... YOUR I.P. FOR YOUR VM
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
os.environ["EPICS_CA_SERVER_PORT"]="6000"

sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\Release')
sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\OnlineModel')

#import onlineModel

import VELA_CLARA_MagnetControl as mag
import VELA_CLARA_BPM_Control as bpm
import VELA_CLARA_LLRFControl as llrf
import VELA_CLARA_Scope_Control as scope

class Model():
	def __init__(self,view,machineType,lineType,gunType):
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
		self.finePhaseData=[]
		self.fineBPMData=[]
		self.approxPhaseFit=[]
		self.approxChargeFit=[]
		self.finePhaseFit=[]
		self.fineBPMFit=[]
		print("Model Initialized")

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


	def claraMethod(self):
		print('clara Method')
		self.method(magnets=[],bpm='',scope='')

	def velaMethod(self):
		print('vela Method')
		self.method(magnets=['QUAD01', 'QUAD02', 'QUAD03', 'QUAD04', 'QUAD05', 'QUAD06',
							'HCOR03', 'HCOR04', 'HCOR05', 'VCOR03', 'VCOR04', 'VCOR05',
							'SOL', 'BSOL', 'DIP-01'], bpm='BPM02', scope='SCOP01')

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

		'''4. Convert Current to Momentum'''
		if self.view.checkBox_4.isChecked()==True:
			print('4. Set Momentum of Beam')

	def setUpMagnets(self,magnets):
		print('1. Setting up Magnets')
		deguassingList=mag.std_vector_string()
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
			else:
				print('Magnet '+magnet+' is off or not selected to be deguassed.')
		print('Magnet to be Deguassed: '+str(deguassingList))
		self.activeMags = mag.std_vector_string()
		self.activeMags.append('QUAD01')
		#(self.activeMags, True)
		self.magnets.degauss(self.activeMags, resetToZero = True)
		while self.magnets.isDegaussing('QUAD01')==True:
			print('hi')
			time.sleep(5)

		print('Switching off magnets...')
		switchOfFList=mag.std_vector_string()
		for magnet in magnets:
			if self.view.checkBox_quadOff and self.magnets.isAQuad(magnet):
				switchOfFList.append(magnets)
			elif self.view.checkBox_corrOff and self.magnets.isACor(magnet):
				switchOfFList.append(magnets)
			else:
				print('No magnets to be switched off.')
			print('Magnet to be Switched Off: '+str(switchOfFList))
			self.magnets.switchOFFpsu(switchOfFList)

			print('Setting Dipole for predicted momentum...')
