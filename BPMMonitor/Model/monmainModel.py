import os,sys
import time
import numpy
import collections

class monModel():
	def __init__(self, bpmCont, scopeCont):
		#Receives scope and BPM controller from monmainApp.py
		self.bpmCont = bpmCont
		self.scopeCont = scopeCont
		self.bpmList = []
		self.velaInjList = []
		#Creates lists for each section of VELA - this will need to be expanded when CLARA arrives.
		self.velaInjList.append('BPM01')
		self.velaInjList.append('BPM02')
		self.velaInjList.append('BPM04')
		self.velaInjList.append('BPM05')
		self.velaInjList.append('BPM06')
		self.velaSP1List = []
		self.velaSP1List.append('BPM01')
		self.velaSP1List.append('BPM02')
		self.velaSP1List.append('BPM03')

	def monitorBPMs(self, pvList, numShots):
		self.pvList = pvList
		self.numShots = numShots
		#Dictionaries for X, Y, Q, Att and resolution data for each BPM are keyed by name
		self.bpmXData = {name:[] for name in self.pvList}
		self.bpmYData = {name:[] for name in self.pvList}
		self.bpmQData = {name:[] for name in self.pvList}
		self.bpmATT1Val = {name:[] for name in self.pvList}
		self.bpmATT2Val = {name:[] for name in self.pvList}
		self.bpmResolution = {name:[] for name in self.pvList}
		#This is an option for getting mean values - not currently implemented
		if self.numShots > 1:
			self.bpmCont.monitorDataForNShots(long(self.numShots), self.pvList)
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
				self.bpmResolution[i] = self.bpmCont.getBPMResolution(i)
			self.orderedX = collections.OrderedDict((name, self.bpmXData[name]) for name in self.pvList)
			self.orderedY = collections.OrderedDict((name, self.bpmYData[name]) for name in self.pvList)
			self.orderedQ = collections.OrderedDict((name, self.bpmQData[name]) for name in self.pvList)
			self.orderedATT1 = collections.OrderedDict((name, self.bpmATT1Val[name]) for name in self.pvList)
			self.orderedATT2 = collections.OrderedDict((name, self.bpmATT2Val[name]) for name in self.pvList)
			self.orderedRes = collections.OrderedDict((name, self.bpmResolution[name]) for name in self.pvList)

		#The default is to get shot-to-shot readings of all the desired numbers
		elif self.numShots == 1:
			for i in self.pvList:
				#This is a hardware controller function - all of the necessary data for each BPM is kept in a struct
				self.data = self.bpmCont.getAllBPMData(i)
				self.bpmXData[i] = self.data.pu1[0] - self.data.pu2[0]
				self.bpmYData[i] = self.data.pu3[0] - self.data.pu4[0]
				self.bpmQData[i] = self.data.q[0]
				self.bpmATT1Val[i] = self.bpmCont.getRA1(i)
				self.bpmATT2Val[i] = self.bpmCont.getRA2(i)
				self.bpmResolution[i] = self.bpmCont.getBPMResolution(i)
			#OrderedDict means that the data is keyed correctly by name
			self.orderedX = collections.OrderedDict((name, self.bpmXData[name]) for name in self.pvList)
			self.orderedY = collections.OrderedDict((name, self.bpmYData[name]) for name in self.pvList)
			self.orderedQ = collections.OrderedDict((name, self.bpmQData[name]) for name in self.pvList)
			self.orderedATT1 = collections.OrderedDict((name, self.bpmATT1Val[name]) for name in self.pvList)
			self.orderedATT2 = collections.OrderedDict((name, self.bpmATT2Val[name]) for name in self.pvList)
			self.orderedRes = collections.OrderedDict((name, self.bpmResolution[name]) for name in self.pvList)

		return self.orderedX, self.orderedY, self.orderedQ, self.orderedATT1, self.orderedATT2, self.orderedRes
