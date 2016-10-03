import velaChargeScopeControl as VCSC
import win32com.client
import epics
import numpy
import time
import sys

#scopeControl = VCSC.velaChargeScopeController()
#trace1 = VCSC.SCOPE_PV_TYPE.TR1
#trace2 = VCSC.SCOPE_PV_TYPE.TR2
#trace3 = VCSC.SCOPE_PV_TYPE.TR3
#trace4 = VCSC.SCOPE_PV_TYPE.TR4

class Model():
	def __init__( self ):
		print 'Model initialised.'
		self.scope=win32com.client.Dispatch("LeCroy.XStreamDSO")

		self.scope.Measure.MeasureMode = "StdVertical"
		print 'This script is logging charge measurements to EPICS - do not close!'

		self.n = 0;
		self.totaltime = 0;
		self.trace1 = "EBT-INJ-SCOPE-01:TR1"
		self.trace2 = "EBT-INJ-SCOPE-01:TR2"
		self.trace3 = "EBT-INJ-SCOPE-01:TR3"
		self.trace4 = "EBT-INJ-SCOPE-01:TR4"
		self.num1 = "EBT-INJ-SCOPE-01:P1"
		self.num2 = "EBT-INJ-SCOPE-01:P2"
		self.num3 = "EBT-INJ-SCOPE-01:P3"
		self.num4 = "EBT-INJ-SCOPE-01:P4"
		self.traceNames = [ self.trace1, self.trace2, self.trace3, self.trace4 ]
		self.numNames = [ self.num1, self.num2, self.num3, self.num4 ]

	def writeToEPICS( self, trN, wfType ):
		if wfType == "trace":
			epics.caput( self.traceNames[ trN - 1 ], self.recordChannel( trN, wfType ) )
			# elif trN == 2:
				# epics.caput( self.traceNames[ trN - 1 ], self.recordTraces( trN ) )
			# elif trN == 3:
				# epics.caput( self.traceNames[ trN - 1 ], self.recordTraces( trN ) )
			# elif trN == 4:
				# epics.caput( self.traceNames[ trN - 1 ], self.recordTraces( trN ) )
		elif wfType == "num":
			epics.caput( self.numNames[ trN - 1 ], self.recordChannel( trN, wfType ) )

	def writeDiagType( self, chanName, type ):
		self.descName = "."
		self.both = ( chanName, "DESC" )
		epics.caput( self.descName.join( self.both ), type )
					
	def recordChannel( self, trNum, wfType ):
		self.chan = 0
		if wfType == "trace":
			if trNum == 1:
				self.chan = self.scope.Zoom.Z1.Out.Result.DataArray
			elif trNum == 2:
				self.chan = self.scope.Zoom.Z2.Out.Result.DataArray
			elif trNum == 3:
				self.chan = self.scope.Zoom.Z3.Out.Result.DataArray
			elif trNum == 4:
				self.chan = self.scope.Zoom.Z4.Out.Result.DataArray
		elif wfType == "num":		
			if trNum == 1:
				self.chan = self.scope.Measure.P1.Out.Result.Value;
			elif trNum == 2:
				self.chan = self.scope.Measure.P2.Out.Result.Value;
			elif trNum == 3:
				self.chan = self.scope.Measure.P3.Out.Result.Value;
			elif trNum == 4:
				self.chan = self.scope.Measure.P4.Out.Result.Value;
		return self.chan
		
	def getAndResetScale( self, trNum ):
		self.scales = [ self.scope.Zoom.Z1.Zoom.Verscale,
						self.scope.Zoom.Z2.Zoom.Verscale,
						self.scope.Zoom.Z3.Zoom.Verscale,
						self.scope.Zoom.Z4.Zoom.Verscale ]
		# self.max = abs( max( self.recordChannel( trNum, "trace" ) ) )
		print max(self.recordChannel( 1, "trace" ))
		self.max = max(self.recordChannel( 1, "trace" ))
		for i in range( 0, len( self.scales ) ):
			# self.scale = float( self.scales[ i ] )
			if self.max > ( 0.9 * float(str(self.scales[ i ] ))):
				self.newscale = 5
				self.scales[ i ] = self.newscale
				
	def resetScale( self, trNum ):
		if trNum == 1:
			self.scale = self.scope.Acquisition.C1.Verscale
		elif trNum == 2:
			self.scale = self.scope.Acquisition.C1.Verscale
		elif trNum == 3:
			self.scale = self.scope.Acquisition.C1.Verscale
		elif trNum == 4:
			self.scale = self.scope.Acquisition.C1.Verscale
		return self.scale
		
	# def recordNums( self, numNum ): # numnumnumnum
			# if numNum == 1:
				# self.num = self.scope.Measure.P1.Out.Result.Value;
			# elif numNum == 2:
				# self.num = self.scope.Measure.P2.Out.Result.Value;
			# elif numNum == 3:
				# self.num = self.scope.Measure.P3.Out.Result.Value;
			# elif numNum == 4:
				# self.num = self.scope.Measure.P4.Out.Result.Value;
		# return self.num
