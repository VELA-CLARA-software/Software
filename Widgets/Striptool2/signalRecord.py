import sys, time, os, datetime, math
import collections
from pyqtgraph.Qt import QtGui, QtCore
try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
except:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
from threading import Thread, Event, Timer

class repeatedTimer(QObject):

    """Repeat `function` every `interval` seconds."""

    dataReady = QtCore.pyqtSignal(list)

    def __init__(self, function, args=[]):
        QObject.__init__(self)
        self.function = function
        self.args = args
        self.start = time.time()
        self.start_accurate = time.clock()
        self.event = Event()
        self.thread = Thread(target=self._target)
        self.thread.daemon = True
        self.intervalChanged = False

    def update(self):
        ''' call signal generating Function '''
        value = self.function(*self.args)
        currenttime = self.start + (time.clock() - self.start_accurate)
        self.dataReady.emit([round(currenttime,3),value])

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

class recordWorker(QtCore.QObject):

    recordLatestValueSignal = QtCore.pyqtSignal(list)
    recordMeanSignal = QtCore.pyqtSignal(float)
    recordStandardDeviationSignal = QtCore.pyqtSignal(float)
    recordMinSignal = QtCore.pyqtSignal(float)
    recordMaxSignal = QtCore.pyqtSignal(float)

    def __init__(self, records, signal, name):
        super(recordWorker, self).__init__()
        self.records = records
        self.signal = signal
        self.name = name
        self.signal.timer.dataReady.connect(self.updateRecord)
        self.buffer = self.records[self.name]['data']
        self.min = sys.maxsize
        self.max = -1*sys.maxsize
        self.mean = 0
        self.sum_x1 = 0
        self.sum_x2 = 0
        self.stddeviation = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.emitStatistics)
        self.timer.start(1000)

    @QtCore.pyqtSlot(list)
    def updateRecord(self, value):
        self.buffer.append(value)
        self.recordLatestValueSignal.emit(value)
        time, val = value
        self.sum_x1 += val
        self.sum_x2 += val**2
        if val < self.min:
            self.min = val
            self.recordMinSignal.emit(val)
        if val > self.max:
            self.max = val
            self.recordMaxSignal.emit(val)

    def emitStatistics(self):
        length = len(self.buffer)
        self.mean = self.sum_x1/length
        self.recordMeanSignal.emit(self.mean)
        self.stddeviation = math.sqrt((self.sum_x2 / length) - (self.mean*self.mean))
        self.recordStandardDeviationSignal.emit(self.stddeviation)

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
