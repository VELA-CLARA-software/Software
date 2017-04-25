import epics, time, math, numpy, sys
from PyQt4 import QtGui
import VELA_CLARA_Scope_Control as vcsc

class scopeWriterModel():
	def __init__(self, scopeCont):
		#Hardware controllers are imported from scope_writer_main.py
		self.scopeController = scopeCont
		#self.scope=win32com.client.Dispatch("LeCroy.XStreamDSO")

		#self.scope.Measure.MeasureMode = "StdVertical"
		print 'This script is logging charge measurements to EPICS - do not close!'

		self.n = 0;
		self.totaltime = 0;
		self.traceNames = self.scopeController.getScopeTracePVs()
		self.numNames = self.scopeController.getScopeNumPVs()

	def readTracesAndWriteAreaToEPICS( self, scope_name, channel_name, baseline_start, baseline_end, area_start, area_end, epics_channel ):
		self.scope_name = scope_name
		self.channel_name = channel_name
		self.baseline_start = baseline_start
		self.baseline_end = baseline_end
		self.area_start = area_start
		self.area_end = area_end
		self.epics_channel = epics_channel
		self.numShots = 1
		print self.scope_name
		print self.channel_name
		self.scopeController.monitorATraceForNShots( self.scope_name, self.channel_name, self.numShots ) # We only take 1 trace - this should allow us to capture "interesting" conditioning events
		while self.scopeController.isMonitoringScopeTrace( self.scope_name, self.channel_name ):
			time.sleep(0.1)

		self.allTraceDataStruct = self.scopeController.getScopeTraceDataStruct( self.scope_name ) # This is a c++ struct containing all scope trace data - see help("vcsc.scopeTraceData") in python for more info.
		self.scopeTraceData = self.allTraceDataStruct.traceData # This is a map containing a vector of vectors for each channel: 2000 points for n shots....
		self.baseline_data = []
		self.data = []
		self.part_trace_data = []
		self.partTrace = self.scopeController.getPartOfTrace( self.scope_name, self.channel_name, self.area_start, self.area_end ) # This is a function in the .pyd library which allows the user to get a section of the trace.
		self.noise = self.scopeController.getAvgNoise( self.scope_name, self.channel_name, self.baseline_start, self.baseline_end) # This takes the mean value of a region with no signal on it.
		for i in range(self.numShots):
			self.part_trace_data.append( numpy.sum( self.partTrace[i] )*self.allTraceDataStruct.timebase ) # This is the "raw" trace section.
			for j in range( len( self.partTrace[ i ] ) ):
				self.partTrace[i][j] = self.partTrace[i][j]-self.noise[i] # Here we subtract the average noise from each point in the trace section - this is what we want.
			self.data.append( numpy.sum( self.partTrace[i] )*self.allTraceDataStruct.timebase ) # We integrate the scope trace.

		self.mean_baseline_area = numpy.mean( self.noise )
		self.mean_trace_data = numpy.mean( self.part_trace_data )
		self.mean_area = numpy.mean( self.data )*math.pow(10,9)
		print self.mean_area

		epics.caput( self.epics_channel, self.mean_area )
		time.sleep(0.1)

	def readTracesAndWriteMaxToEPICS( self, scope_name, channel_name, epics_channel ):
		self.scope_name = scope_name
		self.channel_name = channel_name
		self.epics_channel = epics_channel

		self.numShots = 1
		self.scopeController.monitorTracesForNShots( self.numShots )
		#while self.scopeController.isMonitoringScopeTrace( self.scope_name, self.channel_name ):
		#	time.sleep(0.01)

		self.allTraceDataStruct = self.scopeController.getScopeTraceDataStruct( scope_name )
		self.scopeTraceData = self.allTraceDataStruct.traceData
		self.max = self.scopeController.getMaxOfTraces( self.scope_name, self.channel_name )

		self.mean_max = numpy.mean( self.max ) # We need to include some calibration factors based on diagnostic type here.... more to be added

		epics.caput( self.epics_channel, self.mean_max )
		time.sleep(0.1)

	def readTracesAndWriteMinToEPICS( self, scope_name, channel_name, epics_channel ):
		self.scope_name = scope_name
		self.channel_name = channel_name
		self.epics_channel = epics_channel

		self.numShots = 1
		self.scopeController.monitorTracesForNShots( self.numShots )
		#while self.scopeController.isMonitoringScopeTrace( self.scope_name, self.channel_name ):
		#	time.sleep(0.01)

		self.allTraceDataStruct = self.scopeController.getScopeTraceDataStruct( scope_name )
		self.scopeTraceData = self.allTraceDataStruct.traceData
		self.min = self.scopeController.getMinOfTraces( self.scope_name, self.channel_name )

		self.mean_max = numpy.mean( self.min ) # We need to include some calibration factors based on diagnostic type here.... more to be added

		epics.caput( self.epics_channel, self.mean_min )
		time.sleep(0.1)

	def readTracesAndWriteP2PToEPICS( self, scope_name, channel_name, epics_channel ):
		self.scope_name = scope_name
		self.channel_name = channel_name
		self.epics_channel = epics_channel

		self.numShots = 1
		self.scopeController.monitorTracesForNShots( self.numShots )
		#while self.scopeController.isMonitoringScopeTrace( self.scope_name, self.channel_name ):
		#	time.sleep(0.01)

		self.allTraceDataStruct = self.scopeController.getScopeTraceDataStruct( scope_name )
		self.scopeTraceData = self.allTraceDataStruct.traceData
		self.min = self.scopeController.getMinOfTraces( self.scope_name, self.channel_name )
		self.max = self.scopeController.getMaxOfTraces( self.scope_name, self.channel_name )
		self.p2p = []
		for i in range(len(self.min)):
			self.p2p.append( ( self.max[ i ] - self.min[ i ] ) )

		self.mean_p2p = numpy.mean( self.p2p ) # We need to include some calibration factors based on diagnostic type here.... more to be added

		epics.caput( self.epics_channel, self.mean_p2p )
		time.sleep(0.1)

	def getChannelName(self, channel_name):
		self.channel_name = channel_name
		if self.channel_name == "TR1":
			self.pvType = vcsc.SCOPE_PV_TYPE.TR1
		elif self.channel_name == "TR2":
			self.pvType = vcsc.SCOPE_PV_TYPE.TR2
		elif self.channel_name == "TR3":
			self.pvType = vcsc.SCOPE_PV_TYPE.TR3
		elif self.channel_name == "TR4":
			self.pvType = vcsc.SCOPE_PV_TYPE.TR4
		else:
			self.pvType = vcsc.SCOPE_PV_TYPE.UNKNOWN
		return self.pvType

	def writeToEPICS( self, trN ):
		epics.caput( self.traceNames[ trN - 1 ], self.recordChannel( trN, wfType ) )

	def writeDiagType( self, chanName, type ):
		self.descName = "."
		self.both = ( chanName, "DESC" )
		epics.caput( self.descName.join( self.both ), type )

	def recordChannel( self, trNum ):
		self.chan = 0
		if trNum == 1:
			self.chan = self.scope.Zoom.Z1.Out.Result.DataArray
		elif trNum == 2:
			self.chan = self.scope.Zoom.Z2.Out.Result.DataArray
		elif trNum == 3:
			self.chan = self.scope.Zoom.Z3.Out.Result.DataArray
		elif trNum == 4:
			self.chan = self.scope.Zoom.Z4.Out.Result.DataArray
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
