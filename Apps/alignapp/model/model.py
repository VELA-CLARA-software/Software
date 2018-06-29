from epics import caget,caput
import os,sys
import time
import numpy as np
#sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VM-Controllers\\VELA-CLARA-Controllers\\Controllers\\VELA\INJECTOR\\velaINJMagnets\\bin\\Release')
#sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VM-Controllers\\VELA-CLARA-Controllers\\Controllers\\VELA\INJECTOR\\velaINJBeamPositionMonitors\\bin\\Release')
sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VM-Controllers\\VELA-CLARA-Controllers\\Controllers\\VELA\INJECTOR\\velaRFGun\\bin\\Release') 
sys.path.append('\\\\fed.cclrc.ac.uk\\org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VM-Controllers\\VELA-CLARA'
                '-Controllers\\bin\\Release\\')


#import velaINJMagnetControl as vimc # don't import this magnet controller. 
#import VELA_CLARA_MagnetControl as vimc
#from fauxlaser import fauxLaserController  as flaser
#import velaINJBeamPositionMonitorController as vibpm
#import VELA_CLARA_BPM_Control as vbpmc
from fauxscreenserver import fauxScreenServer as fscreens
#import velaRFGunControl as vrfgc

import VELA_CLARA_MagnetControl as vimc
import VELA_CLARA_BPM_Control as vbpmc
import VELA_CLARA_LLRFControl as llrf
import VELA_CLARA_PILaserControl as flaser

import onlineModel

#import velaRFGunControl as vrfgc
#import velaINJBeamPositionMonitorControl as vbpmc

class Model():
	def __init__(self, view):
#		self.gun =		vrfgc.velaRFGunController(False,False)
#		self.magnets =	vimc.velaINJMagnetController(True,False) # syntax for old mag controller
                self.maginit = vimc.init()
		self.magnets =	self.maginit.virtual_VELA_INJ_Magnet_Controller() # mag controller
#		self.magnets =	vimc.init().virtual_VELA_INJ_Magnet_Controller() # mag controller
		self.bpmsinit = vbpmc.init()
                self.bpms = self.bpmsinit.virtual_VELA_INJ_BPM_Controller()
		self.view = view
		self.updateOutput = 0
                self.laserinit = flaser.init() 
                self.laser = self.laserinit.virtual_PILaser_Controller()
#                self.laser = flaser(999,self.bpms,self) 
                self.scrs = fscreens()
                self.guninit = llrf.init()
                self.gun = self.guninit.virtual_VELA_LRRG_LLRF_Controller();
                self.virtual = True
		print 'Model initialised.'
                if self.virtual:
                        print 'and running the virtual machine simulation'
                        self.simulate = onlineModel.ASTRA()
                        self.gun.setAmp(63)
                        self.gun.setPhi(0)
                        self.laser.setVpos(0.0)
                        self.laser.setHpos(0.0)#mm
                        self.simulate.run(0.0)
#                        self.vm(001, 10, 1320, 0.076, 0.25, 0.25, "F", 0.0, 1800, 1, 0.228, -0.14, 0.138, -0.230, 0, 0)
                       
                
        def dummyfn(self):
                for i in range(0,40):
                      print self.magnets.getMagnetNames()[i]
                self.magnets.setSI('SOL',5.5)
                print self.magnets.getRI('SOL')

        def correctorbit(self):
                print "I'm correcting the orbit"
                ni = 2
                nj = 2
                dxbpm = np.zeros((ni,nj))
                dybpm = np.zeros((ni,nj))
                dxscr = np.zeros((ni,nj))
                dyscr = np.zeros((ni,nj))
#                dx = [[0 for a in range(ni)] for a in range(nj)]
#                dy = [[0 for a in range(ni)] for a in range(nj)]
                for ix in range(0, ni):
                        for iy in range(0,nj):
                                print "*******POSITION ix ", ix, " iy ", iy
