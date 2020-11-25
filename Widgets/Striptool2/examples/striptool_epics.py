import sys, time, os
sys.path.append(".")
sys.path.append("..")
# if sys.version_info<(3,0,0):
# from PyQt4.QtCore import *
# from PyQt4.QtGui import *
# else:
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pyqtgraph as pg
from pyqtgraph.dockarea import *
import generalPlot as generalplot
import scrollingPlot as scrollingplot
import signalTable as signaltable
import numpy as np
from splitterWithHandles import *
import VELA_CLARA_Magnet_Control as vmag
maginit = vmag.init()
Vmagnets = maginit.physical_VELA_INJ_Magnet_Controller()
Cmagnets = maginit.physical_CLARA_PH1_Magnet_Controller()
import VELA_CLARA_BPM_Control as vbpmc
bpms = vbpmc.init()
import  VELA_CLARA_General_Monitor as vgen
general = vgen.init()
''' Load loggerWidget library (comment out if not available) '''
# sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\..\\..\\loggerWidget\\')
# import loggerWidget as lw
# import logging
# logger = logging.getLogger(__name__)

seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}

def convert_to_seconds(s):
    return int(s[:-1]) * seconds_per_unit[s[-1]]

class timeButton(QPushButton):

    timeButtonPushed = pyqtSignal('int')

    def __init__(self, label):
        super(timeButton, self).__init__()
        self.setText(label)
        self.clicked.connect(self.buttonPushed)

    def buttonPushed(self):
        self.timeButtonPushed.emit(convert_to_seconds(str(self.text())))

