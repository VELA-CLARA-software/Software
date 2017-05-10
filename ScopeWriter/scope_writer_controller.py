from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QObject
import threading
import sys
import scope_writer_threads
import VELA_CLARA_Scope_Control as vcsc
import time, numpy, epics, math, threading
import win32com.client

class scopeWriterController(QObject):

	def __init__(self, view, model, scopeCont):
		#Hardware controllers are piped in from the attCalmainApp.py
		super(scopeWriterController, self).__init__()
		self.started = False
		self.view = view
		self.model = model
		#self.logger = logger
		self.scope_writer_threads = scope_writer_threads
		self.threading = threading
		self.scopeCont = scopeCont
		self.scopeName = self.scopeCont.getScopeNames()[0]
		self.pvRoot = self.scopeCont.getScopeTraceDataStruct(self.scopeName).pvRoot
		self.started = False
		self.scope=win32com.client.Dispatch("LeCroy.XStreamDSO")
		self.scope.Measure.MeasureMode = "StdVertical"
		self.traceNames = self.scopeCont.getScopeTracePVs()
		self.numNames = self.scopeCont.getScopeNumPVs()

		self.view.addToListButton.clicked.connect(lambda: self.appendToList())
		self.view.startButton.clicked.connect(lambda: self.startLogging())
		self.view.stopButton.clicked.connect(lambda: self.stopLogging())

	def startLogging(self):
		self.started = True
		self.view.startButton.setEnabled(False)
		self.view.addToListButton.setEnabled(False)
		self.view.startButton.setText("Logging....")
		while self.started == True:
			self.threads = []
			QtGui.QApplication.processEvents()
			for channel in self.layoutWidgets( self.view.channelsVBox ):
				self.channel = self.setScopeChannel( str( channel.itemAt(1).itemAt(1).widget().currentText() ) )
				self.numChannel = self.channel[0]
				self.traceChannelPV = self.channel[1]
				self.channelStr = self.getChannelStrings( self.numChannel )
				self.channelString = self.channelStr[0]
				self.traceChannelString = self.channelStr[1]
				self.epicsPVName = str( channel.itemAt(1).itemAt(1).widget().currentText() )
				self.traceName = str(self.scopeCont.getScopeTraceDataStruct(self.scopeName).pvRoot)
				epics.caput( str( self.traceChannelString ) , self.recordChannel( self.channelString ) )
				self.measurementType = str( channel.itemAt(2).itemAt(1).widget().currentText() )
				self.filterType = str( channel.itemAt(3).itemAt(1).widget().currentText() )
				self.filterInterval = str( channel.itemAt(4).itemAt(1).widget().currentText() )
				if self.measurementType == "Area":
					self.signal = channel.itemAt(5)
					self.signalStart = int( self.signal.itemAt(1).itemAt(0).widget().toPlainText() )
					self.signalEnd = int( self.signal.itemAt(1).itemAt(2).widget().toPlainText() )				#Run threads for ATT calibration
					#self.thread = threading.Thread(target = self.readTracesAndWriteAreaToEPICS, args=(self.scopeName, self.channel, self.baselineStart, self.baselineEnd, self.signalStart, self.signalEnd, self.epicsPVName))
					#self.threads.append( self.thread )
					self.readTracesAndWriteAreaToEPICS(self.scopeName, self.traceChannelPV, self.signalStart, self.signalEnd, self.epicsPVName, self.filterType, self.filterInterval)
				elif self.measurementType == "Max":
					self.readTracesAndWriteMaxToEPICS(self.scopeName, self.traceChannelPV, self.epicsPVName, self.filterType, self.filterInterval)
				elif self.measurementType == "Min":
					self.readTracesAndWriteMinToEPICS(self.scopeName, self.traceChannelPV, self.epicsPVName, self.filterType, self.filterInterval)
				elif self.measurementType == "Peak-to-Peak":
					self.readTracesAndWriteP2PToEPICS(self.scopeName, self.traceChannelPV, self.epicsPVName, self.filterType, self.filterInterval)
				else:
					print "ERROR!!!! Invalid measurement type"

	def stopLogging(self):
		self.started = False
		self.view.startButton.setText("Start logging to EPICS")
		self.view.startButton.setEnabled(True)
		self.view.addToListButton.setEnabled(True)

	def layoutWidgets(self, layout):
		self.layout = layout
		return (self.layout.itemAt(i) for i in range(self.layout.count()))

	def setScopeChannel(self, channel):
		self.channel = channel
		if self.channel[-2:] == "P1":
			self.epicsChan = vcsc.SCOPE_PV_TYPE.P1
			self.traceChan = vcsc.SCOPE_PV_TYPE.TR1
		elif self.channel[-2:] == "P2":
			self.epicsChan = vcsc.SCOPE_PV_TYPE.P2
			self.traceChan = vcsc.SCOPE_PV_TYPE.TR2
		elif self.channel[-2:] == "P3":
			self.epicsChan = vcsc.SCOPE_PV_TYPE.P3
			self.traceChan = vcsc.SCOPE_PV_TYPE.TR3
		elif self.channel[-2:] == "P4":
			self.epicsChan = vcsc.SCOPE_PV_TYPE.P4
			self.traceChan = vcsc.SCOPE_PV_TYPE.TR4
		else:
			print "this channel isn't valid"
			self.epicsChan = vcsc.SCOPE_PV_TYPE.UNKNOWN
		return self.epicsChan, self.traceChan

	def getChannelStrings(self, channel):
		self.channel = channel
		if self.channel == vcsc.SCOPE_PV_TYPE.P1:
			self.epicsPV = self.pvRoot+str(":TR1")
			self.pvSuffix = "TR1"
		elif self.channel == vcsc.SCOPE_PV_TYPE.P2:
			self.epicsPV = self.pvRoot+str(":TR2")
			self.pvSuffix = "TR2"
		elif self.channel == vcsc.SCOPE_PV_TYPE.P3:
			self.epicsPV = self.pvRoot+str(":TR3")
			self.pvSuffix = "TR3"
		elif self.channel == vcsc.SCOPE_PV_TYPE.P4:
			self.epicsPV = self.pvRoot+str(":TR4")
			self.pvSuffix = "TR4"
		else:
			print "this channel isn't valid"
			self.epicsChan = vcsc.SCOPE_PV_TYPE.UNKNOWN
		return self.pvSuffix, self.epicsPV

	def appendToList(self):
		self.view.addChannel( self.view.TabWidget, self.view.channelsVBox, self.scopeCont )

	def recordChannel( self, channelName ):
		self.chan = []
		self.channelName = channelName
		if self.channelName == "TR1":
			self.chan = self.scope.Zoom.Z1.Out.Result.DataArray
		elif self.channelName == "TR2":
			self.chan = self.scope.Zoom.Z2.Out.Result.DataArray
		elif self.channelName == "TR3":
			self.chan = self.scope.Zoom.Z3.Out.Result.DataArray
		elif self.channelName == "TR4":
			self.chan = self.scope.Zoom.Z4.Out.Result.DataArray
		self.list = (len(self.chan),) #Appends the array size to the vector sent to EPICS so that the
		self.cha1 = list(self.list)   #scope controller can dynamically change array size when reading values
		for a in self.chan:
			self.cha1.append(a)
		return self.cha1

	def movingaverage(self, interval, window_size):
		self.window_size = window_size
		self.interval = interval
		self.window = numpy.ones(int(self.window_size))/float(self.window_size)
		return numpy.convolve(self.interval, self.window, 'same')

	def readTracesAndWriteAreaToEPICS( self, scope_name, channel_name, area_start, area_end, epics_channel, filter_type, filter_interval ):
		self.scope_name = scope_name
		self.channel_name = channel_name
		self.area_start = area_start
		self.area_end = area_end
		self.epics_channel = epics_channel
		self.filter_type = filter_type
		self.filter_interval = filter_interval

		self.numShots = 1
		self.scopeCont.monitorATraceForNShots( self.scope_name, self.channel_name, self.numShots ) # We only take 1 trace - this should allow us to capture "interesting" conditioning events
		while self.scopeCont.isMonitoringScopeTrace( self.scope_name, self.channel_name ):
			time.sleep(0.001)

		self.allTraceDataStruct = self.scopeCont.getScopeTraceDataStruct( self.scope_name ) # This is a c++ struct containing all scope trace data - see help("vcsc.scopeTraceData") in python for more info.
		self.scopeTraceData = self.allTraceDataStruct.traceData # This is a map containing a vector of vectors for each channel: 2000 points for n shots....
		self.baseline_data = []
		self.data = []
		self.part_trace_data = []
		self.partTrace = self.scopeCont.getPartOfTrace( self.scope_name, self.channel_name, self.area_start, self.area_end ) # This is a function in the .pyd library which allows the user to get a section of the trace.
		#self.noise = self.scopeCont.getAvgNoise( self.scope_name, self.channel_name, self.baseline_start, self.baseline_end) # This takes the mean value of a region with no signal on it.
		for i in range(self.numShots):
			self.part_trace_data.append( numpy.sum( self.partTrace[i] )*self.allTraceDataStruct.timebase ) # This is the "raw" trace section.
			if self.filter_type == "None":
				self.data.append( numpy.sum( self.partTrace[i] )*self.allTraceDataStruct.timebase )
			elif self.filter_type == "Moving Average":
				self.data.append( numpy.sum( self.movingaverage( self.partTrace[i], self.filter_interval ) )*self.allTraceDataStruct.timebase )
		self.mean_area = numpy.mean( self.data )*math.pow(10,9)
		print self.mean_area

		epics.caput( self.epics_channel, self.mean_area )
		time.sleep(0.1)

	def readTracesAndWriteMaxToEPICS( self, scope_name, channel_name, epics_channel, filter_type, filter_interval ):
		self.scope_name = scope_name
		self.channel_name = channel_name
		self.epics_channel = epics_channel
		self.filter_type = filter_type
		self.filter_interval = filter_interval

		self.numShots = 1
		self.scopeCont.monitorATraceForNShots( self.scope_name, self.channel_name, self.numShots ) # We only take 1 trace - this should allow us to capture "interesting" conditioning events
		while self.scopeCont.isMonitoringScopeTrace( self.scope_name, self.channel_name ):
			time.sleep(0.01)

		self.allTraceDataStruct = self.scopeCont.getScopeTraceDataStruct( scope_name )
		self.scopeTraceData = self.allTraceDataStruct.traceData
		self.max = self.scopeCont.getMaxOfTraces( self.scope_name, self.channel_name )

		self.mean_max = numpy.mean( self.max ) # We need to include some calibration factors based on diagnostic type here.... more to be added

		epics.caput( self.epics_channel, self.mean_max )
		time.sleep(0.1)

	def readTracesAndWriteMinToEPICS( self, scope_name, channel_name, epics_channel, filter_type, filter_interval ):
		self.scope_name = scope_name
		self.channel_name = channel_name
		self.epics_channel = epics_channel
		self.filter_type = filter_type
		self.filter_interval = filter_interval

		self.numShots = 1
		self.scopeCont.monitorATraceForNShots( self.scope_name, self.channel_name, self.numShots ) # We only take 1 trace - this should allow us to capture "interesting" conditioning events
		while self.scopeCont.isMonitoringScopeTrace( self.scope_name, self.channel_name ):
			time.sleep(0.01)

		self.allTraceDataStruct = self.scopeCont.getScopeTraceDataStruct( scope_name )
		self.scopeTraceData = self.allTraceDataStruct.traceData
		self.min = self.scopeCont.getMinOfTraces( self.scope_name, self.channel_name )

		self.mean_max = numpy.mean( self.min ) # We need to include some calibration factors based on diagnostic type here.... more to be added

		epics.caput( self.epics_channel, self.mean_min )
		time.sleep(0.1)

	def readTracesAndWriteP2PToEPICS( self, scope_name, channel_name, epics_channel, filter_type, filter_interval ):
		self.scope_name = scope_name
		self.channel_name = channel_name
		self.epics_channel = epics_channel
		self.filter_type = filter_type
		self.filter_interval = filter_interval

		self.numShots = 1
		self.scopeCont.monitorATraceForNShots( self.scope_name, self.channel_name, self.numShots ) # We only take 1 trace - this should allow us to capture "interesting" conditioning events
		while self.scopeCont.isMonitoringScopeTrace( self.scope_name, self.channel_name ):
			time.sleep(0.01)

		self.allTraceDataStruct = self.scopeCont.getScopeTraceDataStruct( scope_name )
		self.scopeTraceData = self.allTraceDataStruct.traceData
		self.min = self.scopeCont.getMinOfTraces( self.scope_name, self.channel_name )
		self.max = self.scopeCont.getMaxOfTraces( self.scope_name, self.channel_name )
		self.p2p = []
		for i in range(len(self.min)):
			self.p2p.append( ( self.max[ i ] - self.min[ i ] ) )

		self.mean_p2p = numpy.mean( self.p2p ) # We need to include some calibration factors based on diagnostic type here.... more to be added

		epics.caput( self.epics_channel, self.mean_p2p )
		time.sleep(0.1)
