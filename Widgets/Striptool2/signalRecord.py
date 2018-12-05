import sys, time, os, datetime, math
import collections
import tables as tables
# from pyqtgraph.Qt import QtGui, QtCore
try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
except ImportError:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *

class HighPrecisionWallTime(QObject):
    def __init__(self, parent=None):
        super(HighPrecisionWallTime, self).__init__(parent)
        self.start()

    def time(self,):
        dc = time.clock()-self._clock_0
        return self._wall_time_0 + dc

    def elapsed(self):
        return time.clock()-self._clock_0

    def start(self):
        self._wall_time_0 = time.time()
        self._clock_0 = time.clock()

class repeatedTimer(QThread):

    """Repeat `function` every `interval` seconds."""

    dataReady = pyqtSignal(list)

    def __init__(self, function, args=[]):
        super(repeatedTimer, self).__init__()
        self.function = function
        self.args = args
        self.started.connect(self.startTimer)

    def update(self):
        ''' call signal generating Function '''
        value = self.function(*self.args)
        currenttime = self.starttime + self.stopwatch.elapsed()/1000.
        self.dataReady.emit([currenttime,value])

    def startTimer(self):
        self.timer = QTimer(self)
        try:
            self.timer.setTimerType(Qt.PreciseTimer)
        except:
            pass
        self.timer.timeout.connect(self.update)
        self.timer.start(1000.*self.interval)

    def run(self):
        self.exec_()

    def setInterval(self, interval):
        self.interval = 1*interval
        self.i = 1

    def setTimers(self, starttime, stopwatch):
        self.starttime = starttime
        self.stopwatch = stopwatch

class createSignalTimer(QObject):

    def __init__(self, function, args=[]):
        # Initialize the signal as a QObject
        super(createSignalTimer, self).__init__()
        self.timer = repeatedTimer(function, args)
        self.stopwatch = QTime()
        self.resetwatchTimer = QTimer(self)
        self.resetwatchTimer.timeout.connect(self.resetwatch)
        self.resetwatchTimer.start(1*1000)

    def resetwatch(self):
        if abs((time.time() - self.starttime) % self.interval) > self.interval/10.0:
            # print ('resetting stopwatch!  ', abs((time.time() - self.starttime) % self.interval))
            self.starttime = time.time()
            self.timer.starttime = self.starttime
            self.stopwatch.restart()
        else:
            pass
            # print 'timer difference = ', abs((time.time() - self.starttime) % self.interval)

    def startTimer(self, interval=1):
        self.interval = interval
        self.starttime = time.time()
        self.stopwatch.start()
        self.timer.setInterval(interval)
        self.timer.setTimers(self.starttime, self.stopwatch)
        self.timer.start(QThread.TimeCriticalPriority)

    def setInterval(self, interval):
        self.interval = interval
        self.startTimer(interval)

class recordWorker(QObject):

    recordLatestValueSignal = pyqtSignal(list)
    recordMeanSignal = pyqtSignal(float)
    recordMean10Signal = pyqtSignal(list)
    recordMean100Signal = pyqtSignal(list)
    recordMean1000Signal = pyqtSignal(list)
    recordStandardDeviationSignal = pyqtSignal(float)
    recordMinSignal = pyqtSignal(float)
    recordMaxSignal = pyqtSignal(float)
    nsamplesSignal = pyqtSignal(int)

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
        self.timer = QTimer()
        self.timer.timeout.connect(self.emitStatistics)
        self.timer.start(1000)

    @pyqtSlot(list)
    def updateRecord(self, value):
        self.buffer.append(value)
        self.recordLatestValueSignal.emit(value)
        time, val = value
        self.length += 1
        self.nsamplesSignal.emit(self.length)
        if isinstance(val, (int, float)):
            self.buffer10.append(val)
            self.buffer100.append(val)
            self.buffer1000.append(val)
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

class signalRecord(QObject):

    def __init__(self, records, name, pen, timer, maxlength, function, args=[], functionForm=None, functionArgument=None, logScale=False, verticalRange=None, verticalMeanSubtraction=False, axis=None):
        QObject.__init__(self)
        self.record = self
        records[name] = self.record
        self.name = name
        self.timer = timer
        self.signal = createSignalTimer(function, args=args)
        self.pen = pen
        self.timer = timer
        self.maxlength = maxlength
        self.data = collections.deque(maxlen=maxlength)
        self.function = function
        self.args = args
        self.functionForm = functionForm
        self.functionArgument = functionArgument
        self.logScale = logScale
        self.verticalRange = verticalRange
        self.axisname = axis
        self.thread = QThread()
        self.worker = recordWorker(records, self.signal, name)
        records[name].worker = self.worker
        self.worker.moveToThread(self.thread)

    def __getitem__(self, *args, **kwargs):
        return getattr(self, *args, **kwargs)

    def __setitem__(self, *args, **kwargs):
        setattr(self, *args, **kwargs)

    def start(self):
        self.thread.start()
        self.signal.startTimer(self.timer)

    def setLogMode(self, mode):
        self.logScale = mode

    def setInterval(self, newinterval):
        self.signal.setInterval(newinterval)

    def stop(self):
        self.signal.timer.stop()

    def close(self):
        self.stop()
        self.thread.quit()
        self.thread.wait()

class recordData2D(tables.IsDescription):
    time  = tables.Float64Col()     # double (double-precision)
    value  = tables.Float64Col()

class TooLongError(ValueError):
    pass

class signalRecorderH5(QObject):

    def __init__(self, filename="test", flushtime=1):
        super(signalRecorderH5, self).__init__()
        self.records = {}
        _, file_extension = os.path.splitext(filename)
        if not file_extension in ['h5','hdf5']:
            filename = filename+".h5"
        self.filename = filename
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

    def addSignal(self, name='', pen='', timer=1, arrayData=False, maxlength=100, function=None, arg=[], **kwargs):
        sigrec = signalRecord(records=self.records, name=name, pen=pen, timer=timer, maxlength=maxlength, function=function, **kwargs)
        if arrayData is not False:
            recordData = {'time': tables.Float64Col(), 'value': tables.Float64Col(shape=(arrayData,))}
        else:
            recordData = recordData2D
        if not name in self.group:
            print ('name = ', name)
            table = self.h5file.create_table(self.group, name, recordData, name)
            self.tables[name] = table
            table.cols.time.create_csindex()
        else:
            table = self.h5file.get_node('/data/'+name)
            self.tables[name] = table
            sigrec.worker.nsamples = table.nrows
        row = table.row
        self.rows.append(row)
        self.records[name]['signal'].timer.dataReady.connect(lambda x: self.addData(table, row, x, arrayData))
        sigrec.start()

    def pad(self, seq, target_length, padding=0):
        length = len(seq)
        if length > target_length:
            return seq[:target_length]
        else:
            seq.extend([padding] * (target_length - length))
            return seq

    def addData(self, table, row, x, arrayData=False):
        if arrayData is not False:
            row['time'] = x[0]
            row['value'] = self.pad(list(x[1]),arrayData)
        else:
            row['time'], row['value'] = x
        row.append()
        #table.flush()

    def flushTables(self):
        for t in self.tables:
            self.tables[t].flush()

    def close(self):
        try:
            for n,r in self.records.iteritems():
                r['record'].close()
            self.flushTables()
            self.h5file.close()
        except:
            pass

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