class striptool_Demo(QMainWindow):
    def __init__(self, parent = None):
        super(striptool_Demo, self).__init__(parent)

        stdicon = self.style().standardIcon
        style = QStyle
        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        scatterPlotAction = QAction('+Scatter', self)
        scatterPlotAction.setStatusTip('Add Scatter Plot')
        scatterPlotAction.triggered.connect(self.addScatterPlot)

        fftPlotAction = QAction('+FFT', self)
        fftPlotAction.setStatusTip('Add FFT Plot')
        fftPlotAction.triggered.connect(self.addFFTPlot)

        self.setWindowTitle("striptool_Demo")
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        ''' Initiate logger (requires loggerWidget - comment out if not available)'''
        # self.logwidget1 = lw.loggerWidget([logger,striptool.logger])

        ''' These are some options for pyqtgraph that make the graph black-on-white, and turn on antialiasing, which is nicer on the eye '''
        pg.setConfigOptions(antialias=False)
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        ''' initialise an instance of the stripPlot Widget '''
        self.generalplot = generalplot.generalPlot()
        self.scrollingplot = self.generalplot.scrollingPlot()
        self.fftplot = self.generalplot.fftPlot()
        self.histogramplot = self.generalplot.histogramPlot()
        self.scatterplot = self.generalplot.scatterPlot()
        self.legend = self.generalplot.legend()
        self.signaltable = signaltable.signalTable(parent=self.generalplot, VELAMagnetController=Vmagnets, CLARAMagnetController=Cmagnets, BPMController=bpms, GeneralController=general)

        self.enabledPlotNames = []
        self.legend.legendselectionchanged.connect(self.addSignalToFFTHistogramPlots)

        ''' Here we create a DockArea layout widget, and put the 4 types of plot into a grid layout
            We place all of it in a modified QSPlitter (with Handles)
        '''
        self.area = DockArea()
        d1 = Dock("Scrolling Plot")
        d2 = Dock("Plot Legend")
        d3 = Dock("FFT Plot")
        d4 = Dock("Scatter Plot")
        d5 = Dock("Histogram Plot")
        d1.addWidget(self.scrollingplot)
        d2.addWidget(self.legend)
        d3.addWidget(self.fftplot)
        d4.addWidget(self.scatterplot)
        d5.addWidget(self.histogramplot)
        self.area.addDock(d1, position='top')
        self.area.addDock(d2, position='right', relativeTo=d1)
        self.area.addDock(d3,'bottom')
        self.area.addDock(d4, position='right', relativeTo=d3)
        self.area.addDock(d5, position='right', relativeTo=d4)

        ''' Make QSPlitter '''
        self.plotLayout = splitterWithHandles()
        self.plotLayout.setOrientation(Qt.Vertical)
        self.plotLayout.addWidget(self.signaltable)
        self.plotLayout.addWidget(self.area)
        self.timeButtonList = []
        self.timeButton10 = self.createTimeButton('10s')
        self.timeButton60 = self.createTimeButton('1m')
        self.timeButton600 = self.createTimeButton('10m')
        self.timeButton6000 = self.createTimeButton('100m')
        self.timeButton60000 = self.createTimeButton('1000m')
        self.timeButtonWidget = QWidget()
        self.timeButtonLayout = QHBoxLayout()
        self.timeButtonLayout.addWidget(self.timeButton10)
        self.timeButtonLayout.addWidget(self.timeButton60)
        self.timeButtonLayout.addWidget(self.timeButton600)
        self.timeButtonLayout.addWidget(self.timeButton6000)
        self.timeButtonLayout.addWidget(self.timeButton60000)
        self.timeButtonWidget.setLayout(self.timeButtonLayout)
        self.plotLayout.addWidget(self.timeButtonWidget)

        ''' Style QSplitter Handles '''
        self.plotLayout.setHandleWidth(14)
        self.plotLayout.setStyleSheet("QSplitter::handle{background-color:transparent;}");
        ''' Set up the Handles with labels '''
        self.plotLayout.handle(1).setLocation('top','Add Signal')
        self.plotLayout.handle(2).setLocation('bottom','Set Timebase')
        ''' Default the Handles to closed '''
        self.plotLayout.handle(1).setClosed()
        self.plotLayout.handle(2).setClosed()

        ''' This starts the plotting timer (by default at 1 Hz) '''
        self.generalplot.start()
        self.scrollingplot.start()
        self.fftplot.start()
        self.scatterplot.start()
        self.histogramplot.start()

        ''' modify the plot scale to 60 secs '''
        self.scrollingplot.setPlotScale(60)

        ''' Display the Qt App '''
        self.setCentralWidget(self.plotLayout)

    ''' This is a signal generator. It could easily read a magnet current using the hardware controllers
        The signal should have peaks at 5 Hz and 10 Hz, which should be seen on the FFT plot assuming the
        sample rate is high enough
    '''
    def createRandomSignal(self, mean=0, sigma=1, freq=1.682, t=None):
        if t == None:
            t = time.time()
        signalValue = mean+sigma*np.sin(2*freq*np.pi*t+0.05)+0.5*np.random.normal(mean, sigma)#+np.sin(1.384*2*np.pi*t-0.1)+0.5*np.random.normal(mean, sigma)
        return signalValue

    def addScatterPlot(self):
        d = Dock("Scatter Plot")
        scatterplot = self.generalplot.scatterPlot()
        d.addWidget(scatterplot)
        self.area.addDock(d, position='right', relativeTo="Scatter Plot")

    def addFFTPlot(self):
        d = Dock("FFT Plot")
        fftplot = self.generalplot.fftPlot()
        d.addWidget(fftplot)
        self.area.addDock(d, position='right', relativeTo="FFT Plot")

    def addSignalToFFTHistogramPlots(self,names):
        for name in names:
            if name not in self.enabledPlotNames:
                self.enabledPlotNames.append(name)
            self.fftplot.selectionChange(name, True)
            self.histogramplot.selectionChange(name, True)
        for name in self.enabledPlotNames:
            if name not in names:
                self.fftplot.selectionChange(name, self.legend.isFFTEnabled(name))
                self.histogramplot.selectionChange(name, self.legend.isHistogramEnabled(name))

    def pausePlots(self, parentwidget):
        widgets = parentwidget.findChildren((striptool.stripPlot))
        for widget in widgets:
            if widget.isVisible():
                widget.pausePlotting(False)
                widget.plotUpdate()
            else:
                widget.pausePlotting(True)

    def createTimeButton(self,label):
        button = timeButton(label)
        button.timeButtonPushed.connect(self.changePlotScales)
        return button

    def changePlotScales(self, time):
        print( 'time = ', time)
        for plot in self.findChildren((scrollingplot.scrollingPlot)):
            plot.setPlotScale(time)

    def updateStatusBar(self,text):
        self.statusBar.clearMessage()
        self.statusBar.showMessage(text,2000)

    def testSleep(self):
        import time
        for i in range(100):
            self.sp.setPlotScale((i+1)*60)
            self.sp2.setPlotScale((i+1)*60)
            self.sp3.setPlotScale((i+1)*60)
            QtTest.QTest.qWait(1000*60)
        exit()

    def closeEvent(self, event):
        for plot in self.findChildren((scrollingplot.scrollingPlot)):
            plot.close()

def main():
   app = QApplication(sys.argv)
   # app.setStyle(QStyleFactory.create("plastique"))
   ex = striptool_Demo()
   ex.show()
   # ex.testSleep()
   sys.exit(app.exec_())

if __name__ == '__main__':
   main()
