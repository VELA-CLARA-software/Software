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

class monModel():
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
		self.velaSP1List = []
		#self.velaSP1List = vbpmc.std_vector_string()
		self.velaSP1List.append('BPM01')
		self.velaSP1List.append('BPM02')
		self.velaSP1List.append('BPM03')

	def monitorBPMs(self, pvList, numShots):
		self.pvList = pvList
		self.numShots = numShots
		self.bpmXData = {name:[] for name in self.pvList}
		self.bpmYData = {name:[] for name in self.pvList}
		self.bpmQData = {name:[] for name in self.pvList}
		self.bpmATT1Val = {name:[] for name in self.pvList}
		self.bpmATT2Val = {name:[] for name in self.pvList}
		if self.numShots > 1:
			self.bpmCont.monitorMultipleDataForNShots(long(self.numShots), self.pvList)
			for i in self.pvList:
				while self.bpmCont.isMonitoringBPMData(str(i)):
					time.sleep(0.01)
			#for j in range(self.numShots):
			for i in self.pvList:
				self.PU1Data[i] = numpy.mean(self.bpmCont.getBPMRawData(i)[1])
				self.PU2Data[i] = numpy.mean(self.bpmCont.getBPMRawData(i)[2])
				self.PU3Data[i] = numpy.mean(self.bpmCont.getBPMRawData(i)[5])
				self.PU4Data[i] = numpy.mean(self.bpmCont.getBPMRawData(i)[6])
				self.bpmXData[i] = self.PU1Data[i] - self.PU2Data[i]
				self.bpmYData[i] = self.PU3Data[i] = self.PU4Data[i]
				self.bpmQData[i] = numpy.mean(self.bpmCont.getBPMQVec(i))
				self.bpmATT1Val[i] = self.bpmCont.getRA1(i)
				self.bpmATT2Val[i] = self.bpmCont.getRA2(i)
			self.orderedX = collections.OrderedDict((name, self.bpmXData[name]) for name in self.pvList)
			self.orderedY = collections.OrderedDict((name, self.bpmYData[name]) for name in self.pvList)
			self.orderedQ = collections.OrderedDict((name, self.bpmQData[name]) for name in self.pvList)
			self.orderedATT1 = collections.OrderedDict((name, self.bpmATT1Val[name]) for name in self.pvList)
			self.orderedATT2 = collections.OrderedDict((name, self.bpmATT2Val[name]) for name in self.pvList)

		elif self.numShots == 1:
			for i in self.pvList:
				self.data = self.bpmCont.getAllBPMData(i)
				self.bpmXData[i] = self.data.pu1[0] - self.data.pu2[0]
				self.bpmYData[i] = self.data.pu3[0] - self.data.pu4[0]
				self.bpmQData[i] = self.data.q[0]
				print self.bpmQData[i], i
				self.bpmATT1Val[i] = self.bpmCont.getRA1(i)
				self.bpmATT2Val[i] = self.bpmCont.getRA2(i)
			self.orderedX = collections.OrderedDict((name, self.bpmXData[name]) for name in self.pvList)
			self.orderedY = collections.OrderedDict((name, self.bpmYData[name]) for name in self.pvList)
			self.orderedQ = collections.OrderedDict((name, self.bpmQData[name]) for name in self.pvList)
			self.orderedATT1 = collections.OrderedDict((name, self.bpmATT1Val[name]) for name in self.pvList)
			self.orderedATT2 = collections.OrderedDict((name, self.bpmATT2Val[name]) for name in self.pvList)
		return self.orderedX, self.orderedY, self.orderedQ, self.orderedATT1, self.orderedATT2
