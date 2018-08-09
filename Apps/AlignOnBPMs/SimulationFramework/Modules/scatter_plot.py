from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg

app = QtGui.QApplication([])
mw = QtGui.QMainWindow()
mw.resize(800,800)
mw.show()

class scatterPlot(object):
    def __init__(self, x=None, y=None):
        super(scatterPlot, self).__init__()
        self.view = pg.GraphicsLayoutWidget()  ## GraphicsView with GraphicsLayout inserted by default
        mw.setCentralWidget(self.view)

    def addPlot(self, row=0, col=0, x=None, y=None):
        plot = self.view.addPlot(row=row, col=col)
        self.setData(row, col, x, y)

    def setData(self, row=0, col=0, x=None, y=None):
        plot = self.view.getItem(row,col)
        splot = pg.ScatterPlotItem(size=10)
        splot.addPoints(x=x, y=y)
        plot.clear()
        plot.addItem(splot)
