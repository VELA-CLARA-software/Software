import sys, time, os, datetime, math
import collections
# from pyqtgraph.Qt import QtGui, QtCore
try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
except ImportError:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
from threading import Thread, Event, Timer

class repeatedTimer(QObject):

    """Repeat `function` every `interval` seconds."""

    dataReady = pyqtSignal(list)

    def __init__(self, function, args=[]):
        QObject.__init__(self)
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

class createSignalTimer(QObject):

    def __init__(self, function, args=[]):
        # Initialize the signal as a QObject
        QObject.__init__(self)
        self.timer = repeatedTimer(function, args)

    def startTimer(self, interval=1):
        self.timer.setInterval(interval)
        self.timer.thread.start()

    def setInterval(self, interval):
        # self.timer.stop()
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
        self.records = records
        self.name = name
        self.timer = timer
        self.signal = createSignalTimer(function, args=args)
        self.records[name] = {'name': name, 'record': self, 'pen': pen, 'timer': timer, 'maxlength': maxlength, 'data': collections.deque(maxlen=maxlength),
         'function': function, 'args': args, 'functionForm': functionForm, 'functionArgument': functionArgument,
        'signal': self.signal, 'logScale': logScale, 'verticalRange': verticalRange,
        'axisname': axis}
        self.thread = QThread()
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
