from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QObject
import sys,scopeWriterGlobals
import VELA_CLARA_Scope_Control as vcsc
import time, numpy, epics, math, threading
import win32com.client
import scope_writer_logger

class scopeWriterController(QObject):
    def __init__(self, view, scopeCont, loadView, saveView):
        #Hardware controllers are piped in from the attCalmainApp.py
        super(scopeWriterController, self).__init__()
        self.started = False
        self.view = view
        self.loadView = loadView
        self.saveView = saveView
        self.threading = threading
        self.scopeCont = scopeCont
        self.data_logger = scope_writer_logger.data_logger()
        self.scopeName = self.scopeCont.getScopeNames()
        self.pvRoot = self.scopeCont.getScopeTraceDataStruct(self.scopeName[0]).pvRoot
        self.started = False
        # self.scope=win32com.client.Dispatch("LeCroy.XStreamDSO")
        # self.scope.Measure.MeasureMode = "StdVertical"
        self.traceNames = self.scopeCont.getScopeTracePVs()
        self.numNames = self.scopeCont.getScopeNumPVs()
        self.appendToList()
        self.scope=1
        #self.loadView.selectButton.clicked.connect(self.handle_fileLoadSelect)
        #self.saveView.saveNowButton_2.clicked.connect(self.handle_fileSave)
        #self.loadView.fileName.connect(self.handlefilenameUpdated)
        #self.saveView.fileName.connect(self.handlefilenameUpdated)
        self.view.addToListButton.clicked.connect(self.appendToList)
        self.view.startButton.clicked.connect(self.startLogging)
        self.view.stopButton.clicked.connect(self.stopLogging)
        # self.view.ui_btn.clicked.connect(self.browse)
        # self.view.saveButton.clicked.connect(self.handle_fileSave)
        # self.view.loadButton.clicked.connect(self.handle_fileLoadSelect)
        self.view.clearLayoutButton.clicked.connect(self.clearLayout)
        self.view.setTimebaseButton.clicked.connect(self.setTimebase)
        self.view.clearLayoutButton.setEnabled(False)


    @QtCore.pyqtSlot()
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
                self.traceName = str(self.scopeCont.getScopeTraceDataStruct(self.scopeName[0]).pvRoot)
                epics.caput( str( self.traceChannelString ) , self.recordChannel( self.channelString ) )
                self.measurementType = str( channel.itemAt(2).itemAt(1).widget().currentText() )
                self.filterType = str( channel.itemAt(3).itemAt(1).widget().currentText() )
                self.filterInterval = str( channel.itemAt(4).itemAt(1).widget().toPlainText() )
                if self.measurementType == "Area":
                    self.signal = channel.itemAt(5)
                    self.signalStart = int( self.signal.itemAt(1).itemAt(0).widget().toPlainText() )
                    self.signalEnd = int( self.signal.itemAt(1).itemAt(2).widget().toPlainText() )
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

    @QtCore.pyqtSlot()
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

    @QtCore.pyqtSlot()
    def appendToList(self):
        self.view.clearLayoutButton.setEnabled(True)
        self.view.addChannel( self.view.channelsVBox, self.scopeCont )

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
        self.view.traceSizeLabel.setText(str(len(self.chan)))
        if len(self.chan) > 2002:
            self.view.traceWarningLabel.setText("WARNING!!!! \nTrace size > 2002!!!")
        else:
            self.view.traceWarningLabel.setText("")
        return self.cha1

    def movingaverage(self, interval, window_size):
        self.window_size = window_size
        self.interval = interval
        self.window = numpy.ones(int(self.window_size))/float(self.window_size)
        return numpy.convolve(self.interval, self.window, 'same')

    def readTracesAndWriteAreaToEPICS( self, scope_names, channel_name, area_start, area_end, epics_channel, filter_type, filter_interval ):
        self.wvf_name = scope_names[0]
        self.scop_name = scope_names[1]
        self.channel_name = channel_name
        self.area_start = area_start
        self.area_end = area_end
        self.noise_start = 0
        self.noise_end = 100
        self.epics_channel = epics_channel
        self.filter_type = filter_type
        self.filter_interval = filter_interval

        self.numShots = 1
        # We only take 1 trace - this should allow us to capture "interesting" events
        # This is a c++ struct containing all scope trace data - see help("vcsc.scopeTraceData") in python for more info.
        self.allTraceDataStruct = self.scopeCont.getScopeTraceDataStruct( self.wvf_name )
        self.allNumDataStruct = self.scopeCont.getScopeNumDataStruct( self.scop_name )
        # This is a map containing a vector of vectors for each channel: 2000 points for n shots....
        self.scopeTraceData = self.allTraceDataStruct.traceData
        self.baseline_data = []
        self.data = []
        self.part_trace_data = []
        # This is a function in the .pyd library which allows the user to get a section of the trace.
        self.partTrace = self.scopeCont.getPartOfTrace( self.wvf_name, self.channel_name, self.area_start, self.area_end )
        self.partNoiseTrace = self.scopeCont.getPartOfTrace( self.wvf_name, self.channel_name, self.noise_start, self.noise_end )
        self.noise = self.scopeCont.getAvgNoise( self.wvf_name, self.channel_name, self.noise_start, self.noise_end) # This takes the mean value of a region with no signal on it.
        for i in range(self.numShots):
            self.part_trace_data.append( numpy.sum( self.partTrace[i] )*self.allTraceDataStruct.timebase ) # This is the "raw" trace section.
            if self.filter_type == "None":
                self.data.append( numpy.sum( self.partTrace[i] )*self.allTraceDataStruct.timebase )
            elif self.filter_type == "Moving Average":
                self.data.append( numpy.sum( self.movingaverage( self.partTrace[i], self.filter_interval ) )*self.allTraceDataStruct.timebase )
            elif self.filter_type == "Baseline Subtraction":
                self.partNoiseSub = []
                for j in self.partTrace[i]:
                    self.partNoiseSub.append(j - self.noise[i])
                self.data.append( numpy.sum( self.partNoiseSub )*self.allTraceDataStruct.timebase )
        self.mean_area = numpy.mean( self.data )*math.pow(10,12)
        # print self.mean_area
        epics.caput( self.epics_channel, self.mean_area )

    def readTracesAndWriteMaxToEPICS( self, scope_names, channel_name, epics_channel, filter_type, filter_interval ):
        self.wvf_name = scope_names[0]
        self.scop_name = scope_names[1]
        self.channel_name = channel_name
        self.epics_channel = epics_channel
        self.filter_type = filter_type
        self.filter_interval = filter_interval

        self.numShots = 1
        # self.scopeCont.monitorATraceForNShots( self.wvf_name, self.channel_name, self.numShots )
        # while self.scopeCont.isMonitoringScopeTrace( self.wvf_name, self.channel_name ):
            # time.sleep(0.01)

        self.allTraceDataStruct = self.scopeCont.getScopeTraceDataStruct( self.wvf_name )
        self.scopeTraceData = self.allTraceDataStruct.traceData
        self.max = self.scopeCont.getMaxOfTraces( self.wvf_name, self.channel_name )

        self.mean_max = numpy.mean( self.max ) # We need to include some calibration factors based on diagnostic type here.... more to be added

        epics.caput( self.epics_channel, self.mean_max )
        time.sleep(0.1)

    def readTracesAndWriteMinToEPICS( self, scope_names, channel_name, epics_channel, filter_type, filter_interval ):
        self.wvf_name = scope_names[0]
        self.scop_name = scope_names[1]
        self.channel_name = channel_name
        self.epics_channel = epics_channel
        self.filter_type = filter_type
        self.filter_interval = filter_interval

        self.numShots = 1
        # self.scopeCont.monitorATraceForNShots( self.wvf_name, self.channel_name, self.numShots )
        # while self.scopeCont.isMonitoringScopeTrace( self.wvf_name, self.channel_name ):
            # time.sleep(0.01)

        self.allTraceDataStruct = self.scopeCont.getScopeTraceDataStruct( self.wvf_name )
        self.scopeTraceData = self.allTraceDataStruct.traceData
        self.min = self.scopeCont.getMinOfTraces( self.wvf_name, self.channel_name )

        self.mean_min = numpy.mean( self.min )

        epics.caput( self.epics_channel, self.mean_min )
        time.sleep(0.1)

    def readTracesAndWriteP2PToEPICS( self, scope_names, channel_name, epics_channel, filter_type, filter_interval ):
        self.wvf_name = scope_names[0]
        self.scop_name = scope_names[1]
        self.channel_name = channel_name
        self.epics_channel = epics_channel
        self.filter_type = filter_type
        self.filter_interval = filter_interval

        self.numShots = 1
        # self.scopeCont.monitorATraceForNShots( self.wvf_name, self.channel_name, self.numShots )
        # while self.scopeCont.isMonitoringScopeTrace( self.wvf_name, self.channel_name ):
            # time.sleep(0.01)

        self.allTraceDataStruct = self.scopeCont.getScopeTraceDataStruct( self.wvf_name )
        self.scopeTraceData = self.allTraceDataStruct.traceData
        self.min = self.scopeCont.getMinOfTraces( self.wvf_name, self.channel_name )
        self.max = self.scopeCont.getMaxOfTraces( self.wvf_name, self.channel_name )
        self.p2p = []
        for i in range(len(self.min)):
            self.p2p.append( ( self.max[ i ] - self.min[ i ] ) )

        self.mean_p2p = numpy.mean( self.p2p )

        epics.caput( self.epics_channel, self.mean_p2p )
        time.sleep(0.1)

    @QtCore.pyqtSlot()
    def setTimebase(self):
        self.timebase = float(self.view.setTimebaseTextEdit.toPlainText())
        if self.timebase is not None:
            self.scopeCont.setTimebase( self.wvf_name, self.timebase )

    @QtCore.pyqtSlot()
    def clearLayout(self):
        self.length = len(self.view.channelsLayout)
        if self.length > 1:
            self.layout = self.view.channelsLayout.takeAt(self.length - 1)
            self.chanVBox = self.layout.takeAt(0)
            self.allVBox = []
            self.allVBox.append(self.chanVBox)
            # print len(self.allVBox)
            if self.layout is not None:
                if self.layout.count():
                    for vBox in self.allVBox:
                        if vBox.count():
                            for i in range(0, vBox.count()):
                                self.vBoxItem = vBox.takeAt(i) 
                                if self.vBoxItem is not None:
                                    print i
                                    # vBox.removeItem(self.vBoxItem)
                                    self.vBoxItem.widget().hide()
                                    # vBox.removeWidget(self.vBoxItem.widget())
                                # if self.vBoxItem is not None:
                                    # self.vBoxWidget = self.vBoxItem.widget()
                                    # if self.vBoxWidget is not None:
                                        # print "aaa"
                                        # self.vBoxWidget.deleteLater()
                                    # else:
                                        # print "ddd"
                                        # self.clearLayout()
                    # self.item = self.layout.takeAt(0)
                    # self.widget = self.item.widget()
                    # if self.widget is not None:
                        # self.widget.deleteLater()
                    # else:
                        # self.clearLayout()
            # self.clearLayout()

    @QtCore.pyqtSlot()
    def handlefilenameUpdated(self,event):
        print event
        self.view.ui_line.setText(event)

    @QtCore.pyqtSlot()
    def browse(self):
        self.path = str(QtGui.QFileDialog.getOpenFileName(None, 'Select a folder:', scopeWriterGlobals.scopeSetupLocation, "Scope files (*.lss)"))
        if self.path:
            print self.path
            self.lastSlash = self.path.rfind('/')
            self.path = self.path[(self.lastSlash+1):]
            self.view.ui_line.setText(self.path)

    @QtCore.pyqtSlot()
    def saveSetup(self):
        print self.view.ui_line.text()
        self.scope.SaveRecall.Setup.PanelFilename = str(self.view.ui_line.text())
        self.scope.SaveRecall.Setup.DoSavePanel

    @QtCore.pyqtSlot()
    def loadSetup(self):
        print self.view.ui_line.text()
        self.scope.SaveRecall.Setup.PanelFilename = str(self.view.ui_line.text())
        self.scope.SaveRecall.Setup.DoRecallPanel

    @QtCore.pyqtSlot()
    def handle_loadSettings(self):
        self.loadView.show()
        self.loadView.activateWindow()

    @QtCore.pyqtSlot()
    def handle_saveSettings(self):
        self.saveView.show()
        self.saveView.activateWindow()

    @QtCore.pyqtSlot()
    def handle_fileLoadSelect(self):
        self.scope.SaveRecall.Setup.PanelFilename = str(self.view.ui_line.text())
        self.scope.SaveRecall.Setup.DoRecallPanel
        self.loadView.hide()

    @QtCore.pyqtSlot()
    def handle_fileSave(self):
        #self.name = self.saveView.setFileName()
        #self.view.ui_line.setText(self.name)
        self.scope.SaveRecall.Setup.PanelFilename = str(self.view.ui_line.text())
        self.scope.SaveRecall.Setup.DoSavePanel
        self.saveView.hide()
