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
try:
    from PyQt5.QtCore import *
    from  PyQt5.QtGui import *
    from  PyQt5.QtWidgets import *
except:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
# import pyqtgraph as pg
import numpy as np

# from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
# from matplotlib.backends.backend_qt5agg import (
#         FigureCanvas, NavigationToolbar2QT as NavigationToolbar)

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


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

        self.tabWidget.addTab(plotWidget(),"Plotting")

''' This is a QWidget that contains some plots'''
class plotWidget(QWidget):
    def __init__(self, parent=None):
        super(plotWidget, self).__init__(parent)
        '''We can add widgets inside this widget using a layout'''
        self.layout = QVBoxLayout()
        '''This sets the layout into the widget'''
        self.setLayout(self.layout)

        '''lets add some plots'''
        self.plots = {}
        self.randomData = {}
        ''' we store references to the plots, so we can reference them later... '''
        for i in range(3):
            self.plots[i] = plot(i)
            self.randomData[i] = createRandomData()
            ''' Here we add each plot to the LAYOUT of the main WIDGET '''
            self.layout.addWidget(self.plots[i])
            ''' This connects the random data SIGNAL "dataReady" to the function of the plot called "newReading" '''
            self.randomData[i].dataReady.connect(self.plots[i].newReading)

''' This is an object to create some random data'''
class createRandomData(QObject):

    ''' this is a SIGNAL, which EMITS data to whoever is listening'''
    dataReady = pyqtSignal(int, float)

    def __init__(self, parent=None):
        super(createRandomData, self).__init__(parent)
        self.no = 0
        ''' this creates a simple timer in Qt'''
        self.timer = QTimer()
        ''' every time the timer has finished it EMITS a "timeout" signal, and here we connect to that to fire our SIGNAL'''
        self.timer.timeout.connect(self.emitData)
        ''' this sets the time delay in the timer in milliseconds'''
        self.timer.start(100)

    def emitData(self):
        ''' the function is called every time the TIMER fires, and we use it to EMIT our signal'''
        self.dataReady.emit(self.no, random.random())
        self.no += 1

''' This is a plotting widget from pyqtgraph '''
class plot(QWidget):
    def __init__(self, no=0, parent=None):
        super(plot, self).__init__(parent)
        ''' this add a plot to the plotWidget'''
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)
        self._dynamic_ax = self.figure.add_subplot(111)
        self.data = np.empty((0,2),int)
        ''' This make a color, indexed by integer no'''
        # self.color = pg.mkColor(no)
        ''' this adds a plotItem to the plot - this is basically a independent plot line - we could have many of these '''
        ''' Note we don't have to give it data, we can just define the pen color for later '''
        # self.curve = self.plotItem.plot(pen=self.color)


    def reset(self):
        self.data = np.empty((0,2),int)
        self.bpmPlot.clear()

    def newReading(self, x, y):
        ''' this is called with the output of the random functions SIGNAL "dataReady", whihch emits an int and a float '''
        ''' this is one (not very good way) of adding some data to the self.data list '''
        self.data = np.append(self.data, [[x,y]], axis=0)
        _x, _y = zip(*self.data)
        ''' this sets the data to the plot, and updates the plot '''
        self._dynamic_ax.clear()
        # Shift the sinusoid as a function of time.
        self._dynamic_ax.plot(_x, _y)
        self._dynamic_ax.figure.canvas.draw()

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
