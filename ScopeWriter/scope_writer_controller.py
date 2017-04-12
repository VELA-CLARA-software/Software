from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QObject
import threading
import sys
import scope_writer_threads
import VELA_CLARA_Scope_Control as vcsc
import time, numpy, epics, math, threading
#import logging
#logger = logging.getLogger(__name__)

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
				self.epicsPVName = str( channel.itemAt(1).itemAt(1).widget().currentText() )
				self.measurementType = str( channel.itemAt(2).itemAt(1).widget().currentText() )
				if self.measurementType == "Area":
					self.baseline = channel.itemAt(3)
					self.baselineStart = int( self.baseline.itemAt(1).itemAt(0).widget().toPlainText() )
					self.baselineEnd = int( self.baseline.itemAt(1).itemAt(2).widget().toPlainText() )
					self.signal = channel.itemAt(4)
					self.signalStart = int( self.signal.itemAt(1).itemAt(0).widget().toPlainText() )
					self.signalEnd = int( self.signal.itemAt(1).itemAt(2).widget().toPlainText() )				#Run threads for ATT calibration
					#self.thread = threading.Thread(target = self.readTracesAndWriteAreaToEPICS, args=(self.scopeName, self.channel, self.baselineStart, self.baselineEnd, self.signalStart, self.signalEnd, self.epicsPVName))
					#self.threads.append( self.thread )
					self.readTracesAndWriteAreaToEPICS(self.scopeName, self.channel, self.baselineStart, self.baselineEnd, self.signalStart, self.signalEnd, self.epicsPVName)
				elif self.measurementType == "Max":
					self.readTracesAndWriteMaxToEPICS(self.scopeName, self.channel, self.epicsPVName)
				elif self.measurementType == "Min":
					self.readTracesAndWriteMinToEPICS(self.scopeName, self.channel, self.epicsPVName)
				elif self.measurementType == "Peak-to-Peak":
					self.readTracesAndWriteP2PToEPICS(self.scopeName, self.channel, self.epicsPVName)
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
			self.epicsChan = vcsc.SCOPE_PV_TYPE.TR1
			self.epicsPV = self.pvRoot+str(":P1")
		elif self.channel[-2:] == "P2":
			self.epicsChan = vcsc.SCOPE_PV_TYPE.TR2
			self.epicsPV = self.pvRoot+str(":P2")
		elif self.channel[-2:] == "P3":
			self.epicsChan = vcsc.SCOPE_PV_TYPE.TR3
			self.epicsPV = self.pvRoot+str(":P3")
		elif self.channel[-2:] == "P4":
			self.epicsChan = vcsc.SCOPE_PV_TYPE.TR4
			self.epicsPV = self.pvRoot+str(":P4")
		else:
			print "this channel isn't valid"
			self.epicsChan = vcsc.SCOPE_PV_TYPE.UNKNOWN
		return self.epicsChan

	def appendToList(self):
		self.view.addChannel( self.view.TabWidget, self.view.channelsVBox, self.scopeCont )

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
		self.scopeCont.monitorATraceForNShots( self.scope_name, self.channel_name, self.numShots ) # We only take 1 trace - this should allow us to capture "interesting" conditioning events
		while self.scopeCont.isMonitoringScopeTrace( self.scope_name, self.channel_name ):
			time.sleep(0.1)

		self.allTraceDataStruct = self.scopeCont.getScopeTraceDataStruct( self.scope_name ) # This is a c++ struct containing all scope trace data - see help("vcsc.scopeTraceData") in python for more info.
		self.scopeTraceData = self.allTraceDataStruct.traceData # This is a map containing a vector of vectors for each channel: 2000 points for n shots....
		self.baseline_data = []
		self.data = []
		self.part_trace_data = []
		self.partTrace = self.scopeCont.getPartOfTrace( self.scope_name, self.channel_name, self.area_start, self.area_end ) # This is a function in the .pyd library which allows the user to get a section of the trace.
		self.noise = self.scopeCont.getAvgNoise( self.scope_name, self.channel_name, self.baseline_start, self.baseline_end) # This takes the mean value of a region with no signal on it.
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
		self.scopeCont.monitorATraceForNShots( self.scope_name, self.channel_name, self.numShots ) # We only take 1 trace - this should allow us to capture "interesting" conditioning events
		while self.scopeCont.isMonitoringScopeTrace( self.scope_name, self.channel_name ):
			time.sleep(0.01)

		self.allTraceDataStruct = self.scopeCont.getScopeTraceDataStruct( scope_name )
		self.scopeTraceData = self.allTraceDataStruct.traceData
		self.max = self.scopeCont.getMaxOfTraces( self.scope_name, self.channel_name )

		self.mean_max = numpy.mean( self.max ) # We need to include some calibration factors based on diagnostic type here.... more to be added

		epics.caput( self.epics_channel, self.mean_max )
		time.sleep(0.1)

	def readTracesAndWriteMinToEPICS( self, scope_name, channel_name, epics_channel ):
		self.scope_name = scope_name
		self.channel_name = channel_name
		self.epics_channel = epics_channel

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

	def readTracesAndWriteP2PToEPICS( self, scope_name, channel_name, epics_channel ):
		self.scope_name = scope_name
		self.channel_name = channel_name
		self.epics_channel = epics_channel

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
