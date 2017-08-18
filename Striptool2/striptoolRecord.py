import sys, time, os, datetime
# import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy as np
import threading
from threading import Thread, Event, Timer
from PyQt4.QtCore import QObject, pyqtSignal, pyqtSlot

class repeatedTimer:

    """Repeat `function` every `interval` seconds."""

    def __init__(self, interval, function, *args, **kwargs):
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.start = 0 #time.time()
        self.event = Event()
        self.thread = threading.Thread(target=self._target)
        self.thread.daemon = True
        self.intervalChanged = False
        self.thread.start()

    def _target(self):
        while not self.event.wait(self._time):
            self.function(*self.args, **self.kwargs)

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

    dataReady = QtCore.pyqtSignal(list)

    def __init__(self, name, function, arg=[]):
        # Initialize the signal as a QObject
        QObject.__init__(self)
        self.function = function
        self.args = arg
        self.name = name

    def startTimer(self, interval=1):
        self.timer = repeatedTimer(interval, self.update)

    def update(self):
        ''' call signal generating Function '''
        value = self.function(*self.args)
        self.dataReady.emit([round(time.time(),2),value])

    def setInterval(self, interval):
        self.timer.stop()
        self.startTimer(interval)

class recordWorker(QtCore.QObject):

    recordMeanSignal = QtCore.pyqtSignal(float)
    recordStandardDeviationSignal = QtCore.pyqtSignal(float)
    recordMinSignal = QtCore.pyqtSignal(float)
    recordMaxSignal = QtCore.pyqtSignal(float)

    def __init__(self, records, signal, name):
        super(recordWorker, self).__init__()
        self.records = records
        self.signal = signal
        self.name = name
        self.signal.dataReady.connect(self.updateRecord)

    @QtCore.pyqtSlot(list)
    def updateRecord(self, value):
        # if len(self.records[self.name]['data']) > 1 and value[1] == self.records[self.name]['data'][-1][1] and value[1] == self.records[self.name]['data'][-2][1]:
        #     self.records[self.name]['data'][-1] = value
        # else:
        if len(self.records[self.name]['data']) > self.records[self.name]['maxlength']:
            cutlength = len(self.records[self.name]['data']) - self.records[self.name]['maxlength']
            self.records[self.name]['data'] = np.delete(self.records[self.name]['data'],range(cutlength),axis=0)
        if len(self.records[self.name]['data']) < 1:
            self.records[self.name]['data'] = np.array([value])
        else:
            self.records[self.name]['data'] = np.concatenate((self.records[self.name]['data'],[value]), axis=0)
        values = zip(*self.records[self.name]['data'])[1]
        self.recordMeanSignal.emit(np.mean(values))
        self.recordStandardDeviationSignal.emit(np.std(values))
        self.recordMinSignal.emit(np.min(values))
        self.recordMaxSignal.emit(np.max(values))

class SignalRecord(QObject):

    def __init__(self, records, name, pen, timer, maxlength, function, arg=[], functionForm=None, functionArgument=None, logScale=False, verticalRange=False, verticalMeanSubtraction=False):
        QObject.__init__(self)
        self.records = records
        self.name = name
        self.signal = createSignalTimer(name, function, arg=arg)
        self.records[name] = {'name': name, 'record': self, 'pen': pen, 'timer': timer, 'maxlength': maxlength, 'function': function, 'arg': arg, 'ploton': True, 'data': [],
        'functionForm': functionForm, 'functionArgument': functionArgument,
        'logScale': logScale, 'verticalRange': verticalRange, 'verticalMeanSubtraction': verticalMeanSubtraction, 'signal': self.signal, 'worker': None}
        self.thread = QtCore.QThread()
        self.worker = recordWorker(self.records, self.signal, name)
        self.records[name]['worker'] = self.worker
        self.worker.moveToThread(self.thread)
        self.thread.start()
        self.signal.startTimer(timer)

    def setInterval(self, newinterval):
        self.signal.setInterval(newinterval)

    def stop(self):
        self.signal.timer.stop()

    def close(self):
        self.stop()
        self.thread.quit()
        self.thread.wait()
