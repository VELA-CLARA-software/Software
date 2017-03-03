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
import loggerWidget as lw
import logging
logger = logging.getLogger(__name__)

sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\Release')
#sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VM-Controllers\\VELA-CLARA-Controllers\\Controllers\\VELA\INJECTOR\\velaINJBeamPositionMonitors\\bin\\Release')
import VELA_CLARA_MagnetControl as mag
import velaINJBeamPositionMonitorControl as vbpmc


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
        ex.pausePlots(ex.tab)

    class striptool_Demo_Magnets(QMainWindow):
        def __init__(self, app = None, parent = None):
            # super(self.striptool_Demo_Magnets, self).__init__(parent)
            QMainWindow.__init__(self)
            global magnets, bpms

            exitAction = QAction('&Exit', self)
            exitAction.setShortcut('Ctrl+Q')
            exitAction.setStatusTip('Exit application')
            exitAction.triggered.connect(qApp.quit)
            addWindowAction = QAction('&New Window', self)
            addWindowAction.setShortcut('Ctrl+W')
            addWindowAction.setStatusTip('Add new plotting window')
            addWindowAction.triggered.connect(app.addWindow)
            addPlotAction = QAction('&New Plot Tab', self)
            addPlotAction.setShortcut('Ctrl+N')
            addPlotAction.setStatusTip('Add new plotting tab')
            addPlotAction.triggered.connect(self.addLinearPlot)
            addScatterAction = QAction('&New Scatter Tab', self)
            addScatterAction.setShortcut('Ctrl+Shift+N')
            addScatterAction.setStatusTip('Add new scatter tab')
            addScatterAction.triggered.connect(self.addScatterPlot)
            addLogAction = QAction('&New Log Tab', self)
            addLogAction.setShortcut('Ctrl+Shift+L')
            addLogAction.setStatusTip('Add new log tab')
            addLogAction.triggered.connect(self.addLogTab)

            self.setWindowTitle("striptool_Demo_Magnets")
            self.statusBar = QStatusBar()
            self.setStatusBar(self.statusBar)

            menubar = self.menuBar()
            fileMenu = menubar.addMenu('&File')
            fileMenu.addAction(addWindowAction)
            fileMenu.addAction(exitAction)
            fileMenu = menubar.addMenu('&Edit')
            fileMenu.addAction(addPlotAction)
            fileMenu.addAction(addScatterAction)
            fileMenu = menubar.addMenu('&Log')
            fileMenu.addAction(addLogAction)

            self.tab = QTabWidget()
            self.tab.setMovable(True)
            self.tab.setTabsClosable(True)
            self.tab.tabCloseRequested.connect(self.closeTab)

            ''' Here we connect the QTabWidget signal "currentChanged" to a function defined above. This will pause plots not currently visible
                whenever the tabs are changed. This reduces the load as only visible plots are updated. '''
            self.tab.currentChanged.connect(lambda x: self.pausePlots(self.tab))

            ''' Display the Qt App '''
            self.setCentralWidget(self.tab)

            self.numberLinearPlots = 0
            self.numberScatterPlots = 0

        def closeTab(self, index):
            print self.tab.widget(index)
            widget = self.tab.widget(index)
            if widget.type == 'strip':
                for plot in widget.scatterPlots:
                    plot.setParent(None)
            widget.setParent(None)
            print self.tab.findChildren((striptool.stripPlot, scatterplot.scatterPlot))

        def addLogTab(self):
            ''' Initiate logger (requires loggerWidget - comment out if not available)'''
            self.logwidget1 = lw.loggerWidget([logger,striptool.logger])
            ''' Add loggerWidget Tab (requires loggerWidget - comment out if not available)'''
            self.tab.addTab(self.logwidget1,"Log")

        def addLinearPlot(self):
            self.numberLinearPlots += 1
            plot = self.LinearPlotTab(MagnetController=magnets, BPMController=bpms)
            plot.label = "Strip Plot "+str(self.numberLinearPlots)
            self.tab.insertTab(self.tab.count()-1, plot, plot.label)
            self.tab.setCurrentIndex(self.tab.count()-2)
            self.connect(plot, SIGNAL("timeButtonPushed(int)"), self.changePlotScales)
            plot.sp.plotWidget.statusChanged.connect(self.updateStatusBar)
            self.pausePlots(self.tab)

        def addScatterPlot(self):
            # scatterLayout = QGridLayout()
            # scatterWidget = QFrame()
            # scatterWidget.setLayout(scatterLayout)
            print self.tab.currentWidget
            if hasattr(self.tab.currentWidget(),'type'):
                print 'type = ', self.tab.currentWidget().type
                if self.tab.currentWidget().type == 'strip':
                    stripplot = self.tab.currentWidget()
                    # print stripplot
                    scatterplot = self.ScatterPlotTab(parent=self, strip=stripplot, tab=self.tab)
                    self.tab.insertTab(self.tab.currentIndex()+len(stripplot.scatterPlots),scatterplot,scatterplot.scatterplotlabel)
                    self.pausePlots(self.tab)
                elif self.tab.currentWidget().type == 'scatter':
                    self.tab.currentWidget().addScatterPlot()

        class ScatterPlotTab(QWidget):
            def __init__(self, parent=None, strip=None, tab=None):
                QWidget.__init__(self)
                self.tab = tab
                self.strip = strip.sp
                self.strip.label = strip.label
                self.type = 'scatter'
                self.layout = QtGui.QVBoxLayout()
                self.area = DockArea()
                self.layout.addWidget(self.area)
                self.setLayout(self.layout)

                self.numberScatterPlots = 0
                self.scatterLayout = self
                # self.setCentralWidget(self.scatterLayout)
                # self.setLayout(self.scatterLayout)
                self.scatterplotnumber = len(self.tab.currentWidget().scatterPlots)
                self.scatterplotlabel = "Scatter Plot "+str(self.scatterplotnumber+1)+" ("+self.strip.label+")"
                self.addScatterPlot()
                strip.scatterPlots.append(self)

            def addScatterPlot(self):
                ''' initialise scatter plot '''
                scatter = scatterplot.scatterPlot(stripplot=self.strip, plotRateBar=False, color=self.scatterplotnumber+self.numberScatterPlots)
                dock = Dock(str(self.numberScatterPlots), size=(500,200))
                dock.addWidget(scatter)
                self.area.addDock(dock=dock, position='bottom')
                self.numberScatterPlots += 1
                scatter.start()

        class LinearPlotTab(QtGui.QSplitter):

            def __init__(self, parent=None, plotRateBar=False, MagnetController=None, BPMController=None):
                QtGui.QSplitter.__init__(self)
                self.scatterPlots = []
                self.label = ''
                self.type = 'strip'
                ''' initialise an instance of the stripPlot Widget '''
                self.sp = striptool.stripPlot(plotRateBar=plotRateBar)

                ''' Here we create a tab layout widget, and put the 3 stripplots into a grid layout in one of the tabs
                    In the second tab we put the first stripplot. NB: the stripplot "sp" can only exist in one place at a time!
                    Comment out line 83 to see the difference. '''

                self.setHandleWidth(14)
                self.setOrientation(Qt.Vertical)
                self.setStyleSheet("QSplitter::handle{background-color:transparent;}");
                self.addWidget(stable.signalTable(self.sp,MagnetController=MagnetController,BPMController=BPMController))
                self.timeButton10 = self.createTimeButton('10s')
                self.timeButton60 = self.createTimeButton('1m')
                self.timeButton600 = self.createTimeButton('10m')
                self.timeButtonLayout = QHBoxLayout()
                self.timeButtonWidget = QWidget()
                self.timeButtonWidget.setMaximumHeight(100)
                self.timeButtonLayout.addWidget(self.timeButton10)
                self.timeButtonLayout.addWidget(self.timeButton60)
                self.timeButtonLayout.addWidget(self.timeButton600)
                self.timeButtonWidget.setLayout(self.timeButtonLayout)
                self.spTimeButtonsLayout = QVBoxLayout()
                self.spTimeButtonsWidget = QWidget()
                self.spTimeButtonsLayout.addWidget(self.sp,10)
                self.spTimeButtonsLayout.addWidget(self.timeButtonWidget,1)
                self.spTimeButtonsWidget.setLayout(self.spTimeButtonsLayout)
                self.addWidget(self.sp)
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

                ''' This starts the plotting timer (by default at 1 Hz) '''
                self.sp.start()

                ''' modify the plot scale to 10 secs '''
                self.sp.setPlotScale(60)

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

        def pausePlots(self, parentwidget):
            widgets = parentwidget.findChildren((striptool.stripPlot, scatterplot.scatterPlot))
            for widget in widgets:
                if widget.isVisible():
                    widget.pausePlotting(False)
                    widget.plotUpdate()
                else:
                    widget.pausePlotting(True)

        def changePlotScales(self, time):
            print 'time = ', time
            for plot in self.findChildren((striptool.stripPlot)):
                plot.setPlotScale(time)

def main():
   # app = QApplication(sys.argv)
   ''' Initiate magnet and BPM controllers '''
   global magInit, magnets, bpms
   magInit = mag.init()
   magnets = magInit.virtual_VELA_INJ_Magnet_Controller()
   bpms = vbpmc.velaINJBeamPositionMonitorController(False, False)

   ''' These are some options for pyqtgraph that make the graph black-on-white, and turn on antialiasing, which is nicer on the eye '''
   pg.setConfigOptions(antialias=True)
   pg.setConfigOption('background', 'w')
   pg.setConfigOption('foreground', 'k')
   mainApp()

if __name__ == '__main__':
   main()
