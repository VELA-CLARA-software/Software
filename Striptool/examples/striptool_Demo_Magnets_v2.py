import sys, time, os
sys.path.append("..")
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui
import pyqtgraph as pg
from pyqtgraph.dockarea import *
import striptool as striptool
import scatterPlot as scatterplot
import numpy as np
''' Load loggerWidget library (comment out if not available) '''
sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\..\\..\\loggerWidget\\')
from ConfigParser import SafeConfigParser
import loggerWidget as lw
import logging
logger = logging.getLogger(__name__)

import VELA_CLARA_MagnetControl as vmag
import VELA_CLARA_BPM_Control as vbpmc
import  VELA_CLARA_General_Monitor as vgen

import striptoolSignalTable as stable

seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}

def convert_to_seconds(s):
    return int(s[:-1]) * seconds_per_unit[s[-1]]

class timeButton(QPushButton):
    def __init__(self, mainForm):
        super(timeButton, self).__init__()
        self.__mainForm = mainForm
        self.connect(self, SIGNAL("clicked ()"), self.buttonPushed)

    def buttonPushed(self):
        # send signal to MainForm class, self.__comboID is actually row number, ind is what is selected
        self.__mainForm.emit(SIGNAL("timeButtonPushed(int)"), convert_to_seconds(str(self.text())))

class mainApp(QApplication):
    def __init__(self):
        super(mainApp, self).__init__(sys.argv)
        self.windows = []
        self.addWindow()
        sys.exit(self.exec_())

    def addWindow(self):
        ex = self.striptool_Demo_Magnets(app=self)
        self.windows.append(ex)
        ex.show()

    class striptool_Demo_Magnets(QMainWindow):
        def __init__(self, app = None, parent = None):
            # super(self.striptool_Demo_Magnets, self).__init__(parent)
            QMainWindow.__init__(self)
            self.setWindowTitle("striptool_Demo_Magnets")
            self.statusBar = QStatusBar()
            self.setStatusBar(self.statusBar)

            self.tab = DockSplitter(statusBar=self.statusBar)

            ''' Display the Qt App '''
            self.setCentralWidget(self.tab)

            loadAction = QAction('&Load and add signals', self)
            loadAction.setShortcut('Ctrl+L')
            loadAction.setStatusTip('Load signals from file, appending new signals')
            loadAction.triggered.connect(lambda: self.tab.loadSettings(False))

            overwriteAction = QAction('&Load and overwrite signals', self)
            overwriteAction.setShortcut('Ctrl+Shift+L')
            overwriteAction.setStatusTip('Load signals from file, overwriting previous signals')
            overwriteAction.triggered.connect(lambda: self.tab.loadSettings(overwrite=True))

            saveAction = QAction('&Save signals', self)
            saveAction.setShortcut('Ctrl+S')
            saveAction.setStatusTip('Save signals to a file')
            saveAction.triggered.connect(self.tab.saveSettings)

            exitAction = QAction('&Exit', self)
            exitAction.setShortcut('Ctrl+Q')
            exitAction.setStatusTip('Exit application')
            exitAction.triggered.connect(qApp.quit)
            addWindowAction = QAction('&New Window', self)
            addWindowAction.setShortcut('Ctrl+W')
            addWindowAction.setStatusTip('Add new plotting window')
            addWindowAction.triggered.connect(app.addWindow)
            addScatterAction = QAction('&New Scatter Tab', self)
            addScatterAction.setShortcut('Ctrl+Shift+N')
            addScatterAction.setStatusTip('Add new scatter tab')
            addScatterAction.triggered.connect(self.tab.addScatterPlot)

            menubar = self.menuBar()
            fileMenu = menubar.addMenu('&File')
            fileMenu.addAction(addWindowAction)
            fileMenu.addSeparator()
            fileMenu.addAction(loadAction)
            fileMenu.addAction(overwriteAction)
            fileMenu.addAction(saveAction)
            fileMenu.addSeparator()
            fileMenu.addAction(exitAction)
            fileMenu = menubar.addMenu('&Edit')
            fileMenu.addAction(addScatterAction)

            # self.config = SafeConfigParser()

        def closeEvent(self, event):
            self.tab.strip.close()

