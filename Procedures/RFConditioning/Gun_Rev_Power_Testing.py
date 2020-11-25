import epics, math, time, sys
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class RFTest(QMainWindow):

    def __init__(self):
        super(RFTest, self).__init__()

        self.plotWidget = pg.GraphicsLayoutWidget()
        self.plotFWD = self.plotWidget.addPlot(row=0, col=0)
        self.plotREV = self.plotWidget.addPlot(row=0, col=1)
        self.plotFWDRatio = self.plotWidget.addPlot(row=1, col=0,setRange=[0.9,1.1])
        self.plotREVRatio = self.plotWidget.addPlot(row=1, col=1,setRange=[0.9,1.1])
        self.plotFWDRatio.vb.disableAutoRange(axis='y')
        self.plotREVRatio.vb.disableAutoRange(axis='y')
        self.plotFWDRatio.vb.setLimits(yMin=0.7,yMax=2)
        self.plotREVRatio.vb.setLimits(yMin=0.7,yMax=2)
        self.curveFWD = self.plotFWD.plot()
        self.curveFWDMean = self.plotFWD.plot()
        self.curveFWDRatio = self.plotFWDRatio.plot()

        self.curveREV = self.plotREV.plot()
        self.curveREVMean = self.plotREV.plot()
        self.curveREVRatio = self.plotREVRatio.plot()

        self.setCentralWidget(self.plotWidget)

        self.fwd_power = epics.PV('CLA-GUN-LRF-CTRL-01:ad1:ch3:power_remote.POWER')
        self.rev_power = epics.PV('CLA-GUN-LRF-CTRL-01:ad1:ch4:power_remote.POWER')
        self.pulse_length = epics.PV('CLA-GUN-LRF-CTRL-01:vm:feed_fwd:duration')
    	self.llrf_time_pv = epics.PV('CLA-GUN-LRF-CTRL-01:app:time_vector')

        self.timevector = self.llrf_time_pv.get()
        self.llrf_check_width =  0.4
        self.llrf_end_offset    =  0.12
        self.llrf_pulse_offset = 0.75 # usec from start of llrf trace until RF ramps on

        self.new_pulse_length = self.pulse_length.get()
        print self.new_pulse_length
        self.llrf_time_stop   = self.llrf_pulse_offset + self.new_pulse_length - self.llrf_end_offset
        self.llrf_time_start  = self.llrf_pulse_offset
        self.llrf_index_start = self.get_LLRF_power_trace_index_at_time_t( self.llrf_time_start )
        self.llrf_index_stop  = self.get_LLRF_power_trace_index_at_time_t( self.llrf_time_stop  )

        # llrf_index_start = 0
        # llrf_index_stop = -1

        self.fwd_power_list = []
        self.rev_power_list = []
        self.new_fwd_value = self.get_power(self.fwd_power)[self.llrf_index_start:self.llrf_index_stop:1]
        self.new_rev_value = self.get_power(self.rev_power)[self.llrf_index_start:self.llrf_index_stop:1]

        self.curveFWD.setData({'x': self.timevector[self.llrf_index_start:self.llrf_index_stop:1], 'y': self.new_fwd_value}, pen='r')
        self.curveREV.setData({'x': self.timevector[self.llrf_index_start:self.llrf_index_stop:1], 'y': self.new_rev_value}, pen='b')

        for i in range(10):
            self.fwd_power_list.append(self.new_fwd_value)
            self.rev_power_list.append(self.new_rev_value)

        self.starttime = time.time()

    def get_power(self,pv):
      return pv.get()

    def get_LLRF_power_trace_index_at_time_t(self, t):
    	# the LLRF times
    	# return next( x[0] for x in enumerate( self.timevector ) if x[1] > t)
        return next(idx for idx, obj in enumerate(self.timevector) if obj > t)

    def runAnalysis(self):
        # print 'rep-rate = ', 1/(time.time()-self.starttime)
        self.starttime = time.time()
        if self.new_pulse_length != self.pulse_length.get():
            self.new_pulse_length = self.pulse_length.get()
            print self.new_pulse_length
            self.timevector = self.llrf_time_pv.get()
            self.llrf_time_stop   = self.llrf_pulse_offset + self.new_pulse_length - self.llrf_end_offset
            self.llrf_time_start  = self.llrf_pulse_offset
            self.llrf_index_start = self.get_LLRF_power_trace_index_at_time_t( self.llrf_time_start )
            self.llrf_index_stop  = self.get_LLRF_power_trace_index_at_time_t( self.llrf_time_stop  )

        self.all_fwd_value = self.get_power(self.fwd_power)
        self.new_fwd_value = self.all_fwd_value[self.llrf_index_start:self.llrf_index_stop:1]
        self.all_rev_value = self.get_power(self.rev_power)
        self.new_rev_value = self.all_rev_value[self.llrf_index_start:self.llrf_index_stop:1]

        self.mean_fwd_value = np.mean(self.fwd_power_list,0)
        self.mean_rev_value = np.mean(self.rev_power_list,0)
        self.max_fwd_value = max(self.mean_fwd_value/self.new_fwd_value)
        self.max_rev_value = max(self.mean_rev_value/self.new_rev_value)

        self.fwd_power_list.append(self.new_fwd_value)
        if len(self.fwd_power_list) > 10:
            self.fwd_power_list.pop(0)
        self.rev_power_list.append(self.new_rev_value)
        if len(self.rev_power_list) > 10:
            self.rev_power_list.pop(0)

        if self.max_fwd_value > 1.5 and min(self.new_fwd_value) > 1e6:
            print 'Breakdown on the FWD power? Max = ', self.max_fwd_value
        if self.max_rev_value > 1.5 and min(self.new_fwd_value) > 1e6:
            print 'Breakdown on the REV power? Max = ', self.max_rev_value

    def updatePlots(self):
        cuttimevector = self.timevector[self.llrf_index_start:self.llrf_index_stop:1]
        self.curveFWD.setData({'x': self.timevector, 'y': self.all_fwd_value}, pen='r')
        self.curveREV.setData({'x': self.timevector, 'y': self.all_rev_value}, pen='r')

        self.curveFWDMean.setData({'x': cuttimevector, 'y': self.mean_fwd_value}, pen='b')
        self.curveREVMean.setData({'x': cuttimevector, 'y': self.mean_rev_value}, pen='b')

        self.curveFWDRatio.setData({'x': cuttimevector, 'y': self.mean_fwd_value/self.new_fwd_value}, pen='b')
        self.curveREVRatio.setData({'x': cuttimevector, 'y': self.mean_rev_value/self.new_rev_value}, pen='b')

def main():
    app = QApplication(sys.argv)
    pg.setConfigOptions(antialias=True)
    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')
    # app.setStyle(QStyleFactory.create("plastique"))
    ex = RFTest()
    ex.show()
    timer = QTimer()
    timer.timeout.connect(ex.runAnalysis)
    timer.start(100)
    plottimer = QTimer()
    plottimer.timeout.connect(ex.updatePlots)
    plottimer.start(1000)
    sys.exit(app.exec_())

if __name__ == '__main__':
   main()
