import os,sys
import time
import numpy
import collections

class attCalModel():
	def __init__(self, bpmCont, scopeCont):
		#Hardware controllers are imported from attCalmainApp.py
		self.bpmCont = bpmCont
		self.scopeCont = scopeCont
		self.bpmList = []

	def monitorBPMs(self, pvList, numShots):
		#Uses hardware controller functions to take BPM data and store in dictionaries based on PV name and ATT values
		self.pvList = pvList
		self.numShots = numShots
		self.bpmData = {name:[[] for i in range(self.numShots)] for name in self.pvList}
		self.bpmCont.monitorMultipleDataForNShots(long(self.numShots), self.pvList)
		for i in self.pvList:
			while self.bpmCont.isMonitoringBPMData(str(i)):
				time.sleep(0.01)
			self.bpmData[i] = self.bpmCont.getBPMRawData(i)
		return self.bpmData

	def scanAttenuation(self, pvList, numShots, sliderMin, sliderMax):
		#These are set by the user in the GUI and piped through
		self.pvList = pvList
		self.numShots = int(numShots)
		self.sliderMin = int(sliderMin)
		self.sliderMax = int(sliderMax)

		#Dictionaries to store the BPM raw voltages, keyed by shot, ATT value, and BPM name
		self.U11 = {name:[[[] for i in range(self.numShots)] for i in range(self.sliderMax)] for name in self.pvList}
		self.U12 = {name:[[[] for i in range(self.numShots)] for i in range(self.sliderMax)] for name in self.pvList}
		self.U13 = {name:[[[] for i in range(self.numShots)] for i in range(self.sliderMax)] for name in self.pvList}
		self.U14 = {name:[[[] for i in range(self.numShots)] for i in range(self.sliderMax)] for name in self.pvList}
		self.U21 = {name:[[[] for i in range(self.numShots)] for i in range(self.sliderMax)] for name in self.pvList}
		self.U22 = {name:[[[] for i in range(self.numShots)] for i in range(self.sliderMax)] for name in self.pvList}
		self.U23 = {name:[[[] for i in range(self.numShots)] for i in range(self.sliderMax)] for name in self.pvList}
		self.U24 = {name:[[[] for i in range(self.numShots)] for i in range(self.sliderMax)] for name in self.pvList}
		self.rawDataMeanV11 = collections.defaultdict(dict)
		self.rawDataMeanV12 = collections.defaultdict(dict)
		self.rawDataMeanV21 = collections.defaultdict(dict)
		self.rawDataMeanV22 = collections.defaultdict(dict)
		self.V11V12sum = collections.defaultdict(dict)
		self.V21V22sum = collections.defaultdict(dict)

		#See BPM software documentation for this algorithm
		for i in range(self.sliderMin, self.sliderMax):
			for h in self.pvList:
				self.bpmCont.setSA1(str(h), i)
				self.bpmCont.setSA2(str(h), i)
				print "Setting SA1 = SA2 = ", i, " for ", str(h)
				if not self.bpmCont.getRA1(str(h)) == i:
					print "ERROR!!!!!!", str(h), " RA1 not set correctly"
				elif not self.bpmCont.getRA2(str(h)) == i:
					print "ERROR!!!!!!", str(h), " RA2 not set correctly"
				else:
					pass
			self.bpmData = self.monitorBPMs(self.pvList, self.numShots)
			for h in self.pvList:
				for j in range(self.numShots):
					self.U11[h][i][j] = self.bpmData[h][j][1]
					self.U12[h][i][j] = self.bpmData[h][j][2]
					self.U14[h][i][j] = self.bpmData[h][j][4]
					self.U21[h][i][j] = self.bpmData[h][j][5]
					self.U22[h][i][j] = self.bpmData[h][j][6]
					self.U24[h][i][j] = self.bpmData[h][j][8]
					print h, "   ",self.U11[h][i][j],"  ",self.U12[h][i][j],"  ",self.U21[h][i][j],"  ",self.U22[h][i][j]
				self.rawDataMeanV11[h][i] = abs( numpy.mean( self.U11[h][i] ) - numpy.mean( self.U14[h][i]  ) )
				self.rawDataMeanV12[h][i] = abs( numpy.mean( self.U12[h][i] ) - numpy.mean( self.U14[h][i]  ) )
				self.rawDataMeanV21[h][i] = abs( numpy.mean( self.U21[h][i] ) - numpy.mean( self.U24[h][i]  ) )
				self.rawDataMeanV22[h][i] = abs( numpy.mean( self.U22[h][i] ) - numpy.mean( self.U24[h][i]  ) )
				self.V11V12sum[h][i] = ( ( self.rawDataMeanV11[h][i] + self.rawDataMeanV12[h][i] ) / 2 )
				self.V21V22sum[h][i] = ( ( self.rawDataMeanV21[h][i] + self.rawDataMeanV22[h][i] ) / 2 )

		return self.V11V12sum, self.V21V22sum

	def findNearest(self, dict, value):
		#Finds the value for V1 - V2 = 0V for both horizontal and vertical planes
		self.vals = numpy.array( dict.values() )
		self.keys = numpy.array( dict.keys() )
		self.idx = numpy.abs( self.vals - value).argmin()
		return ( self.keys[ self.idx  ], self.vals[ self.idx ] )

	def setAttenuation(self, pvList, v1cal, v2cal):
		self.att1Cal = {}
		self.att2Cal = {}
		self.v1cal = v1cal
		self.v2cal = v2cal
		for i in self.pvList:
			self.att1Cal[i] = self.findNearest( self.v1cal[i], 1.0 )
			self.att2Cal[i] = self.findNearest( self.v2cal[i], 1.0 )

			#Writes a text file with calibrated BPM attenuation values and V1,2 cal. After calibration, these values
			#can be put into the BPM hardware controller config file: \\fed.cclrc.ac.uk\Org\NLab\ASTeC\Projects\VELA\Software\Config
			with open( str( i ), "w" ) as text_file:
				text_file.write( "ATT1 Cal = "+str( self.att1Cal[i][0] ) )
				text_file.write( "\n" )
				text_file.write( "ATT2 Cal = "+str( self.att2Cal[i][0] ) )
				text_file.write( "\n" )
				text_file.write( "V1 Cal = "+str( self.att1Cal[i][1] ) )
				text_file.write( "\n" )
				text_file.write( "V2 Cal = "+str( self.att2Cal[i][1] ) )
				text_file.write( "\n" )
				text_file.write( "Q Cal = "+str( self.scopeCont.getWCMQ() ) )
			self.bpmCont.setSA1( i, self.att1Cal[i][0] )
			self.bpmCont.setSA2( i, self.att2Cal[i][0] )
			print 'Setting SA1 for ', i, ' = ', self.att1Cal[i][0]
			print 'Setting SA2 for ', i, ' = ', self.att2Cal[i][0]
		return self.att1Cal, self.att2Cal

	def getBPMReadAttenuation(self, pvName):
		self.pvName = pvName
		self.bpmRA1 = self.bpmCont.getRA1(self.pvName)
		self.bpmRA2 = self.bpmCont.getRA2(self.pvName)
		return self.bpmRA1, self.bpmRA2

	def getWCMQ(self):
		#Charge readings are currently based on WCM charge - this may not be the best option as we go further away from the gun
		self.wcmQ = self.scopeCont.getWCMQ()
		return self.wcmQ
