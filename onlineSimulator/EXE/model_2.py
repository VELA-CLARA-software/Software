
import sys,os
import time
os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12" #BE SPECIFIC.... YOUR I.P. FOR YOUR VM
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
os.environ["EPICS_CA_SERVER_PORT"]="6000"
sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\stagetim')
sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\OnlineModel')
import onlineModel

import VELA_CLARA_Magnet_Control as mag
import VELA_CLARA_BPM_Control as bpm
import VELA_CLARA_LLRFControl as llrf
import VELA_CLARA_PILaserControl as pil

class Model():
	def __init__(self,view):
		self.view = view
		self.magInit = mag.init()
		self.bpmInit = bpm.init()
		self.pilInit = pil.init()
		self.llrfInit = llrf.init()

		self.magnets = 	self.magInit.virtual_VELA_INJ_Magnet_Controller()
		self.laser = 	self.pilInit.virtual_PILaser_Controller()
		self.bpms = 	self.bpmInit.virtual_VELA_INJ_BPM_Controller()
		self.gun = 		self.llrfInit.virtual_CLARA_LRRG_LLRF_Controller()
		self.LINAC01 = 	self.llrfInit.virtual_L01_LLRF_Controller()
		self.Cmagnets = self.magInit.virtual_CLARA_PH1_Magnet_Controller()
		'''Turning Magnets ON'''
		self.magnets.switchONpsu('SOL')
		self.magnets.switchONpsu('QUAD01')
		self.magnets.switchONpsu('QUAD02')
		self.magnets.switchONpsu('QUAD03')
		self.magnets.switchONpsu('QUAD04')
		self.magnets.switchONpsu('QUAD05')
		self.magnets.switchONpsu('QUAD06')
		self.magnets.switchONpsu('BSOL')

		self.Cmagnets.switchONpsu('LRG-BSOL')
		self.Cmagnets.switchONpsu('LRG-SOL')
		self.Cmagnets.switchONpsu('L01-SOL1')
		self.Cmagnets.switchONpsu('L01-SOL2')
		self.Cmagnets.switchONpsu('S02-QUAD1')
		self.Cmagnets.switchONpsu('S02-QUAD2')
		self.Cmagnets.switchONpsu('S02-QUAD3')
		self.Cmagnets.switchONpsu('S02-QUAD4')
		self.Cmagnets.switchONpsu('C2V-QUAD1')
		self.Cmagnets.switchONpsu('C2V-QUAD2')
		self.Cmagnets.switchONpsu('C2V-QUAD3')
		self.Cmagnets.switchONpsu('S01-HCOR1')
		self.Cmagnets.switchONpsu('S01-VCOR1')
		self.Cmagnets.switchONpsu('S01-HCOR1')
		self.Cmagnets.switchONpsu('S01-VCOR2')
		self.Cmagnets.switchONpsu('S02-HCOR1')
		self.Cmagnets.switchONpsu('S02-VCOR1')
		self.Cmagnets.switchONpsu('S02-HCOR2')
		self.Cmagnets.switchONpsu('S02-VCOR2')
		self.Cmagnets.switchONpsu('S02-HCOR3')
		self.Cmagnets.switchONpsu('S02-VCOR3')
		self.Cmagnets.switchONpsu('C2V-HCOR1')
		self.Cmagnets.switchONpsu('C2V-VCOR1')
		self.Cmagnets.switchONpsu('DIP01')
		self.Cmagnets.switchONpsu('DIP02')

		self.ASTRA = onlineModel.ASTRA(V_MAG_Ctrl=self.magnets,
									C_S01_MAG_Ctrl=self.Cmagnets,
									C_S02_MAG_Ctrl=self.Cmagnets,
									C2V_MAG_Ctrl=self.Cmagnets,
									V_RF_Ctrl=self.gun,
									C_RF_Ctrl=self.gun,
									L01_RF_Ctrl=self.LINAC01,
									messages=False)

		print("Model Initialized")

	def run(self):
		#set stuff
		self.laser.setVpos(self.view.doubleSpinBox_y_off.value())
		self.laser.setHpos(self.view.doubleSpinBox_x_off.value())
		self.magnets.setSI('SOL',self.view.doubleSpinBox_V_sol.value())
		self.magnets.setSI('QUAD01',self.view.doubleSpinBox_V_q1.value())
		self.magnets.setSI('QUAD02',self.view.doubleSpinBox_V_q2.value())
		self.magnets.setSI('QUAD03',self.view.doubleSpinBox_V_q3.value())
		self.magnets.setSI('QUAD04',self.view.doubleSpinBox_V_q4.value())
		self.magnets.setSI('QUAD05',self.view.doubleSpinBox_sp_q5.value())
		self.magnets.setSI('QUAD06',self.view.doubleSpinBox_sp_q6.value())

		self.magnets.setSI('HCOR01',self.view.doubleSpinBox_V_hcor01.value())
		self.magnets.setSI('HCOR02',self.view.doubleSpinBox_V_hcor02.value())
		self.magnets.setSI('HCOR03',self.view.doubleSpinBox_V_hcor03.value())
		self.magnets.setSI('HCOR04',self.view.doubleSpinBox_V_hcor04.value())
		self.magnets.setSI('HCOR05',self.view.doubleSpinBox_sp_hcor05.value())
		self.magnets.setSI('VCOR01',self.view.doubleSpinBox_V_vcor01.value())
		self.magnets.setSI('VCOR02',self.view.doubleSpinBox_V_vcor02.value())
		self.magnets.setSI('VCOR03',self.view.doubleSpinBox_V_vcor03.value())
		self.magnets.setSI('VCOR04',self.view.doubleSpinBox_V_vcor04.value())
		self.magnets.setSI('VCOR05',self.view.doubleSpinBox_sp_vcor05.value())

		self.Cmagnets.setSI('S02-QUAD1',self.view.doubleSpinBox_C_s02_q1.value())
		self.Cmagnets.setSI('S02-QUAD2',self.view.doubleSpinBox_C_s02_q2.value())
		self.Cmagnets.setSI('S02-QUAD3',self.view.doubleSpinBox_C_s02_q3.value())
		self.Cmagnets.setSI('S02-QUAD4',self.view.doubleSpinBox_C_s02_q4.value())
		self.Cmagnets.setSI('C2V-QUAD1',self.view.doubleSpinBox_c2v_q1.value())
		self.Cmagnets.setSI('C2V-QUAD2',self.view.doubleSpinBox_c2v_q2.value())
		self.Cmagnets.setSI('C2V-QUAD3',self.view.doubleSpinBox_c2v_q3.value())

		self.Cmagnets.setSI('S01-HCOR1',self.view.doubleSpinBox_C_s01_hcor01.value())
		self.Cmagnets.setSI('S01-HCOR2',self.view.doubleSpinBox_C_s01_hcor02.value())
		self.Cmagnets.setSI('S02-HCOR1',self.view.doubleSpinBox_C_s02_hcor01.value())
		self.Cmagnets.setSI('S02-HCOR2',self.view.doubleSpinBox_C_s02_hcor02.value())
		self.Cmagnets.setSI('S02-HCOR3',self.view.doubleSpinBox_C_s02_hcor03.value())
		self.Cmagnets.setSI('C2V-HCOR1',self.view.doubleSpinBox_c2v_hcor01.value())
		self.Cmagnets.setSI('S01-VCOR1',self.view.doubleSpinBox_C_s01_vcor01.value())
		self.Cmagnets.setSI('S01-VCOR2',self.view.doubleSpinBox_C_s01_vcor02.value())
		self.Cmagnets.setSI('S02-VCOR1',self.view.doubleSpinBox_C_s02_vcor01.value())
		self.Cmagnets.setSI('S02-VCOR2',self.view.doubleSpinBox_C_s02_vcor02.value())
		self.Cmagnets.setSI('S02-VCOR3',self.view.doubleSpinBox_C_s02_vcor03.value())
		self.Cmagnets.setSI('C2V-VCOR1',self.view.doubleSpinBox_c2v_vcor01.value())

		self.Cmagnets.setSI('LRG-SOL',self.view.doubleSpinBox_C_sol.value())
		self.Cmagnets.setSI('L01-SOL1',self.view.doubleSpinBox_LINAC01_sol01.value())
		self.Cmagnets.setSI('L01-SOL2',self.view.doubleSpinBox_LINAC01_sol02.value())
		self.Cmagnets.setSI('DIP01',self.view.doubleSpinBox_c2v_d1.value())
		self.Cmagnets.setSI('DIP02',self.view.doubleSpinBox_c2v_d2.value())

		#print str(self.view.lineEdit_start.text())[:2]
		if str(self.view.lineEdit_start.text())[:2]=='C1':
			self.gun.setPhiDEG(self.view.doubleSpinBox_CGUN_phi.value())
			self.gun.setAmpMVM(self.view.doubleSpinBox_CGUN_grad.value())
		elif str(self.view.lineEdit_start.text())[:2]=='V1':
			self.gun.setPhiDEG(self.view.doubleSpinBox_VGUN_phi.value())
			self.gun.setAmpMVM(self.view.doubleSpinBox_VGUN_grad.value())
		else:
			print 'NOT STARTING ON A LINE WITH A GUN!'
		self.LINAC01.setAmpMVM(self.view.doubleSpinBox_LINAC01_grad.value())
		self.LINAC01.setPhiDEG(self.view.doubleSpinBox_LINAC01_phi.value())
		time.sleep(1)
		self.ASTRA.go(str(self.view.lineEdit_start.text()),str(self.view.lineEdit_stop.text()),'temp-start.ini')
		self.ASTRA.go('C1-GUN','SP-YAG04','temp-start.ini')