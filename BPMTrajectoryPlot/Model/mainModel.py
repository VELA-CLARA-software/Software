import epics
import random
import os,sys
import time
import numpy
import collections
sys.path.append('D:\\VELA-CLARA_software\\VELA-CLARA-Controllers-New-Structure-With-Magnets\\bin\\Release')
#sys.path.append('D:\\VELA-CLARA_software\\VELA-CLARA-Controllers\\Controllers\\VELA\\GENERIC\\velaChargeScope\\bin\\Release')

import VELA_CLARA_BPM_Control as vbpmc
#import VELA_CLARA_Scope_Control as vcsc

class Model():
	def __init__(self, bpmCont, scopeCont):
		self.bpmCont = bpmCont
		self.scopeCont = scopeCont
		self.bpmList = []
		#self.velaInjList = vbpmc.std_vector_string()
		self.velaInjList = []
		self.velaInjList.append('BPM01')
		self.velaInjList.append('BPM02')
		self.velaInjList.append('BPM04')
		self.velaInjList.append('BPM05')
		self.velaInjList.append('BPM06')
		#self.velaSP1List = vbpmc.std_vector_string()
		self.velaSP1List = []
		self.velaSP1List.append('BPM01')
		self.velaSP1List.append('BPM02')
		self.velaSP1List.append('BPM03')

	def monitorBPMs(self, pvList, numShots):
		self.pvList = pvList
		self.numShots = numShots
		self.bpmXData = {name:[] for name in self.pvList}
		self.bpmYData = {name:[] for name in self.pvList}
		if self.numShots > 1:
			self.bpmCont.monitorMultipleDataForNShots(long(self.numShots), self.pvList)
			for i in self.pvList:
				while self.bpmCont.isMonitoringBPMData(str(i)):
					time.sleep(0.01)
			#for j in range(self.numShots):
			for i in self.pvList:
				self.bpmXData[i] = numpy.mean(self.bpmCont.getBPMXVec(i))
				self.bpmYData[i] = numpy.mean(self.bpmCont.getBPMYVec(i))
			self.orderedX = collections.OrderedDict((name, self.bpmXData[name]) for name in self.pvList)
			self.orderedY = collections.OrderedDict((name, self.bpmYData[name]) for name in self.pvList)
		elif self.numShots == 1:
			for i in self.pvList:
				self.data = self.bpmCont.getAllBPMData(i)
				self.bpmXData[i] = self.data.x[0]
				self.bpmYData[i] = self.data.y[0]
			self.orderedX = collections.OrderedDict((name, self.bpmXData[name]) for name in self.pvList)
			self.orderedY = collections.OrderedDict((name, self.bpmYData[name]) for name in self.pvList)
			#time.sleep(0.1)
		return self.orderedX, self.orderedY
