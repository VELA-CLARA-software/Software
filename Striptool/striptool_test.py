from PyQt4.QtCore import *
from PyQt4.QtGui import *
import pyqtgraph as pg
import striptool as striptool
import numpy as np
import sys, time, os
''' Load loggerWidget library (comment out if not available) '''
sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\..\\..\\loggerWidget\\')
import loggerWidget as lw
import logging
logger = logging.getLogger(__name__)

''' This is a signal generator. It could easily read a magnet current using the hardware controllers
    The signal should have peaks at 5 Hz and 10 Hz, which should be seen on the FFT plot assuming the
    sample rate is high enough
'''
def createRandomSignal(offset=0):
    signalValue = np.sin(2*2*np.pi*time.time()+0.05)+np.sin(1.384*2*np.pi*time.time()-0.1)+0.5*np.random.normal()
    return signalValue+offset

def pausePlots(parentwidget):
    widgets = parentwidget.findChildren(striptool.stripPlot)
    for widget in widgets:
        if widget.isVisible():
            widget.pausePlotting(False)
            widget.plotUpdate()
        else:
            widget.pausePlotting(True)

def main():

    ''' Initiate PyQT application '''
    app = QApplication(sys.argv)

    ''' Initiate logger (requires loggerWidget - comment out if not available)'''
    logwidget1 = lw.loggerWidget([logger,striptool.logger])

    ''' These are some options for pyqtgraph that make the graph black-on-white, and turn on antialiasing, which is nicer on the eye '''
    pg.setConfigOptions(antialias=True)
    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')

    ''' initialise an instance of the stripPlot Widget '''
    sp = striptool.stripPlot(plotRateBar=False)
    sp2 = striptool.stripPlot(plotRateBar=False)
    sp3 = striptool.stripPlot(plotRateBar=False)

    ''' This sets the signal length at which the system starts decimating the data to speed up plotting.
        For a 2*DecimateLength signal, the decimation factor would be 2.
        Record lengths > 10,000 should plot fine for most people, and is the default.
        Here I set it to 1000 as an example :
             - a 3600 length record would decimate at order 1/3 and would have a plotting record length of 1200
             - you probably don't need to use this unless you are having trouble with slow plotting.'''
    sp.setDecimateLength(100000)

    ''' Add some signals to the striptool - note they call our signal generator at a frequency of 1/timer (100 Hz and 10 Hz in these cases).
        The 'pen' argument sets the color of the curves, but can be changed in the GUI
            - see <http://www.pyqtgraph.org/documentation/style.html>'''
    sp.addSignal(name='signal1',pen='r', timer=1.0/10.0, function=lambda: createRandomSignal(-0.5))
    sp2.addSignal(name='signal2',pen='g', timer=1.0/10.0, function=lambda: createRandomSignal(0.5))
    sp3.addSignal(name='signal3',pen='b', timer=1.0/50.0, function=lambda: createRandomSignal(0.5))

    ''' To remove a signal, reference it by name or use the in-built controls'''
    # sp.removeSignal(name='signal1')
    # sp.removeSignal(name='signal2')

    ''' Here we create a tab layout widget, and put the 3 stripplots into a grid layout in one of the tabs
        In the second tab we put the first stripplot. NB: the stripplot "sp" can only exist in one place at a time!
        Comment out line 83 to see the difference. '''
    tab = QTabWidget()
    plotLayout = QGridLayout()
    plotLayout.addWidget(sp,0,0,1,1)
    plotLayout.addWidget(sp2,0,1,1,1)
    plotLayout.addWidget(sp3,1,0,1,2)
    plotWidget = QFrame()
    plotWidget.setLayout(plotLayout)
    tab.addTab(plotWidget,"Strip Plot")
    tab.addTab(sp,"Strip Plot 1")
    ''' Here we connect the QTabWidget signal "currentChanged" to a function defined above. This will pause plots not currently visible
        whenever the tabs are changed. This reduces the load as only visible plots are updated. '''
    tab.currentChanged.connect(lambda x: pausePlots(tab))

    ''' Add loggerWidget Tab (requires loggerWidget - comment out if not available)'''
    tab.addTab(logwidget1,"Log")
    layout = QWidget()

    ''' This starts the plotting timer (by default at 1 Hz) '''
    sp.start()
    sp2.start()
    sp3.start()
    ''' Display the Qt App '''
    tab.show()

    ''' modify the plot scale to 10 secs '''
    sp.setPlotScale(60)
    sp2.setPlotScale(60)
    sp3.setPlotScale(600)

    ''' Default PyQT exit handler '''
    sys.exit(app.exec_())

if __name__ == '__main__':
   main()
