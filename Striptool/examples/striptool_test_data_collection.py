import sys, time, os
sys.path.append("..")
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import pyqtgraph as pg
import striptool as striptool
import numpy as np
''' Load loggerWidget library (comment out if not available) '''
# import loggerWidget as lw
# import logging
# logger = logging.getLogger(__name__)

''' This is a signal generator. It could easily read a magnet current using the hardware controllers
    The signal should have peaks at 5 Hz and 10 Hz, which should be seen on the FFT plot assuming the
    sample rate is high enough
'''
def createRandomSignal(offset=0):
    signalValue = np.sin(2*2*np.pi*time.time()+0.05)+np.sin(1.384*2*np.pi*time.time()-0.1)+0.5*np.random.normal()
    return signalValue+offset

def main():

    ''' Initiate PyQT application '''
    app = QApplication(sys.argv)

    ''' initialise an instance of the stripPlot Widget '''
    sp = striptool.stripPlot(plotRateBar=False)

    ''' Add some signals to the striptool - note they call our signal generator at a frequency of 1/timer (100 Hz and 10 Hz in these cases).
        The 'pen' argument sets the color of the curves, but can be changed in the GUI
            - see <http://www.pyqtgraph.org/documentation/style.html>'''
    sp.addSignal(name='signal1',pen='r', timer=1.0/100.0, function=lambda: createRandomSignal(-0.5))
    sp.addSignal(name='signal2',pen='r', timer=1.0/100.0, function=lambda: createRandomSignal(-0.5))
    sp.addSignal(name='signal3',pen='r', timer=1.0/100.0, function=lambda: createRandomSignal(-0.5))
    sp.addSignal(name='signal4',pen='r', timer=1.0/100.0, function=lambda: createRandomSignal(-0.5))
    sp.addSignal(name='signal5',pen='r', timer=1.0/100.0, function=lambda: createRandomSignal(-0.5))
    sp.addSignal(name='signal6',pen='r', timer=1.0/100.0, function=lambda: createRandomSignal(-0.5))
    sp.addSignal(name='signal7',pen='r', timer=1.0/100.0, function=lambda: createRandomSignal(-0.5))
    sp.addSignal(name='signal8',pen='r', timer=1.0/100.0, function=lambda: createRandomSignal(-0.5))
    sp.addSignal(name='signal9',pen='r', timer=1.0/100.0, function=lambda: createRandomSignal(-0.5))
    sp.addSignal(name='signal10',pen='r', timer=1.0/100.0, function=lambda: createRandomSignal(-0.5))

    ''' This starts the plotting timer (by default at 1 Hz) '''
    sp.start()

    ''' collect 10s worth of data '''
    for i in range(60):
        print i
        time.sleep(1)
    ''' save data '''
    sp.saveAllCurves("signal.csv")

    exit()

    ''' Default PyQT exit handler '''
    sys.exit(app.exec_())

if __name__ == '__main__':
   main()
