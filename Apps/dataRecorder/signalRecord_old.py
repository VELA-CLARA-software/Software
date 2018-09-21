import sys, time, os, datetime, math
import collections
from pyqtgraph.Qt import QtGui, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from threading import Thread, Event, Timer
import tables as tables

class repeatedTimer(QtCore.QObject):

    """Repeat `function` every `interval` seconds."""

    dataReady = QtCore.pyqtSignal(list)

    def __init__(self, function, args=[]):
        QtCore.QObject.__init__(self)
        self.function = function
        self.args = args
        self.start = time.time()
        self.start_accurate = time.clock()
        self.event = Event()
        self.thread = Thread(target=self._target)
        self.thread.daemon = True

    def update(self):
        ''' call signal generating Function '''
        value = self.function(*self.args)
        currenttime = self.start + (time.clock() - self.start_accurate)
        currenttime = time.time()
        self.dataReady.emit([round(currenttime,4),value])

    def _target(self):
        while not self.event.wait(self._time):
            self.update()

    @property
    def _time(self):
        if (self.interval) - ((time.time() - self.start) % self.interval) < 0.001:
            return self.interval
        else:
            return (self.interval) - ((time.time() - self.start) % self.interval)

    def stop(self):
        self.event.set()
        self.thread.join()

    def setInterval(self, interval):
        self.interval = interval

class createSignalTimer(QtCore.QObject):

    def __init__(self, function, args=[]):
        # Initialize the signal as a QtCore.QObject
        QtCore.QObject.__init__(self)
        self.timer = repeatedTimer(function, args)

    def startTimer(self, interval=1):
        self.timer.setInterval(interval)
        self.timer.thread.start()

    def setInterval(self, interval):
        # self.timer.stop()
        self.startTimer(interval)

class recordWorker(QtCore.QObject):

    recordLatestValueSignal = QtCore.pyqtSignal(list)
    recordMeanSignal = QtCore.pyqtSignal(float)
    recordMean10Signal = QtCore.pyqtSignal(list)
    recordMean100Signal = QtCore.pyqtSignal(list)
    recordMean1000Signal = QtCore.pyqtSignal(list)
    recordStandardDeviationSignal = QtCore.pyqtSignal(float)
    recordMinSignal = QtCore.pyqtSignal(float)
    recordMaxSignal = QtCore.pyqtSignal(float)
    nsamplesSignal = QtCore.pyqtSignal(int)

    def calculate_mean(self, numbers):
        return float(sum(numbers)) /  max(len(numbers), 1)

    def __init__(self, records, signal, name):
        super(recordWorker, self).__init__()
        self.records = records
        self.signal = signal
        self.name = name
        self.signal.timer.dataReady.connect(self.updateRecord)
        self.buffer = self.records[self.name]['data']
        self.buffer1000 = collections.deque(maxlen=1000)
        self.buffer100 = collections.deque(maxlen=100)
        self.buffer10 = collections.deque(maxlen=10)
        self.resetStatistics(True)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.emitStatistics)
        self.timer.start(1000)

    @QtCore.pyqtSlot(list)
    def updateRecord(self, value):
        self.buffer.append(value)
        self.recordLatestValueSignal.emit(value)
        time, val = value
        if isinstance(val,(int, float)):
            self.buffer10.append(val)
            self.buffer100.append(val)
            self.buffer1000.append(val)
            self.length += 1
            self.sum_x1 += val
            self.sum_x2 += val**2
            if val < self.min:
                self.min = float(val)
                self.recordMinSignal.emit(val)
            if val > self.max:
                self.max = float(val)
                self.recordMaxSignal.emit(val)
            self.recordMean10Signal.emit([time,self.calculate_mean(self.buffer10)])
            self.recordMean100Signal.emit([time,self.calculate_mean(self.buffer100)])
            self.recordMean1000Signal.emit([time,self.calculate_mean(self.buffer1000)])
            self.nsamplesSignal.emit(self.length)
        else:
            pass
            # print('Not a number! = ', self.name, val)

    def emitStatistics(self):
        length = self.length
        if length > 0:
            self.mean = self.sum_x1/length
            self.recordMeanSignal.emit(self.mean)
            if length > 2:
                if (self.sum_x2 / length) - (self.mean*self.mean) > 0:
                    self.stddeviation = math.sqrt((self.sum_x2 / length) - (self.mean*self.mean))
                else:
                    self.stddeviation = 0
                self.recordStandardDeviationSignal.emit(self.stddeviation)
        # if len(self.buffer10) > 0:
        #     self.recordMean10Signal.emit(self.calculate_mean(self.buffer10))
        #     self.recordMean100Signal.emit(self.calculate_mean(self.buffer100))
        #     self.recordMean1000Signal.emit(self.calculate_mean(self.buffer1000))

    def resetStatistics(self, value):
        if value is True:
            self.length = 0
            self.min = sys.maxsize
            self.max = -1*sys.maxsize
            self.mean = 0
            self.sum_x1 = 0
            self.sum_x2 = 0
            self.stddeviation = 0
            # self.buffer10.clear()
            # self.buffer100.clear()
            # self.buffer1000.clear()

