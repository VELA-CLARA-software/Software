import sys, time, os
sys.path.append("..")
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import pyqtgraph as pg
import striptool as striptool
import scatterPlot as scatterplot
import numpy as np
''' Load loggerWidget library (comment out if not available) '''
sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\..\\..\\loggerWidget\\')
# import loggerWidget as lw
# import logging
# logger = logging.getLogger(__name__)

''' This is a signal generator. It could easily read a magnet current using the hardware controllers
    The signal should have peaks at 5 Hz and 10 Hz, which should be seen on the FFT plot assuming the
    sample rate is high enough
'''

class scatterPlot_Demo(QMainWindow):
    def __init__(self, parent = None):
        super(scatterPlot_Demo, self).__init__(parent)

        self.setWindowTitle("scatterPlot_Demo")
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        ''' Initiate logger (requires loggerWidget - comment out if not available)'''
        # logwidget1 = lw.loggerWidget([logger,striptool.logger])

        ''' These are some options for pyqtgraph that make the graph black-on-white, and turn on antialiasing, which is nicer on the eye '''
        pg.setConfigOptions(antialias=True)
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        ''' initialise an instance of the stripPlot Widget '''
        self.strip = striptool.stripPlot(plotRateBar=False)

        ''' Add some signals to the striptool - note they call our signal generator at a frequency of 1/timer (100 Hz and 10 Hz in these cases).
            The 'pen' argument sets the color of the curves, but can be changed in the GUI
                - see <http://www.pyqtgraph.org/documentation/style.html>'''
        self.strip.addSignal(name='signal1',pen='r', timer=1.0/10.0, function=lambda: self.createRandomSignal(-0.5))
        self.strip.addSignal(name='signal2',pen='g', timer=1.0/10.0, function=lambda: self.createRandomSignal(0.5))
        self.strip.addSignal(name='signal3',pen='b', timer=1.0/10.0, function=lambda: self.createRandomSignal(0.0))
        self.strip.addSignal(name='signal4',pen='y', timer=1.0/10.0, function=lambda: self.createRandomSignal(0.0))

        ''' Here we create a tab layout widget, and put the 3 stripplots into a grid layout in one of the tabs
            In the second tab we put the first stripplot. NB: the stripplot "sp" can only exist in one place at a time!
            Comment out line 83 to see the difference. '''
        self.tab = QTabWidget()
        self.numberScatterPlots = 0

        self.stripWidget = pg.LayoutWidget()
        self.stripWidget.addWidget(self.strip,1,0,3,3)

        self.scatterLayout = QGridLayout()
        self.scatterWidget = QFrame()
        self.scatterWidget.setLayout(self.scatterLayout)
        self.addScatterPlotButton = QPushButton('Add Plot')
        self.addScatterPlotButton.clicked.connect(lambda: self.addScatterPlot(self.strip))
        self.scatterLayout.addWidget(self.addScatterPlotButton,0,0)
        self.addScatterPlot(self.strip)
        self.tab.addTab(self.stripWidget,"Strip Plot")
        self.tab.addTab(self.scatterWidget,"Scatter Plot")
        ''' Here we connect the QTabWidget signal "currentChanged" to a function defined above. This will pause plots not currently visible
            whenever the tabs are changed. This reduces the load as only visible plots are updated. '''
        self.tab.currentChanged.connect(lambda x: self.pausePlots(self.tab))

        ''' This starts the plotting timer (by default at 1 Hz) '''
        self.strip.start()

        ''' modify the plot scale to 10 secs '''
        self.strip.setPlotScale(60)

        ''' Display the Qt App '''
        self.setCentralWidget(self.tab)

        self.strip.plotWidget.statusChanged.connect(self.updateStatusBar)

    def updateStatusBar(self,text):
        self.statusBar.clearMessage()
    	self.statusBar.showMessage(text,2000)

    def createRandomSignal(self, offset=0):
        signalValue = np.sin(2*2*np.pi*time.time()+0.05)+np.sin(1.384*2*np.pi*time.time()-0.1)+0.5*np.random.normal()
        return signalValue+offset

    def createRandomSignal2(self, offset=0):
        signalValue = -1*(np.sin(2*12*np.pi*time.time()+0.05)+np.sin(0.2563*2*np.pi*time.time()-0.1))+0.5*np.random.normal()
        return signalValue+offset

    def pausePlots(self, parentwidget):
        widgets = parentwidget.findChildren((striptool.stripPlot,scatterplot.scatterPlot))
        for widget in widgets:
            if widget.isVisible():
                widget.pausePlotting(False)
                widget.plotUpdate()
            else:
                widget.pausePlotting(True)

    def addScatterPlot(self, strip):
        ''' initialise scatter plot '''
        self.scatter = scatterplot.scatterPlot(stripplot=strip, plotRateBar=False, color=self.numberScatterPlots)
        row = 1 + self.numberScatterPlots / 3
        print 'row = ', row
        col = (self.numberScatterPlots) % 3
        print 'col = ', col
        self.scatterLayout.addWidget(self.scatter,row,col)
        self.numberScatterPlots += 1
        self.scatter.start()
        self.scatter.setPlotScale(xRange=[-10,10],yRange=[-10,10])
        self.scatter.plotWidget.statusChanged.connect(self.updateStatusBar)

def main():
   app = QApplication(sys.argv)
   ex = statusdemo()
   ex.show()
   ex.pausePlots(ex.tab)
   sys.exit(app.exec_())

if __name__ == '__main__':
   main()
