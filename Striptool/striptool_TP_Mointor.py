import sys,os
os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12" #BE SPECIFIC.... YOUR I.P. FOR YOUR VM
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import striptool as striptool
import numpy as np
import sys, time
import pyqtgraph as pg
''' Load loggerWidget library (comment out if not available) '''
#import loggerWidget as lw
import logging
logger = logging.getLogger(__name__)

sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\Release')
import VELA_CLARA_MagnetControl as mag

def main():

    ''' Initiate PyQT application '''
    app = QApplication(sys.argv)
    magInit = mag.init()
    magnets = magInit.virtual_VELA_INJ_Magnet_Controller()
    ''' Initiate logger (requires loggerWidget - comment out if not available)'''
    #logwidget1 = lw.loggerWidget([logger,striptool.logger])

    ''' initialise an instance of the stripPlot Widget '''
    sp = striptool.stripPlot()
    sp2 = striptool.stripPlot()

    ''' These are some options for pyqtgraph that make the graph black-on-white, and turn on antialiasing, which is nicer on the eye '''
    pg.setConfigOptions(antialias=True)
    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')

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
    sp.addSignal(name='HCOR01_RI',pen='r', timer=1.0/10.0, function=lambda: magnets.getRI('HCOR01'))
    sp.addSignal(name='HCOR02_RI',pen='g', timer=1.0/10.0, function=lambda: magnets.getRI('HCOR02'))
    sp2.addSignal(name='QUAD01_RI',pen='r', timer=1.0/50.0, function=lambda: magnets.getRI('QUAD01'))
    # sp2.addSignal(name='signal2',pen='g', timer=1.0/50.0, function=lambda: createRandomSignal(-0.5))


    ''' To remove a signal, reference it by name or use the in-built controls'''
    # sp.removeSignal(name='signal1')
    # sp.removeSignal(name='signal2')

    ''' Here we create a tab layout widget, and put the strip plot in one of the tabs, with an empty QWidget in the other '''
    tab = QTabWidget()
    tab.addTab(sp,"Strip Plot")
    tab.addTab(sp2,"Strip Plot 2")
    ''' Add loggerWidget Tab (requires loggerWidget - comment out if not available)'''
    #tab.addTab(logwidget1,"Log")
    layout = QWidget()

    ''' This starts the plotting timer (by default at 1 Hz) '''
    sp.start()
    sp2.start()
    ''' Display the Qt App '''
    tab.show()

    ''' modify the plot scale to 10 secs '''
    sp.setPlotScale(60)
    # sp2.setPlotScale(60)

    ''' Default PyQT exit handler '''
    sys.exit(app.exec_())

if __name__ == '__main__':
   main()
