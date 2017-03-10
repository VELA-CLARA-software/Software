"""

"""
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QThread
import os,sys

#class ASTRA(QThread):
class ASTRA():
	def __init__(self):
#		QtCore.QThread.__init__(self)
		self.runNum='001'
		self.particleNum = 1 		#Units of 1000s!!!
		self.pulseLength = 0.076	#units of picoseconds
		self.spotSize =  0.25		#diameter in units of mm (i think)
		self.charge = 0.25			#units of nC
		self.spaceCharge = 'F' 		#T or F (on/off)
		self.solAndBSol = 0.0		#Max amplitude in units of T
		self.EndOfLine = 500		#units of cm

	def __del__(self):
		self.wait()

	def run(self,SAB):
		self.solAndBSol = SAB
		os.system('VBoxManage --nologo guestcontrol "VMSimulator" run "usr/bin/python" --username "vmsim" --password "password" -- /home/vmsim/Desktop/virtualManager/run_astra.py ' +
			' ' + str(self.runNum) +
			' ' + str(self.particleNum) +
			' ' + str(self.pulseLength) +
			' ' + str(self.spotSize) +
			' ' + str(self.charge) +
			' ' + str(self.spaceCharge) +
			' ' + str(self.solAndBSol) +
			' ' + str(self.EndOfLine))
