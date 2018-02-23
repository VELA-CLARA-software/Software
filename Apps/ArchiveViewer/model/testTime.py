import sys
import numpy as np
import datetime

from PyQt4.QtCore import QTime, QTimer
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

from collections import deque

import pytz
UNIX_EPOCH_naive = datetime.datetime(1970, 1, 1, 0, 0) #offset-naive datetime
UNIX_EPOCH_offset_aware = datetime.datetime(1970, 1, 1, 0, 0, tzinfo = pytz.utc) #offset-aware datetime
UNIX_EPOCH = UNIX_EPOCH_naive

TS_MULT_us = 1e6

def now_timestamp(ts_mult=TS_MULT_us, epoch=UNIX_EPOCH):
    return(int((datetime.datetime.utcnow() - epoch).total_seconds()*ts_mult))

def int2dt(ts, ts_mult=TS_MULT_us):
    return(datetime.datetime.utcfromtimestamp(float(ts)/ts_mult))

def dt2int(dt, ts_mult=TS_MULT_us, epoch=UNIX_EPOCH):
    delta = dt - epoch
    return(int(delta.total_seconds()*ts_mult))

def td2int(td, ts_mult=TS_MULT_us):
    return(int(td.total_seconds()*ts_mult))

def int2td(ts, ts_mult=TS_MULT_us):
    return(datetime.timedelta(seconds=float(ts)/ts_mult))

class TimeAxisItem(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        super(TimeAxisItem,self).__init__(*args, **kwargs)

    def tickStrings(self, values, scale, spacing):
        # PySide's QTime() initialiser fails miserably and dismisses args/kwargs
        #return [QTime().addMSecs(value).toString('mm:ss') for value in values]
        return [int2dt(value).strftime("%H:%M:%S.%f") for value in values]

class MyApplication(QtGui.QApplication):
    def __init__(self, *args, **kwargs):
        super(MyApplication, self).__init__(*args, **kwargs)
        self.t = QTime()
        self.t.start()

        maxlen = 200
        self.data_x = deque(maxlen=maxlen)
        self.data_y = deque(maxlen=maxlen)

        self.win = pg.GraphicsWindow(title="Basic plotting examples")
        self.win.resize(1000,600)

        self.plot = self.win.addPlot(title='Timed data', axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        #self.plot.setYRange(0, 150)
        self.curve = self.plot.plot()

        self.tmr = QTimer()
        self.tmr.timeout.connect(self.update)
        self.tmr.start(100)

        self.y = 100

    def update(self):
        #self.data.append({'x': self.t.elapsed(), 'y': np.random.randint(0, 100)})
        x = now_timestamp()
        self.y = self.y + np.random.uniform(-1, 1)

        self.data_x.append(x)
        self.data_y.append(self.y)
        self.curve.setData(x=list(self.data_x), y=list(self.data_y))

def main():
    app = MyApplication(sys.argv)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
