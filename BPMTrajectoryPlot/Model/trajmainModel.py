import time
import numpy
import collections

class trajModel():
	def __init__(self, bpmCont, scopeCont):
		self.bpmCont = bpmCont
		self.scopeCont = scopeCont
		self.bpmList = []
		self.velaInjList = []
		#These can be added to when the time comes
		self.velaInjList.append('BPM01')
		self.velaInjList.append('BPM02')
		self.velaInjList.append('BPM04')
		self.velaInjList.append('BPM05')
		self.velaInjList.append('BPM06')
		self.velaSP1List = []
		self.velaSP1List.append('BPM01')
		self.velaSP1List.append('BPM02')
		self.velaSP1List.append('BPM03')
		self.velaBA1List = []
		self.velaBA1List.append('BA1-BPM01')
		self.velaBA1List.append('BA1-BPM02')
		self.velaBA1List.append('BA1-BPM03')
		self.velaBA1List.append('BA1-BPM04')

	def monitorBPMs(self, pvList, numShots):
		self.pvList = pvList
		self.numShots = numShots
		#BPM X, Y and Q data is keyed by PV name
		self.bpmXData = {name:[] for name in self.pvList}
		self.bpmYData = {name:[] for name in self.pvList}
		self.bpmQData = {name:[] for name in self.pvList}
		#This is not currently implemented - it will allow averaging of data. This can be used instead if people want
		if self.numShots > 1:
			self.bpmCont.monitorMultipleDataForNShots(long(self.numShots), self.pvList)
			for i in self.pvList:
				while self.bpmCont.isMonitoringBPMData(str(i)):
					time.sleep(0.01)
			for i in self.pvList:
				self.bpmXData[i] = numpy.mean(self.bpmCont.getBPMXVec(i))
				self.bpmYData[i] = numpy.mean(self.bpmCont.getBPMYVec(i))
				self.bpmQData[i] = numpy.mean(self.bpmCont.getBPMQVec(i))
			self.orderedX = collections.OrderedDict((name, self.bpmXData[name]) for name in self.pvList)
			self.orderedY = collections.OrderedDict((name, self.bpmYData[name]) for name in self.pvList)
			self.orderedQ = collections.OrderedDict((name, self.bpmQData[name]) for name in self.pvList)

		#The default setting is shot-to-shot data
		elif self.numShots == 1:
			for i in self.pvList:
				#This is a function in the BPM hardware controller containing a struct with all the relevant data
				self.data = self.bpmCont.getAllBPMData(i)
				self.bpmXData[i] = self.data.x[0]
				self.bpmYData[i] = self.data.y[0]
				self.bpmQData[i] = self.data.q[0]
			#OrderedDict allows correct keying in dictionaries
			self.orderedX = collections.OrderedDict((name, self.bpmXData[name]) for name in self.pvList)
			self.orderedY = collections.OrderedDict((name, self.bpmYData[name]) for name in self.pvList)
			self.orderedQ = collections.OrderedDict((name, self.bpmQData[name]) for name in self.pvList)
			#time.sleep(0.1)
		return self.orderedX, self.orderedY, self.orderedQ
