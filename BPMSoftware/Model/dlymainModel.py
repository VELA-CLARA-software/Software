import epics
import random
import os,sys
import time
import numpy
import collections

class dlyModel():
	def __init__(self, bpmCont):
		#Receives BPM controller from dlymainApp.py
		self.bpmCont = bpmCont
		self.bpmList = []

	def monitorBPMs(self, pvList, numShots):
		self.pvList = pvList
		self.numShots = numShots
		self.bpmData = {name:[[] for i in range(self.numShots)] for name in self.pvList}
		#Uses hardware controller functions to take BPM data and store in dictionaries based on PV name and DLY values
		self.bpmCont.monitorDataForNShots(long(self.numShots), self.pvList)
		for i in self.pvList:
			while self.bpmCont.isMonitoringBPMData(str(i)):
				time.sleep(0.01)
			self.bpmData[i] = self.bpmCont.getBPMRawData(i)
		return self.bpmData

	def scanDLY1(self, pvList, numShots, sliderMin, sliderMax):
		#These are set by the user in the GUI and piped through
		self.pvList = pvList
		self.numShots = int(numShots)
		self.sliderMin = int(sliderMin)
		self.sliderMax = int(sliderMax)

		#Dictionaries to store the BPM raw voltages, keyed by shot, DLY value, and BPM name
		self.U11 = {name:[[[] for i in range(self.numShots)] for i in range(self.sliderMax)] for name in self.pvList}
		self.U12 = {name:[[[] for i in range(self.numShots)] for i in range(self.sliderMax)] for name in self.pvList}
		self.U21 = {name:[[[] for i in range(self.numShots)] for i in range(self.sliderMax)] for name in self.pvList}
		self.U22 = {name:[[[] for i in range(self.numShots)] for i in range(self.sliderMax)] for name in self.pvList}
		self.DV1 = {name:[[[] for i in range(self.numShots)] for i in range(self.sliderMax)] for name in self.pvList}
		self.DV2 = {name:[[[] for i in range(self.numShots)] for i in range(self.sliderMax)] for name in self.pvList}
		self.RD1 = collections.defaultdict(dict)
		self.DV1Mean = collections.defaultdict(dict)
		self.DV2Mean = collections.defaultdict(dict)
		self.dv1MinVal = collections.defaultdict(dict)
		self.dv2MinVal = collections.defaultdict(dict)
		self.newDLY1 = collections.defaultdict(dict)

		#See BPM software documentation for this algorithm
		for i in range(self.sliderMin, self.sliderMax):
			for h in self.pvList:
				self.bpmCont.setSD1(str(h), i)
				print "Setting SD1=", i, " for BPM ", str(h)
				if not self.bpmCont.getRD1(str(h)) == i:
					print "ERROR!!!!!!", str(h), " SD1 not set correctly"
				else:
					pass
			self.bpmData = self.monitorBPMs(self.pvList, self.numShots)
			for h in self.pvList:
				for j in range(self.numShots):
					self.U11[h][i][j] = self.bpmData[h][j][1]
					self.U12[h][i][j] = self.bpmData[h][j][2]
					self.U21[h][i][j] = self.bpmData[h][j][5]
					self.U22[h][i][j] = self.bpmData[h][j][6]
					print h, "   ",self.U11[h][i][j],"  ",self.U12[h][i][j],"  ",self.U21[h][i][j],"  ",self.U22[h][i][j]
					self.DV1[h][i][j] = (2*self.U11[h][i][j])/(self.U21[h][i][j] + self.U22[h][i][j])
					self.DV2[h][i][j] = (2*self.U12[h][i][j])/(self.U21[h][i][j] + self.U22[h][i][j])
				self.DV1Mean[h][i] = numpy.mean(self.DV1[h][i])
				self.DV2Mean[h][i] = numpy.mean(self.DV2[h][i])
				self.RD1[h][i] = i

		for h in self.pvList:
			self.dv1MinVal[h] = min(self.DV1Mean[h])
			self.dv2MinVal[h] = min(self.DV2Mean[h])
			self.newDLY1[h] = int(numpy.mean(self.dv1MinVal[h] + self.dv2MinVal[h]))

		return self.U11, self.U12, self.U21, self.U22, self.DV1, self.DV2, self.DV1Mean, self.DV2Mean, self.RD1, self.newDLY1

	def setMinDLY1(self, pvList, newDLY1):
		self.pvList = pvList
		self.newDLY1 = newDLY1
		for h in self.pvList:
			self.bpmCont.setSD1(str(h), long(self.newDLY1[h]))
			print self.newDLY1[h]

	def scanDLY2(self, pvList, numShots, rd1):
		#Scan DLY2 based on measurement of DLY1
		self.pvList = pvList
		self.numShots = int(numShots)
		self.U11 = {name:[[[] for i in range(self.numShots)] for i in range(-20,20)] for name in self.pvList}
		self.U12 = {name:[[[] for i in range(self.numShots)] for i in range(-20,20)] for name in self.pvList}
		self.U21 = {name:[[[] for i in range(self.numShots)] for i in range(-20,20)] for name in self.pvList}
		self.U22 = {name:[[[] for i in range(self.numShots)] for i in range(-20,20)] for name in self.pvList}
		self.DV1 = {name:[[[] for i in range(self.numShots)] for i in range(-20,20)] for name in self.pvList}
		self.DV2 = {name:[[[] for i in range(self.numShots)] for i in range(-20,20)] for name in self.pvList}
		self.RD1 = rd1
		self.DV1Mean = collections.defaultdict(dict)
		self.DV2Mean = collections.defaultdict(dict)
		self.RD2 = collections.defaultdict(dict)
		self.SD2 = collections.defaultdict(dict)
		self.newDLY2 = collections.defaultdict(dict)
		self.bpmData = collections.defaultdict(dict)

		for h in self.pvList:
			print self.RD1[h]
			for i in range(self.RD1[h] - 20, self.RD1[h] + 20):
				if i >= (self.RD1[h] + 20):
					break
				for h in self.pvList:
					self.bpmCont.setSD2(str(h), i)
					print "Setting SD2=", i, " for BPM ", str(h)
					if not self.bpmCont.getRD2(str(h)) == i:
						print "ERROR!!!!!!", str(h), " SD2 not set correctly"
					else:
						pass
				self.bpmDataMon = self.monitorBPMs(self.pvList, self.numShots)
				self.bpmData[i] = self.bpmDataMon
				for h in self.pvList:
					for j in range(self.numShots):
						self.U11[h][i][j] = self.bpmData[i][h][j][1]
						self.U12[h][i][j] = self.bpmData[i][h][j][2]
						self.U21[h][i][j] = self.bpmData[i][h][j][5]
						self.U22[h][i][j] = self.bpmData[i][h][j][6]
						print h, "   ",self.U11[h][i][j],"  ",self.U12[h][i][j],"  ",self.U21[h][i][j],"  ",self.U22[h][i][j]
						self.DV1[h][i][j] = (2*self.U11[h][i][j])/(self.U21[h][i][j] + self.U22[h][i][j])
						self.DV2[h][i][j] = (2*self.U12[h][i][j])/(self.U21[h][i][j] + self.U22[h][i][j])
					self.DV1Mean[h][i] = numpy.mean(self.DV1[h][i])
					self.DV2Mean[h][i] = numpy.mean(self.DV2[h][i])
					self.RD2[h][i] = self.bpmCont.getRD2(str(h))

		for h in self.pvList:
			self.dv1MinVal[h] = min(self.DV1Mean[h])
			self.dv2MinVal[h] = min(self.DV2Mean[h])
			self.newDLY2[h] = int(numpy.mean(self.dv1MinVal[h] + self.dv2MinVal[h]))

		return self.U11, self.U12, self.U21, self.U22, self.DV1, self.DV2, self.DV1Mean, self.DV2Mean, self.RD2, self.newDLY2

	def setMinDLY2(self, pvList, newDLY2):
		self.pvList = pvList
		self.newDLY1 = newDLY2
		for h in self.pvList:
			self.bpmCont.setSD2(str(h), long(self.newDLY2[h]))
			print self.newDLY2[h]

	def getBPMReadDLY(self, pvName):
		self.pvName = pvName
		self.bpmRD1 = self.bpmCont.getRD1(self.pvName)
		self.bpmRD2 = self.bpmCont.getRD2(self.pvName)
		return self.bpmRD1, self.bpmRD2
