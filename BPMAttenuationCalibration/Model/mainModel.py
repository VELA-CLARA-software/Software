import epics
import random
import os,sys
import time
import numpy
sys.path.append('D:\\VELA-CLARA_software\\VELA-CLARA-Controllers\\Controllers\\VELA\\INJECTOR\\velaINJBeamPositionMonitors\\bin\\Release')
sys.path.append('D:\\VELA-CLARA_software\\VELA-CLARA-Controllers\\Controllers\\VELA\\GENERIC\\velaChargeScope\\bin\\Release')

import velaINJBeamPositionMonitorControl as vbpmc
import velaChargeScopeControl as vcsc

class Model():
	def __init__(self):
		self.bpmController = vbpmc.velaINJBeamPositionMonitorController(False,False,False)
		self.scopeController = vcsc.velaChargeScopeController(False,False,False)
		self.bpmList = []

	def scanAttenuation(self, pvName, numShots, sliderMin, sliderMax):
		self.pvName = pvName
		self.numShots = int(numShots)
		self.sliderMin = int(sliderMin)
		self.sliderMax = int(sliderMax)

		self.U11 = [[[] for i in range(self.numShots)] for i in range(self.sliderMax)]#511]
		self.U12 = [[[] for i in range(self.numShots)] for i in range(self.sliderMax)]#511]
		self.U13 = [[[] for i in range(self.numShots)] for i in range(self.sliderMax)]#511]
		self.U14 = [[[] for i in range(self.numShots)] for i in range(self.sliderMax)]#511]
		self.U21 = [[[] for i in range(self.numShots)] for i in range(self.sliderMax)]#511]
		self.U22 = [[[] for i in range(self.numShots)] for i in range(self.sliderMax)]#511]
		self.U23 = [[[] for i in range(self.numShots)] for i in range(self.sliderMax)]#511]
		self.U24 = [[[] for i in range(self.numShots)] for i in range(self.sliderMax)]#511]
		#self.U11 = [[]]
		#self.U12 = [[]]
		#self.U14 = [[]]
		#self.U21 = [[]]
		#self.U22 = [[]]
		#self.U24 = [[]]
		self.rawDataMeanV11 = {}
		self.rawDataMeanV12 = {}
		self.rawDataMeanV21 = {}
		self.rawDataMeanV22 = {}
		#self.V11V12sum = [[] for i in range(self.sliderMax)]
		#self.V21V22sum = [[] for i in range(self.sliderMax)]
		self.V11V12sum = {}
		self.V21V22sum = {}
		self.dataSA1 = []
		self.dataSA2 = []
		for i in range(self.sliderMin, self.sliderMax):
			self.bpmController.setSA1(str(self.pvName), i)
			self.bpmController.setSA2(str(self.pvName), i)
			self.bpmController.monitorDataForNShots(long(self.numShots), self.pvName)
			while self.bpmController.isMonitoringBPMData(self.pvName):
				time.sleep(0.5)
			for j in range(0, self.numShots):
				self.bpmData = self.bpmController.getBPMRawData(self.pvName)
				self.U11[i][j] = self.bpmData[j][1]
				self.U12[i][j] = self.bpmData[j][2]
				self.U14[i][j] = self.bpmData[j][4]
				self.U21[i][j] = self.bpmData[j][5]
				self.U22[i][j] = self.bpmData[j][6]
				self.U24[i][j] = self.bpmData[j][8]

				print self.U11[i][j],"  ",self.U12[i][j],"  ",self.U21[i][j],"  ",self.U22[i][j]
			self.rawDataMeanV11[i] = abs( numpy.mean( self.U11[i] ) - numpy.mean( self.U14[i]  ) )
			self.rawDataMeanV12[i] = abs( numpy.mean( self.U12[i] ) - numpy.mean( self.U14[i]  ) )
			self.rawDataMeanV21[i] = abs( numpy.mean( self.U21[i] ) - numpy.mean( self.U24[i]  ) )
			self.rawDataMeanV22[i] = abs( numpy.mean( self.U22[i] ) - numpy.mean( self.U24[i]  ) )
			self.V11V12sum[i] = ( ( self.rawDataMeanV11[i] + self.rawDataMeanV12[i] ) / 2 )
			self.V21V22sum[i] = ( ( self.rawDataMeanV21[i] + self.rawDataMeanV22[i] ) / 2 )
			self.dataSA1.append( i )
			self.dataSA2.append( i )


		self.remove = 0
		while self.remove < self.sliderMin:
			self.U11.pop(0)
			self.U12.pop(0)
			self.U14.pop(0)
			self.U21.pop(0)
			self.U22.pop(0)
			self.U24.pop(0)
			#self.V11V12sum.pop(0)
			#self.V21V22sum.pop(0)
			self.dataSA1.pop(0)
			self.dataSA2.pop(0)
			self.remove = self.remove + 1
			if self.remove == self.sliderMin:
				break

		print self.V11V12sum, self.dataSA1

		return self.V11V12sum, self.V21V22sum, self.dataSA1, self.dataSA2

	def findNearest(self, dict, value):
		self.vals = numpy.array( dict.values() )
		self.keys = numpy.array( dict.keys() )
		self.idx = numpy.abs( self.vals - value).argmin()
		return ( self.keys[ self.idx  ], self.vals[ self.idx ] )

	def setAttenuation(self, pvName, v1cal, v2cal):
		self.pvName = pvName
		self.v1cal = v1cal
		self.v2cal = v2cal
		self.att1Cal = self.findNearest( self.v1cal, 1.0 )
		self.att2Cal = self.findNearest( self.v2cal, 1.0 )

		with open( str( self.pvName ), "w" ) as text_file:
			text_file.write( str( self.att1Cal[ 0 ] ) )
			text_file.write( "\n" )
			text_file.write( str( self.att2Cal[ 0 ] ) )
			text_file.write( "\n" )
			text_file.write( str( self.att1Cal[ 1 ] ) )
			text_file.write( "\n" )
			text_file.write( str( self.att2Cal[ 1 ] ) )
			text_file.write( "\n" )
			text_file.write( str( self.scopeController.getWCMQ() ) )
		self.bpmController.setSA1( self.pvName, self.att1Cal[ 0 ] )
		self.bpmController.setSA2( self.pvName, self.att2Cal[ 0 ] )
		print 'Setting SA1 = ', self.att1Cal[ 0 ]
		print 'Setting SA2 = ', self.att2Cal[ 0 ]
		return self.att1Cal[0], self.att1Cal[1], self.att2Cal[0], self.att2Cal[1]

	def getBPMReadAttenuation(self, pvName):
		self.pvName = pvName
		self.bpmRA1 = self.bpmController.getRA1(self.pvName)
		self.bpmRA2 = self.bpmController.getRA2(self.pvName)
		return self.bpmRA1, self.bpmRA2
