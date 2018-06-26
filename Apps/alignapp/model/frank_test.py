import epics
from epics import caget,caput
import os,sys
import time
import randomPVs
import threading
import VELA_CLARA_MagnetControl as vimc
import VELA_CLARA_BPM_Control as vbpmc

os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12" #BE SPECIFIC.... YOUR I.P. FOR YOUR VM 
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"

class main():
	def __init__(self):
		# Initialise magnet and BPM controllers, and import function to set random PVs to EPICS
		self.magnetController = vimc.init()
		self.bpmController = vbpmc.init()
		self.setRanPVs = randomPVs.setRandomPV()
		# The following two lines set the area of interest - in this case the VELA injector section, for the virtual machine
		self.vela_inj = vimc.MACHINE_AREA.VELA_INJ
		self.virtual = vimc.MACHINE_MODE.VIRTUAL
		# This instantiates the controller modules for BPMs and magnets, meaning that you can access the hardware controllers
		# through these objects
		self.magnets =	self.magnetController.getMagnetController(self.virtual, self.vela_inj)
		self.bpms = self.bpmController.getBPMController(self.virtual, self.vela_inj)
		# All the magnets and BPMs belonging to this section of the machine are named here
		self.magnetPVs = self.magnets.getQuadNames()
		self.bpmPVs = self.bpms.getBPMNames()
		# As we are just doing a tester, we can change quad01 and look at bpm01
		self.quad01 = self.magnetPVs[0]
		self.bpm01 = self.bpmPVs[0]
		# This is to get the full EPICS PV ('VM-EBT-blahblah') for doing caput to EPICS
		self.allBPM01Data = self.bpms.getBPMDataObject(self.bpm01)
		self.fullBPM01PV = self.allBPM01Data.pvRoot+":DATA:B2V.VALA"
		# We will set a range of values to a PV so that we can loop over them
		self.valuesToSet = [1,2,3,4,5]
		self.results = self.moveAndMonitor(self.bpm01, self.quad01, self.valuesToSet, self.fullBPM01PV)
		for i in self.valuesToSet:
			print "BPM x for QUAD01 = ", self.results[0][i-1], " is ", self.results[1][i-1]
			print "BPM y for QUAD01 = ", self.results[0][i-1], " is ", self.results[2][i-1]
		
		
	def moveAndMonitor(self, bpmPV, magPV, values, fullBPMPV):
		self.bpmPV = bpmPV
		self.magPV = magPV
		self.fullBPMPV = fullBPMPV
		self.magRIVals = []
		self.bpmXVals = []
		self.bpmYVals = []
		self.values = values
		# We loop over the values given above
		for i in self.values:
			# Set a magnet current according to the list of values, and append the read current to a new array
			self.magnets.setSI(self.magPV, i)
			self.magRIVals.append(self.magnets.getRI(self.magPV))
			# Set a random value to the BPMs, just for 1 shot in this case
			self.setRanPVs.caputRanPV(self.fullBPMPV, i-3, i+3, 1, 1, "array")
			time.sleep(0.2)
			# Append the read BPM X and Y values to arrays, and return all these values to the main function
			self.bpmXVals.append(self.bpms.getX(self.bpmPV))
			self.bpmYVals.append(self.bpms.getY(self.bpmPV))
		return self.magRIVals, self.bpmXVals, self.bpmYVals
			
if __name__ == '__main__':
    app = main()