#                                self.laser.setXposition(ix)
#                                self.laser.setYposition(iy)
                                self.laser.setVpos(5.0)
                                self.laser.setHpos(5.0)#mm
# set solenoids to first value 
                                self.magnets.setSI('SOL',10.0) # keep this
                                if self.virtual: 
                                        print "VIRTUAL MACHINE 1"
                                        self.simulate.run(0.1)
#                                        self.laser.C = np.array([[1,1], [1,1]]) # delete this
#                                        self.laser.setXpositionf(ix)# delete this
#                                        self.laser.setYpositionf(iy) # delete this
#                                        self.laser.setbeampos2()
                                        time.sleep(1)

# get the BPM-1 x,y                               
                                x1bpm = self.bpms.getXFromPV('BPM02')
                                y1bpm = self.bpms.getYFromPV('BPM02')
                                print "***DEBUG1", x1bpm, y1bpm
# get screen YAG-01 x,y 
# this assumes that an image server will be written and running 
                                x1scr = self.scrs.getX('YAG01')
                                y1scr = self.scrs.getY('YAG01')

# set the solenoid to a different value
                                self.magnets.setSI('SOL',15.0)
                                if self.virtual: 
                                        self.simulate.run(0.4)                                        
#                                        self.laser.C = np.array([[2,2], [2,2]]) # delete this
#                                        self.laser.setXpositionf(ix)# delete this
#                                        self.laser.setYpositionf(iy) # delete this
#                                        self.laser.setbeampos2()
                                        time.sleep(1)

# get the BPM1-1 x,y again
                                x2bpm = self.bpms.getXFromPV('BPM02')
                                y2bpm = self.bpms.getYFromPV('BPM02')
                                print "***DEBUG2", x2bpm, y2bpm
# get screen YAG-01 x,y again
# this assumes that an image server will be written and running 
                                x2scr = self.scrs.getX('YAG01')
                                y2scr = self.scrs.getY('YAG01')

# delx,dely 
                                print "sequenceee", x1bpm, x2bpm, y1bpm, y2bpm
#                                dx[ix][iy] = x2[0]-x1[0]
#                                dy[ix][iy] = y2[0]-y1[0]
                                dxbpm[ix][iy] = abs(x2bpm-x1bpm)
                                dybpm[ix][iy] = abs(y2bpm-y1bpm)
                                dxscr[ix][iy] = abs(x2scr-x1scr)
                                dyscr[ix][iy] = abs(y2scr-y1scr)
                                print "*******end of loop ix ", ix, " iy ", iy
                print "x movement of BPM array is ", dxbpm
                print "the minium movement of the BPM is ", np.amin(dxbpm)
                print "y movement of BPM array is ", dybpm
                print "the minium movement of the BPM is ", np.amin(dybpm)


        def vm(self, runNum, numPart, endOfLine, pLen, spotSize, charge, scTF, solBSol, rfAmp, rfPhase, qK1, qK2, qK3, qK4, offX, offY):
		# Instantiate controllers
#		self.magnetController = vimc.init()
#		self.bpmController = vbpmc.init()
#		self.vela_inj = vbpmc.MACHINE_AREA.VELA_INJ
#		self.virtual = vbpmc.MACHINE_MODE.VIRTUAL
#		self.magnets =	self.magnetController.getMagnetController(self.virtual, self.vela_inj)
#		self.bpms = self.bpmController.getBPMController(self.virtual, self.vela_inj)
#                self.magnets = self.magnetController.virtual_VELA_INJ_Magnet_Controller()
#                self.bpms = self.bpmController.virtual_VELA_INJ_BPM_Controller()
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

#		os.system('VBoxManage --nologo guestcontrol "VMSimulator" copyto --username "vmsim" --password "password" --target-directory "/home/vmsim/Desktop/virtualManager/" "'+os.getcwd()+'\\astraSetup"')

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
