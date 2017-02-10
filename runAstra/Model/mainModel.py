import epics
from epics import caget,caput
import os,sys
import time
sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VM-Controllers\\VELA-CLARA-Controllers\\Controllers\\VELA\INJECTOR\\velaRFGun\\bin\\Release')

import VELA_CLARA_MagnetControl as vimc
import velaRFGunControl as vrfgc
import VELA_CLARA_BPM_Control as vbpmc
class Model():
	def __init__(self, view):
		self.magnetController = vimc.init()
		self.bpmController = vbpmc.init()
		self.vela_inj = vbpmc.MACHINE_AREA.VELA_INJ
		self.virtual = vbpmc.MACHINE_MODE.VIRTUAL
		self.magnets =	self.magnetController.getMagnetController(self.virtual, self.vela_inj)
		self.bpms = self.bpmController.getBPMController(self.virtual, self.vela_inj)
		self.gun =		vrfgc.velaRFGunController(False,False)
		self.view = view
		self.updateOutput = 0
		print 'Model initialised.'
	def runASTRA(self):

		setup = open('astraSetup', 'w')
		# run number# aa = str(self.view.lineEdit_RN.text())
		setup.write(self.view.lineEdit_RN.text()+'\n')
		# particle number
		setup.write(self.view.lineEdit_NOP.text()+'\n')
		# start
		setup.write('0'+'\n')
		# stop
		setup.write(self.view.lineEdit_EOL.text()+'\n')
		# generarte distrib
		setup.write('True'+'\n')
		# name of distrib
		setup.write('N/A'+'\n')
		# pulse length
		setup.write(self.view.lineEdit_PL.text()+'\n')
		# spotsize
		setup.write(self.view.lineEdit_SS.text()+'\n')
		# Charge
		setup.write(self.view.lineEdit_C.text()+'\n')
		# space Charge
		setup.write(self.view.lineEdit_SC.text()+'\n')
		# SOL and BSOL
		setup.write(self.view.lineEdit_SAB.text()+'\n')
		# QUADS in USE
		quadCheckBoxes = [self.view.checkBox_useQuad_1,self.view.checkBox_useQuad_2,self.view.checkBox_useQuad_3,self.view.checkBox_useQuad_4,self.view.checkBox_useQuad_5,self.view.checkBox_useQuad_6,self.view.checkBox_useQuad_7,self.view.checkBox_useQuad_8,self.view.checkBox_useQuad_9]
		quadsInUse = []
		for i in range(9):
			if quadCheckBoxes[i].isChecked():
				quadsInUse.append('1')
				print(1)
			else :
				print(0)
				quadsInUse.append('0')
		for quad in quadsInUse:
			setup.write(quad+' ')# Screens in Use
		setup.write('\n'+"-1.5"+'\n')
		setup.write("-1.5"+'\n')# BPMs in Use
		setup.write(""+'\n')
		setup.close()

		os.system('VBoxManage --nologo guestcontrol "VMSimulator" copyto --username "vmsim" --password "password" --target-directory "/home/vmsim/Desktop/virtualManager/" "'+os.getcwd()+'\\astraSetup"')

		os.system('VBoxManage --nologo guestcontrol "VMSimulator" run "usr/bin/python" --username "vmsim" --password "password" -- /home/vmsim/Desktop/virtualManager/run_astra.py ' +
			' ' + str(self.view.lineEdit_RN.text()) +
			' ' + str(self.view.lineEdit_NOP.text()) +
			' ' + str(self.view.lineEdit_PL.text()) +
			' ' + str(self.view.lineEdit_SS.text()) +
			' ' + str(self.view.lineEdit_C.text()) +
			' ' + str(self.view.lineEdit_SC.text()) +
			' ' + str(self.view.lineEdit_SAB.text()) +
			' ' + str(self.view.lineEdit_EOL.text()) +
			' ' + str(-1.5) +
			' ' + str(-1.5))
		print(			' ' + str(self.view.lineEdit_RN.text()) +
					' ' + str(self.view.lineEdit_NOP.text()) +
					' ' + str(self.view.lineEdit_PL.text()) +
					' ' + str(self.view.lineEdit_SS.text()) +
					' ' + str(self.view.lineEdit_C.text()) +
					' ' + str(self.view.lineEdit_SC.text()) +
					' ' + str(self.view.lineEdit_SAB.text()) +
					' ' + str(self.view.lineEdit_EOL.text()))
		self.updateOutput=1
		print("Updating output graphs..")
		time.sleep(5) # THis allows output graphs to update
		print("Done.")
		self.updateOutput=0



	#setup.close()# / home / vmsim / Desktop / virtualManager / run_astra.py# / home / vmsim / Desktop / hi.py
	def setVM(self):

		self.gun.setAmp(long(self.view.lineEdit_RFGA.text()))
		self.gun.setPhi(long(self.view.lineEdit_RFGP.text()))
		self.magnets.setSI('QUAD01', float(self.view.lineEdit_Q1C.text()))
		self.magnets.setSI('QUAD02', float(self.view.lineEdit_Q2C.text()))
		self.magnets.setSI('QUAD03', float(self.view.lineEdit_Q3C.text()))
		self.magnets.setSI('QUAD04', float(self.view.lineEdit_Q4C.text()))
		self.magnets.setSI('QUAD07', float(self.view.lineEdit_Q7C.text()))
		self.magnets.setSI('QUAD08', float(self.view.lineEdit_Q8C.text()))
		self.magnets.setSI('QUAD09', float(self.view.lineEdit_Q9C.text()))
		self.magnets.switchONpsu('QUAD01')
		self.magnets.switchONpsu('QUAD02')
		self.magnets.switchONpsu('QUAD03')
		self.magnets.switchONpsu('QUAD04')
		self.magnets.switchONpsu('QUAD07')
		self.magnets.switchONpsu('QUAD08')
		self.magnets.switchONpsu('QUAD09')
