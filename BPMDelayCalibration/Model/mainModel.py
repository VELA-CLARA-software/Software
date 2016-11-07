import epics
import random
import os,sys
import time
import numpy
sys.path.append('D:\\VELA-CLARA_software\\VELA-CLARA-Controllers\\Controllers\\VELA\\INJECTOR\\velaINJBeamPositionMonitors\\bin\\Release')
#sys.path.append('D:\\VELA-CLARA-Controllers-master\\VELA-CLARA-Controllers\\Controllers\\VELA\\GENERIC\\velaChargeScope\\bin\\Release')

import velaINJBeamPositionMonitorControl as vbpmc
#import velaChargeScopeControl as vcsc
class Model():
	def __init__(self):
		self.bpmController = vbpmc.velaINJBeamPositionMonitorController(False,False,False)
		#self.scopeController = vcsc.velaChargeScopeController(False,False,False)
		self.bpmList = []

	def scanDLY1(self, pvName, numShots, sliderMin, sliderMax):
		self.pvName = pvName
		self.numShots = int(numShots)
		self.sliderMin = int(sliderMin)
		self.sliderMax = int(sliderMax)

		self.U11 = [[[] for i in range(self.numShots)] for i in range(self.sliderMax)]#511]
		self.U12 = [[[] for i in range(self.numShots)] for i in range(self.sliderMax)]#511]
		self.U21 = [[[] for i in range(self.numShots)] for i in range(self.sliderMax)]#511]
		self.U22 = [[[] for i in range(self.numShots)] for i in range(self.sliderMax)]#511]
		self.DV1 = [[[] for i in range(self.numShots)] for i in range(self.sliderMax)]#511]
		self.DV2 = [[[] for i in range(self.numShots)] for i in range(self.sliderMax)]#511]
		self.RD1 = []
		for i in range(self.sliderMin, self.sliderMax):
			self.bpmController.setSD1(str(self.pvName), i)
			self.bpmController.monitorDataForNShots(long(self.numShots), self.pvName)
			while self.bpmController.isMonitoringBPMData(self.pvName):
				time.sleep(0.5)
			for j in range(0, self.numShots):
				self.bpmData = self.bpmController.getBPMRawData(self.pvName)
				self.U11[i][j] = self.bpmData[j][1]
				self.U12[i][j] = self.bpmData[j][2]
				self.U21[i][j] = self.bpmData[j][5]
				self.U22[i][j] = self.bpmData[j][6]
				print self.U11[i][j],"  ",self.U12[i][j],"  ",self.U21[i][j],"  ",self.U22[i][j]
				#if not self.U11[i][j] == 0 or not self.U12[i][j] == 0 or not self.U21[i][j] == 0 or not self.U22[i][j] == 0:
				self.DV1[i][j] = (2*self.U11[i][j])/(self.U21[i][j] + self.U22[i][j])
				self.DV2[i][j] = (2*self.U12[i][j])/(self.U21[i][j] + self.U22[i][j])
				print j,'         ',i
			self.RD1.append(self.bpmController.getRD1(self.pvName))
		self.remove = 0
		while self.remove < self.sliderMin:
			self.U11.pop(0)
			self.U12.pop(0)
			self.U21.pop(0)
			self.U22.pop(0)
			self.DV1.pop(0)
			self.DV2.pop(0)
			self.remove = self.remove + 1
			if self.remove == self.sliderMin:
				break
		return self.U11, self.U12, self.U21, self.U22, self.DV1, self.DV2, self.RD1

	def setMinDLY1(self, pvName, dv1, dv2):
		self.pvName = pvName
		self.dv1 = dv1
		self.dv2 = dv2
		self.dv1Mean = []
		self.dv2Mean = []
		for i, j in zip(self.dv1, self.dv2):
			self.dv1Mean.append(numpy.mean(i))
			self.dv2Mean.append(numpy.mean(j))
			print numpy.mean(i)
		self.dv1MinVal = min(self.dv1Mean)
		self.dv2MinVal = min(self.dv2Mean)
		self.newDLY1 = int(numpy.mean(self.dv1MinVal + self.dv2MinVal))
		self.bpmController.setSD1(str(self.pvName), long(self.newDLY1))
		return self.newDLY1

	def scanDLY2(self, pvName, numShots):
		self.pvName = pvName
		self.numShots = int(numShots)
		self.U11 = [[[] for i in range(self.numShots)] for i in range(41)]#511]
		self.U12 = [[[] for i in range(self.numShots)] for i in range(41)]#511]
		self.U21 = [[[] for i in range(self.numShots)] for i in range(41)]#511]
		self.U22 = [[[] for i in range(self.numShots)] for i in range(41)]#511]
		self.DV1 = [[[] for i in range(self.numShots)] for i in range(41)]#511]
		self.DV2 = [[[] for i in range(self.numShots)] for i in range(41)]#511]
		self.RD2 = [0]
		self.bpmRD1 = self.bpmController.getRD1(self.pvName)

		for i in range(self.bpmRD1 - 20, self.bpmRD1 + 20):
			self.bpmController.setSD2(str(self.pvName), i)
			self.bpmController.monitorDataForNShots(long(self.numShots), str(self.pvName))
			while self.bpmController.isMonitoringBPMData(str(self.pvName)):
				time.sleep(0.01)
			for j in range(0, self.numShots):
				self.bpmData = self.bpmController.getBPMRawData(self.pvName)
				self.U11[i][j] = self.bpmData[j][1]
				self.U12[i][j] = self.bpmData[j][2]
				self.U21[i][j] = self.bpmData[j][5]
				self.U22[i][j] = self.bpmData[j][6]
				print self.U11[i][j],"  ",self.U12[i][j],"  ",self.U21[i][j],"  ",self.U22[i][j]
				self.DV1[i][j] = (2*self.U21[i][j])/(self.U11[i][j] + self.U12[i][j])
				self.DV2[i][j] = (2*self.U22[i][j])/(self.U11[i][j] + self.U12[i][j])
				print j,'         ',i

			self.RD2.append(self.bpmController.getRD2(self.pvName))

		return self.U11, self.U12, self.U21, self.U22, self.DV1, self.DV2, self.RD2

	def setMinDLY2(self, pvName, dv1, dv2):
		self.pvName = pvName
		self.dv1 = dv1
		self.dv2 = dv2
		self.dv1Mean = []
		self.dv2Mean = []
		for i, j in zip(self.dv1, self.dv2):
			self.dv1Mean.append(numpy.mean(i))
			self.dv2Mean.append(numpy.mean(j))
		self.dv1MinVal = min(self.dv1Mean)
		self.dv2MinVal = min(self.dv2Mean)
		self.newDLY2 = int(numpy.mean(self.dv1MinVal + self.dv2MinVal))
		self.bpmController.setSD2(str(self.pvName), long(self.newDLY2))
		return self.newDLY2

	def getBPMReadDLY(self, pvName):
		self.pvName = pvName
		self.bpmRD1 = self.bpmController.getRD1(self.pvName)
		self.bpmRD2 = self.bpmController.getRD2(self.pvName)
		return self.bpmRD1, self.bpmRD2
