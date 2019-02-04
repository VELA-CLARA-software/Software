import sys, time, os, datetime, math
import collections
import tables as tables
sys.path.append("../../../")
import Software.Procedures.qt as qt

class HighPrecisionWallTime(qt.QObject):
    def __init__(self, parent=None):
        super(HighPrecisionWallTime, self).__init__(parent)
        self.start()

    def time(self,):
        dc = time.clock()-self._clock_0
        if dc > 60:
            # print 'reset'
            self._wall_time_0 = time.time()
            self._clock_0 = time.clock()
            dc = 0
        return self._wall_time_0 + dc

    def elapsed(self):
        return time.clock()-self._clock_0

    def start(self):
        self._wall_time_0 = time.time()
        self._clock_0 = time.clock()

class repeatedTimer(qt.QThread):

    """Repeat `function` every `interval` seconds."""

    dataReady = qt.pyqtSignal(list)

    def __init__(self, function, args=[]):
        super(repeatedTimer, self).__init__()
        self.function = function
        self.args = args
        self.started.connect(self.startTimer)

    def update(self):
        ''' call signal generating Function '''
        if (self.stopwatch.elapsed()) < 0.0001:
            pass
        else:
            value = self.function(*self.args)
            currenttime = self.stopwatch.time()
            self.dataReady.emit([currenttime,value])

    def startTimer(self):
        self.timer = qt.QTimer(self)
        self.stopwatch = HighPrecisionWallTime(self)
        try:
            self.timer.setTimerType(qt.Qt.PreciseTimer)
        except:
            pass
        self.timer.timeout.connect(self.update)
        self.abstart = time.time()
        self.timer.start(1000.*self.interval)
        self.stopwatch.start()

    def run(self):
        self.exec_()

    def setInterval(self, interval):
        self.interval = 1*interval
        self.i = 1

class createSignalTimer(qt.QObject):

    def __init__(self, function, args=[]):
        # Initialize the signal as a QObject
        super(createSignalTimer, self).__init__()
        self.timer = repeatedTimer(function, args)

    def startTimer(self, interval=1):
        self.timer.setInterval(interval)
        self.timer.start(qt.QThread.TimeCriticalPriority)

    def setInterval(self, interval):
        # self.timer.stop()
        self.startTimer(interval)

class recordWorker(qt.QObject):

    recordLatestValueSignal = qt.pyqtSignal(list)
    recordMeanSignal = qt.pyqtSignal(float)
    recordMean10Signal = qt.pyqtSignal(list)
    recordMean100Signal = qt.pyqtSignal(list)
    recordMean1000Signal = qt.pyqtSignal(list)
    recordStandardDeviationSignal = qt.pyqtSignal(float)
    recordMinSignal = qt.pyqtSignal(float)
    recordMaxSignal = qt.pyqtSignal(float)
    nsamplesSignal = qt.pyqtSignal(int)

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
        self.timer = qt.QTimer()
        self.timer.timeout.connect(self.emitStatistics)
        self.timer.start(1000)

    @qt.pyqtSlot(list)
    def updateRecord(self, value):
        self.buffer.append(value)
        self.recordLatestValueSignal.emit(value)
        time, val = value
        self.buffer10.append(val)
        self.buffer100.append(val)
        self.buffer1000.append(val)
        self.length += 1
        self.nsamplesSignal.emit(self.length)
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

class signalRecord(qt.QObject):

    def __init__(self, records, name, pen, timer, maxlength, function, args=[], functionForm=None, functionArgument=None, logScale=False, verticalRange=None, verticalMeanSubtraction=False, axis=None):
        qt.QObject.__init__(self)
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
        self.thread = qt.QThread()
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

class recordData(tables.IsDescription):
    time  = tables.Float64Col()     # double (double-precision)
    value  = tables.Float64Col()

class signalRecorderH5(qt.QObject):

    def __init__(self, filename="test", flushtime=1):
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
        self.timer = qt.QTimer()
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
