# pyqtgraph examples : bar chart
# pythonprogramminglanguage.com
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

win = pg.plot()
win.setWindowTitle('pyqtgraph BarGraphItem')

# create list of floats
y1 = np.linspace(0, 20, num=3)

# create horizontal list
x = np.arange(3)

# create bar chart
bg1 = pg.BarGraphItem(x=x, height=y1, width=[0.6,0.2,1], pen='r', brush='b')
bg2 = pg.BarGraphItem(x=x, height=y1, width=[0.3,0.1,0.5], pen='g',brush=None, brushes=None)

win.addItem(bg1)
win.addItem(bg2)
## Start Qt event loop unless running in interactive mode or using
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
