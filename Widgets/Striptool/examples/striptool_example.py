import sys, time, os
sys.path.append("..") # Only required if Striptool++ is not on the PYTHONPATH
from PyQt4 import QtCore, QtGui
import pyqtgraph as pg
import striptool as striptool
import numpy as np

class striptool_Demo(QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(striptool_Demo, self).__init__(parent)

        ''' These are some options for pyqtgraph that make the graph black-on-white, and turn on antialiasing, which is nicer on the eye '''
        pg.setConfigOptions(antialias=True)
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        ''' initialise an instance of the stripPlot Widget '''
        self.sp = striptool.stripPlot(plotRateBar=True,crosshairs=True)

        ''' Start the striptool plotting... '''
        self.sp.start()

        ''' Set the striptool as the central widget '''
        self.setCentralWidget(self.sp)

        ''' Add signal using generating function "createRandomSignal", defining the pen color and the recording rate '''
        self.sp.addSignal(name='signal1',pen='r', timer=1.0/100.0, function=self.createRandomSignal, arg=[0.5])

        ''' Set the starting time scale in seconds'''
        self.sp.setPlotScale(600)

        ''' Set the plot update rate in Hz '''
        self.sp.setPlotRate(10)

    ''' Create a double-sinusoidal function with offset '''
    def createRandomSignal(self, offset=0):
        t = time.time()
        signalValue = np.sin(2*2*np.pi*t+0.05)+np.sin(1.384*2*np.pi*t-0.1)+0.5*np.random.normal()
        return signalValue+offset

    ''' For a clean exit, close the striptool '''
    def closeEvent(self, e):
        self.sp.close()

def main():
    app = QtGui.QApplication(sys.argv)
    example = striptool_Demo()
    example.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
   main()