class DockSplitter(QtGui.QSplitter):

    def __init__(self, parent=None, statusBar=None):
        QtGui.QSplitter.__init__(self)
        # global MagnetController, BPMController
        self.statusBar = statusBar
        self.area = DockArea()
        self.setHandleWidth(14)
        self.setOrientation(Qt.Vertical)
        self.setStyleSheet("QSplitter::handle{background-color:transparent;}");

        self.addLinearPlot()
        self.signaltable=stable.signalTable(self.strip,MagnetController=magnets,BPMController=bpms, GeneralController=general)
        self.addWidget(self.signaltable)

        self.timeButton10s = self.createTimeButton('10s')
        self.timeButton1m = self.createTimeButton('1m')
        self.timeButton10m = self.createTimeButton('10m')
        self.timeButton1h = self.createTimeButton('1h')
        self.timeButton8h = self.createTimeButton('8h')
        self.timeButtonLayout = QHBoxLayout()
        self.timeButtonWidget = QWidget()
        self.timeButtonWidget.setMaximumHeight(100)
        self.timeButtonLayout.addWidget(self.timeButton10s)
        self.timeButtonLayout.addWidget(self.timeButton1m)
        self.timeButtonLayout.addWidget(self.timeButton10m)
        self.timeButtonLayout.addWidget(self.timeButton1h)
        self.timeButtonLayout.addWidget(self.timeButton8h)

        self.timeButtonWidget.setLayout(self.timeButtonLayout)
        self.spTimeButtonsLayout = QVBoxLayout()
        self.spTimeButtonsWidget = QWidget()
        self.spTimeButtonsLayout.addWidget(self.timeButtonWidget,1)
        self.spTimeButtonsWidget.setLayout(self.spTimeButtonsLayout)
        self.addWidget(self.area)
        self.addWidget(self.timeButtonWidget)

        handle = self.handle(1)
        layout = QtGui.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.splitterbutton = [1,2,3]
        self.splitterbuttonArrows = [1,2,3]

        self.splitterbutton[0] = QtGui.QToolButton(handle)
        self.splitterbutton[0].setArrowType(QtCore.Qt.DownArrow)
        self.splitterbuttonArrows[0] = [QtCore.Qt.UpArrow,QtCore.Qt.DownArrow]
        self.splitterbutton[0].clicked.connect(
            lambda: self.handleSplitterButton(no=0,closed=False))
        self.splitterMoved.connect(lambda x: self.handleSplitterButtonArrow(no=0, pos=x))
        layout.addWidget(self.splitterbutton[0])
        handle.setLayout(layout)

        handle = self.handle(2)
        layout = QtGui.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.splitterbutton[2] = QtGui.QToolButton(handle)
        self.splitterbutton[2].setArrowType(QtCore.Qt.DownArrow)
        self.splitterbuttonArrows[2] = [QtCore.Qt.DownArrow, QtCore.Qt.UpArrow]
        self.splitterbutton[2].clicked.connect(
            lambda: self.handleSplitterButton(no=2,closed=False))
        self.splitterMoved.connect(lambda x: self.handleSplitterButtonArrow(no=2, pos=x))
        layout.addWidget(self.splitterbutton[2])
        handle.setLayout(layout)

        self.setStretchFactor(0,1)
        self.setStretchFactor(1,4)
        self.setStretchFactor(2,1)
        self.GUIsizes = [100, 1000, 100]
        self.handleSplitterButton(no=0,closed=True)
        self.handleSplitterButton(no=2,closed=True)

        self.numberScatterPlots = 0
        self.scatterPlots = []

    def loadSettings(self, overwrite=False):
        loadFileNames = QtGui.QFileDialog.getOpenFileNames(self, caption='Load Settings', directory='', filter="Settings files (*.cfg);;", selectedFilter="Settings files (*.cfg)")
        if overwrite:
            self.strip.deleteAllCurves(reply=True)
        for loadFile in loadFileNames:
            config = SafeConfigParser()
            config.read(str(loadFile))
            for section in config.sections():
                if not section == 'Plotting':
                    functionform = eval(config.get(section,'functionform'))
                    self.signaltable.addRow(name=config.get(section,'name'), functionForm=functionform , functionArgument=config.get(section,'functionargument'), freq=config.getfloat(section,'freq'), colourpickercolour=config.get(section,'pen'))

    def saveSettings(self):
        saveFileName = str(QtGui.QFileDialog.getSaveFileName(self, 'Save Settings', '', filter="Settings files (*.cfg);;", selectedFilter="Settings files (*.cfg)"))
        filename, file_extension = os.path.splitext(saveFileName)
        config = SafeConfigParser()
        for name in self.strip.records:
            section = str(name)
            config.add_section(section)
            config.set(section, 'name', str(self.strip.records[name]['name']))
            config.set(section, 'pen', str(self.strip.records[name]['pen'].name()))
            config.set(section, 'freq', str(1.0/self.strip.records[name]['timer']))
            config.set(section, 'maxlength', str(self.strip.records[name]['maxlength']))
            config.set(section, 'functionForm', str(self.strip.records[name]['functionForm']))
            config.set(section, 'functionArgument', str(self.strip.records[name]['functionArgument']))
        with open(saveFileName, 'wb') as configfile:
            config.write(configfile)

    def addLinearPlot(self):
        ''' initialise scatter plot '''
        self.strip = striptool.stripPlot(plotRateBar=True)
        self.connect(self, SIGNAL("timeButtonPushed(int)"), self.changePlotScales)
        self.strip.plotWidget.statusChanged.connect(self.updateStatusBar)
        dock = Dock('Linear', size=(500,200))
        dock.addWidget(self.strip)
        self.area.addDock(dock=dock, position='bottom')
        self.strip.setPlotScale(60)
        self.strip.start()
        self.strip.pausePlotting(False)

    def appendScatterPlots(self, dock):
        for widget in dock.widgets:
            if isinstance(widget, scatterplot.scatterPlot):
                self.scatterPlots.append(dock)

    def addScatterPlot(self):
        self.scatterPlots = []
        print self.findChildren(scatterplot.scatterPlot)
        docks = self.findChildren((Dock))
        for dock in docks:
            self.appendScatterPlots(dock)
        # print self.scatterPlots
        ''' initialise scatter plot '''
        scatter = scatterplot.scatterPlot(stripplot=self.strip, plotRateBar=False, color=self.numberScatterPlots)
        dock = Dock('Scatter '+str(self.numberScatterPlots), size=(500,200))
        dock.addWidget(scatter)
        # print type(dock)
        if not len(self.scatterPlots) > 0:
            self.area.addDock(dock=dock, position='bottom')
        else:
            self.area.addDock(dock=dock, position='below', relativeTo=self.scatterPlots[-1])
        self.scatterPlots.append(dock)
        self.numberScatterPlots += 1
        scatter.start()

    def handleSplitterButton(self, no=0, closed=True):
        sizes = self.sizes()
        if closed:
            self.setStretchFactor(no,0)
            self.GUIsizes[no] = 0
        elif sizes[no] == 0:
            self.setStretchFactor(no,1)
            self.GUIsizes[no] = 100
        else:
            self.setStretchFactor(no,0)
            self.GUIsizes[no] = 0
        self.setSizes(self.GUIsizes)
        self.handleSplitterButtonArrow(no=no)

    def handleSplitterButtonArrow(self, no=0, pos=0):
        sizes = self.sizes()
        if sizes[no] > 0:
            self.splitterbutton[no].setArrowType(self.splitterbuttonArrows[no][0])
        else:
            self.splitterbutton[no].setArrowType(self.splitterbuttonArrows[no][1])

    def createTimeButton(self,label):
        button = timeButton(self)
        button.setText(label)
        return button

    def updateStatusBar(self,text):
        self.statusBar.clearMessage()
        self.statusBar.showMessage(text,2000)

    def changePlotScales(self, time):
        # print 'time = ', time
        for plot in self.findChildren((striptool.stripPlot)):
            plot.setPlotScale(time)

def main():
   # app = QApplication(sys.argv)
   ''' Initiate magnet and BPM controllers '''
   global magInit, magnets, bpms, general
   magInit = vmag.init()
   magnets = magInit.virtual_VELA_INJ_Magnet_Controller()
<<<<<<< HEAD
   bpmInit = vbpmc.init()
   bpms = bpmInit.virtual_VELA_INJ_BPM_Controller()
   general = vgen.init()

=======
   bpms = vbpmc.velaINJBeamPositionMonitorController(False, False)
>>>>>>> 4ca5038f8fd7937332dc468ca9c3c4c7ddb4ecc4

   ''' These are some options for pyqtgraph that make the graph black-on-white, and turn on antialiasing, which is nicer on the eye '''
   pg.setConfigOptions(antialias=True)
   pg.setConfigOption('background', 'w')
   pg.setConfigOption('foreground', 'k')
   mainApp()

if __name__ == '__main__':
   main()