class signalRecord(QtCore.QObject):

    def __init__(self, records, name, pen, timer, maxlength, function, args=[], functionForm=None, functionArgument=None, logScale=False, verticalRange=None, verticalMeanSubtraction=False, axis=None):
        QtCore.QObject.__init__(self)
        self.records = records
        self.name = name
        self.timer = timer
        self.signal = createSignalTimer(function, args=args)
        self.records[name] = {'name': name, 'record': self, 'pen': pen, 'timer': timer, 'maxlength': maxlength, 'data': collections.deque(maxlen=maxlength),
         'function': function, 'args': args, 'functionForm': functionForm, 'functionArgument': functionArgument,
        'signal': self.signal, 'logScale': logScale, 'verticalRange': verticalRange,
        'axisname': axis}
        self.thread = QtCore.QThread()
        self.worker = recordWorker(self.records, self.signal, name)
        self.records[name]['worker'] = self.worker
        self.worker.moveToThread(self.thread)

    def start(self):
        self.thread.start()
        self.signal.startTimer(self.timer)

    def setLogMode(self, mode):
        self.records[self.name]['logScale'] = mode

    def setInterval(self, newinterval):
        self.signal.setInterval(newinterval)

    def stop(self):
        self.signal.timer.stop()

    def close(self):
        self.stop()
        self.thread.quit()
        self.thread.wait()

class recordData(tables.IsDescription):
    time  = tables.Float64Col()     # double (double-precision)
    value  = tables.Float64Col()

class signalRecorderH5(QObject):

    def __init__(self, filename="test", flushtime=10):
        super(signalRecorderH5, self).__init__()
        self.records = {}
        _, file_extension = os.path.splitext(filename)
        if not file_extension in ['h5','hdf5']:
            filename = filename+".h5"
        self.h5file = tables.open_file(filename, mode = "a", title = filename)
        self.rootnode = self.h5file.get_node('/')
        if 'data' not in self.rootnode:
            self.group = self.h5file.create_group('/', 'data', 'Saved Data')
        else:
            self.group = self.h5file.get_node('/data')
            # print self.group
        self.tables = {}
        self.rows = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.flushTables)
        self.timer.start(1000*flushtime)

    def addSignal(self, name='', pen='', timer=1, maxlength=100, function=None, arg=[], **kwargs):
        sigrec = signalRecord(records=self.records, name=name, pen=pen, timer=timer, maxlength=maxlength, function=function, **kwargs)
        if not name in self.group:
            table = self.h5file.create_table(self.group, name, recordData, name)
            self.tables[name] = table
            table.cols.time.create_csindex()
        else:
            table = self.h5file.get_node('/data/'+name)
            self.tables[name] = table
            sigrec.worker.nsamples = table.nrows
        row = table.row
        self.rows.append(row)
        self.records[name]['signal'].timer.dataReady.connect(lambda x: self.addData(table, row,x))
        sigrec.start()

    def addData(self, table, row, x):
        row['time'], row['value'] = x
        row.append()
        #table.flush()

    def flushTables(self):
        for t in self.tables:
            self.tables[t].flush()

    def close(self):
        for n,r in self.records.iteritems():
            r['record'].close()
        self.flushTables()
        self.h5file.close()

    def closeEvent(self, event):
        self.close()

    def getDataTime(self, name='', start=None, stop=None, array=None):
        table = self.h5file.get_node('/data/'+name)
        start = -100 if start is None else start
        start = time.time() + start if start < 0 else start
        stop =  -1 if stop is None else stop
        stop = time.time() + stop if stop < 0 else stop
        data = [[row['time'], row['value']] for row in table.itersorted('time') if (start < row['time'] < stop)]
        return data

    def getDataSlice(self, name='', start=None, stop=None, array=None):
        table = self.h5file.get_node('/data/'+name)
        start = -100 if start is None else start
        start = table.nrows + start if start < 0 else start
        stop =  -1 if stop is None else stop
        stop = table.nrows + stop + 1 if stop < 0 else stop
        data = [[row['time'], row['value']] for row in table.itersorted('time', start=start, stop=stop)]
        return data
