import sys, os, math
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname( os.path.abspath(__file__)))))
from SimulationFramework.Framework import *
import SimulationFramework.Modules.read_beam_file as rbf
from pyqtgraph.Qt import QtGui, QtCore
beam = rbf.beam()
import SimulationFramework.Modules.scatter_plot as scatter

sp = scatter.scatterPlot()

beam.read_HDF5_beam_file('C2V/CLA-C2V-DIA-BPM-01.hdf5', local=False)
sp.addPlot(0,0,x=beam.x, y=beam.y)

beam.read_HDF5_beam_file('C2V/CLA-C2V-DIA-BPM-01.hdf5', local=True)
sp.addPlot(0,1,x=beam.x, y=beam.y)


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
