import sys, os
try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
except ImportError:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
import pyqtgraph as pg
import numpy as np
import random, time
sys.path.append(os.path.dirname( os.path.abspath(__file__)) + "/../../../")
from Software.Widgets.generic.pv import *
from Software.Widgets.QLabeledWidget import *
from Software.Widgets.typeCounter import *

pg.setConfigOptions(antialias=True)
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
from collections import OrderedDict
import yaml
import tables as tables


class recordWaveformData(tables.IsDescription):
    x  = tables.Float64Col()     # double (double-precision)
    y  = tables.Float64Col()

class klystronCalibrate(QMainWindow):
    def __init__(self, parent = None):
        super(klystronCalibrate, self).__init__(parent)
        self.widget = QWidget()
        # self.setCentralWidget(self.widget)
        self.gunKLYFWDPowerPV = PVObject('CLA-GUN-LRF-CTRL-01:ad1:ch1:power_remote.POWER')
        self.gunGUNFWDPowerPV = PVObject('CLA-GUN-LRF-CTRL-01:ad1:ch3:power_remote.POWER')
        self.ampPV = PVObject('CLA-GUN-LRF-CTRL-01:vm:dsp:sp_amp:amplitude')
        self.ampPV.writeAccess = False
        self.wavePlot = waveformPlot([self.gunKLYFWDPowerPV,self.gunGUNFWDPowerPV])
        # self.wavePV.newValue.connect(self.wavePlot.newWaveform)
        self.h5file = tables.open_file('klystron_ampset.h5', mode = "w", title = 'Klystron vs amp set')
        self.rootnode = self.h5file.get_node('/')

        self.layout = QVBoxLayout()

        self.readbackBox = QHBoxLayout()

        self.ampReadBack = QLabeledWidget(QLineEdit(),'Amp Set: ')
        self.ampReadBack.widget.setText(str(self.ampPV.value))
        self.ampPV.newValue.connect(lambda x,y: self.ampReadBack.widget.setText(str(y)))

        self.klystronReadBack = QLabeledWidget(QLineEdit(),'Kly Max: ')
        self.klystronReadBack.widget.setText(str(max(self.gunKLYFWDPowerPV.value)))
        self.gunKLYFWDPowerPV.newValue.connect(lambda x,y: self.klystronReadBack.widget.setText(str(max(y))))

        self.readbackBox.addWidget(self.ampReadBack)
        self.readbackBox.addWidget(self.klystronReadBack)

        self.layout.addLayout(self.readbackBox)
        self.layout.addWidget(self.wavePlot)

        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)
        # self.scanAmp()

    def scanAmp(self):
        self.ampranges = np.arange(100,16301,100)
        self.i = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.changeAmp)
        self.counter = typeCounter()
        self.gunKLYFWDPowerPV.newValue.connect(self.savePlotData)
        self.timer.start(1*1000)

    def changeAmp(self):
        self.ampPV.put(self.ampranges[self.i])
        time.sleep(0.5)
        # print 'amp = ', self.ampranges[self.i]
        if self.i+1 >= len(self.ampranges):
            self.timer.stop()
            sys.exit()
        self.i += 1

    def savePlotData(self, time, data=None):
        amp = str(int(self.ampPV.value))
        if not '/set_'+amp in self.h5file:
            self.group = self.h5file.create_group('/', 'set_'+amp, 'set_'+amp)
        data = self.wavePV.value
        no = self.counter.add(amp)
        print 'no = ', no
        table = self.h5file.create_table(self.group, 'no_'+str(no), recordWaveformData, 'set = '+str(amp)+', no = '+str(no))
        row = table.row
        data = self.wavePlot.data
        self.saveRow(row, data)
        table.flush()

    def saveRow(self, row, data):
        for x, y in data:
            row['x'], row['y'] = x, y
            row.append()

class waveformPlot(pg.PlotWidget):
    def __init__(self, pv=None, parent=None):
        super(waveformPlot, self).__init__(parent)
        if not isinstance(pv,(list,tuple)):
            self.pv = [pv]
        else:
            self.pv = pv
        self.plotItem = self.getPlotItem()
        self.plotItem.showGrid(x=True, y=True)
        self.plots = {}
        self.data = {}
        for i, p in enumerate(self.pv):
            name = p.name
            print name
            plot = self.plotItem.plot(pen=pg.mkColor(i))
            self.plots[name] = plot
            p.newValue.connect(self.newWaveform)
        print self.plots
        self.plotItem.setYRange(0,10e6)

    def newWaveform(self, time, data, name):
        name = str(name)
        x = range(len(data))
        y = data
        self.data[name] = np.array(zip(x,y))
        self.plots[name].setData(self.data[name])

def main():
    global app
    app = QApplication(sys.argv)
    ex = klystronCalibrate()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
   main()
