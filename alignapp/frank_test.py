import epics
from epics import caget,caput
import os,sys
import time
sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VM-Controllers\\VELA-CLARA-Controllers\\Controllers\\VELA\INJECTOR\\velaRFGun\\bin\\Release')
os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12" #BE SPECIFIC.... YOUR I.P. FOR YOUR VM 
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
import VELA_CLARA_MagnetControl as vimc
import velaRFGunControl as vrfgc
import VELA_CLARA_BPM_Control as vbpmc
class main():
	def __init__(self, runNum, numPart, endOfLine, pLen, spotSize, charge, scTF, solBSol, rfAmp, rfPhase, qK1, qK2, qK3, qK4, offX, offY):
		# Instantiate controllers
		self.magnetController = vimc.init()
		self.bpmController = vbpmc.init()
		self.vela_inj = vbpmc.MACHINE_AREA.VELA_INJ
		self.virtual = vbpmc.MACHINE_MODE.VIRTUAL
#		self.magnets =	self.magnetController.getMagnetController(self.virtual, self.vela_inj)
#		self.bpms = self.bpmController.getBPMController(self.virtual, self.vela_inj)
                self.magnets = self.magnetController.virtual_VELA_INJ_Magnet_Controller()
                self.bpms = self.bpmController.virtual_VELA_INJ_BPM_Controller()
		self.gun = vrfgc.velaRFGunController(False,False)
		# Run number is a 3-digit number required for online model
		self.runNum = str(runNum)
		# Number of particles (in 1000s)
		self.numPart = str(numPart)
		# End of beamline - TP and BDM program goes up to 1320cm
		self.endOfLine = str(endOfLine)
		#self.genDist = str(genDist)
		# Laser pulse length
		self.pLen = str(pLen)
		# Laser spot size
		self.spotSize = str(spotSize)
		# Bunch charge in nC
		self.charge = str(charge)
		# Space charge True/False
		self.scTF = str(scTF)
		# Combined sol/bsol field
		self.solBSol = str(solBSol)
		# RF amplitude and phase
		self.rfAmp = str(rfAmp)
		self.rfPhase = str(rfPhase)
		# Quad strengths
		self.qK1 = str(qK1)
		self.qK2 = str(qK2)
		self.qK3 = str(qK3)
		self.qK4 = str(qK4)
		# X and Y offsets
		self.offX = str(offX)
		self.offY = str(offY)
		print 'Model initialised.'
		self.runASTRA()
		
	def runASTRA(self):

		setup = open('astraSetup', 'w')
		# run number# aa = str(self.view.lineEdit_RN.text())
		setup.write(self.runNum+'\n')
		# particle number
		setup.write(self.numPart+'\n')
		# start
		setup.write('0'+'\n')
		# stop
		setup.write(self.endOfLine+'\n')
		# generarte distrib
		setup.write('True'+'\n')
		# name of distrib
		setup.write('N/A'+'\n')
		# pulse length
		setup.write(self.pLen+'\n')
		# spotsize
		setup.write(self.spotSize+'\n')
		# Charge
		setup.write(self.charge+'\n')
		# space Charge
		setup.write(self.scTF+'\n')
		# SOL and BSOL
		setup.write(self.solBSol+'\n')
		# QUADS in USE
		setup.write(self.qK1+' ')
		setup.write(self.qK2+' ')
		setup.write(self.qK3+' ')
		setup.write(self.qK4+' \n')
		# X and Y offsets
		setup.write(self.offX+'\n')
		setup.write(self.offY+'\n')
		setup.write(""+'\n')
		setup.close()
		
		self.gun.setAmp(long(self.rfAmp))
		self.gun.setPhi(long(self.rfPhase))
		self.magnets.setSI('QUAD01', float(self.qK1))
		self.magnets.setSI('QUAD02', float(self.qK2))
		self.magnets.setSI('QUAD03', float(self.qK3))
		self.magnets.setSI('QUAD04', float(self.qK4))
		self.magnets.switchONpsu('QUAD01')
		self.magnets.switchONpsu('QUAD02')
		self.magnets.switchONpsu('QUAD03')
		self.magnets.switchONpsu('QUAD04')

		os.system('VBoxManage --nologo guestcontrol "VMSimulator" copyto --username "vmsim" --password "password" --target-directory "/home/vmsim/Desktop/virtualManager/" "'+os.getcwd()+'\\astraSetup"')

		os.system('VBoxManage --nologo guestcontrol "VMSimulator" run "usr/bin/python" --username "vmsim" --password "password" -- /home/vmsim/Desktop/virtualManager/run_astra.py ' +
			' ' + str(self.runNum) +
			' ' + str(self.numPart) +
			' ' + str(self.pLen) +
			' ' + str(self.spotSize) +
			' ' + str(self.charge) +
			' ' + str(self.scTF) +
			' ' + str(self.solBSol) +
			' ' + str(self.endOfLine) +
			' ' + str(self.offX) +
			' ' + str(self.offY))
						
if __name__ == '__main__':
    app = main(123, 1, 1320, 0.076, 0.25, 0.25, "F", 0.0, 1800, 1, 0.228, -0.14, 0.138, -0.230, 10.0, -10.0)
	# This will just run 1 ASTRA simulation - if you want to loop over a range of offsets you would do:
	# xoffRange = [-2, -1, 0, 1, 2]
	# bpmXPos = {num for num in xoffRange}
	# for i in xoffRange:
		# main(blah, blah, blah, i, blah)
		# num[i] = bpmController.getX('BPM01')
	# This would all be in a separate function which you could iterate over (I'm not 100% sure if this is what you want, or how well this works)
	# I'm going home now, but will check all this tomorrow
