"""
To make this work, you will need to install PyQt5 on Python 3

you should be able to do:
    pip install pyqt5

If you are on python 2, you can still use PyQt5.

If you need PyQt4 for some reason (only on python2 I think), you can replace the
import statements with:
from PyQt4.QtCore import *
from PyQt4.QtGui import *

for numpy and pyqtgraph, you should be able to do:
    pip install pyqtgraph numpy

"""

import sys, os, random
from PyQt5.QtCore import *
from  PyQt5.QtGui import *
from  PyQt5.QtWidgets import *
import pyqtgraph as pg
import numpy as np
from pv import *

class mainWindow(QMainWindow):
  def __init__(self, parent = None):
        super(mainWindow, self).__init__(parent)

        self.setWindowTitle('This is an example PyQt application')

        ''' This adds a menu bar to the window'''
        menubar = self.menuBar()
        '''This adds a "File" menu entry'''
        fileMenu = menubar.addMenu('&File')

        '''This defines an action that will go in the menu bar'''
        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)
        '''this adds the exit function to the "File" menu'''
        fileMenu.addAction(exitAction)

        ''' This defines a Widget '''
        self.tabWidget = QTabWidget()
        ''' This defines the main widget inside the main window'''
        self.setCentralWidget(self.tabWidget)
        bpms = ['IS1BPM01', 'IS1BPM02','IS1BPM03','IS1BPM04']
        for b in bpms:
            self.tabWidget.addTab(bpmFFTPlot(b+'-positionArrayHorizM'),b)

''' This is a QWidget that contains some plots'''
class bpmFFTPlot(QWidget):
    def __init__(self, bpmName, parent=None):
        super(bpmFFTPlot, self).__init__(parent)
        '''We can add widgets inside this widget using a layout'''
        self.layout = QVBoxLayout()
        '''This sets the layout into the widget'''
        self.setLayout(self.layout)

        self.lengthWidget = QSpinBox()
        self.lengthWidget.setMinimum(1)
        self.lengthWidget.setMaximum(600)
        self.lengthWidget.setValue(300)
        self.lengthWidget.setMaximumWidth(300)

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.lengthWidget)
        self.layout.addLayout(self.buttonLayout)

        '''lets add some plots'''
        self.plots = {}
        self.randomData = {}
        ''' we store references to the plots, so we can reference them later... '''
        for i in range(2):
            if i == 1:
                self.plots[i] = plot(i, fft=True)
            else:
                self.plots[i] = plot(i, fft=False)
            ''' Here we add each plot to the LAYOUT of the main WIDGET '''
            self.lengthWidget.valueChanged.connect(self.plots[i].setLength)
            self.layout.addWidget(self.plots[i])
            self.pv = PVWaveform(bpmName)
            self.pv.newValue.connect(self.plots[i].newReading)

''' This is a plotting widget from pyqtgraph '''
class plot(pg.PlotWidget):
    def __init__(self, no=0, fft=False, parent=None):
        super(plot, self).__init__(parent)
        self.FFTEnabled = fft
        self.length = 300
        ''' this add a plot to the plotWidget'''
        self.plotItem = self.getPlotItem()
        self.plotItem.showGrid(x=True, y=True)
        self.data = np.empty((0,2),int)
        ''' This make a color, indexed by integer no'''
        self.color = pg.mkColor(no)
        ''' this adds a plotItem to the plot - this is basically a independent plot line - we could have many of these '''
        ''' Note we don't have to give it data, we can just define the pen color for later '''
        self.curve = self.plotItem.plot(pen=self.color)

    def setLength(self, length):
        self.length = length

    def reset(self):
        self.data = np.empty((0,2),int)
        self.bpmPlot.clear()

    def newReading(self, x, y):
        y = y[: self.length]
        x = np.array(range(len(y)))
        if self.FFTEnabled and self.isVisible():
            x, y = self._fourierTransform(x, y)
            y = y/max(y)
        if self.isVisible():
            print ('new data!')
            self.curve.setData({'x': x, 'y': y})

    def _fourierTransform(self, x, y):
        ## Perform fourier transform. If x values are not sampled uniformly,
        ## then use np.interp to resample before taking fft.
        # print 'length x = ', len(x)
        dx = np.diff(x)
        uniform = not np.any(np.abs(dx-dx[0]) > (abs(dx[0]) / 100.))
        starttime = time.clock()
        if not uniform:
            # print('FFT not uniform!  ', max(np.abs(dx-dx[0])), ' > ', (abs(dx[0]) / 1000.))
            # x2 = np.linspace(x[0], x[0] + len(x)*self.timer, len(x))
            x2 = np.linspace(x[0], x[-1], len(x))
            y = np.interp(x2, x, y)
            x = x2
        f = np.fft.fft(y) / len(y)
        y = abs(f[1:int(len(f)/2)])
        dt = x[-1] - x[0]
        x = np.linspace(0, 0.5*len(x)/dt, len(y))
        # print 'FFT took ', time.clock() - starttime
        return x, y

def main():
    ''' this is REQUIRED for Qt applications '''
    app = QApplication(sys.argv)
    ''' run the mainWindow main window'''
    ex = mainWindow()
    ''' show the application - REQUIRED to see anything... '''
    ex.show()
    ''' This is REQUIRED to stop the application from quitting straight away '''
    sys.exit(app.exec_())

if __name__ == '__main__':
   main()
