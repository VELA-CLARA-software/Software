import sys, time, os, datetime
# import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
# import numpy as np
import threading
from threading import Thread, Event, Timer
from PyQt4.QtCore import QObject, pyqtSignal, pyqtSlot

class repeatedTimera:

    """Repeat `function` every `interval` seconds."""

    def __init__(self, interval, function, *args, **kwargs):
        self.interval = 1000*interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.thread = QtCore.QThread()
        self.worker = repeatedWorker(interval, function, *args, **kwargs)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.loop)
        self.thread.start()
        self.thread.setPriority(QThread.TimeCriticalPriority)

    def setInterval(self, interval):
        self.worker.setInterval(interval)

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

class repeatedWorker(QtCore.QObject):
    def __init__(self, interval, function, *args, **kwargs):
        super(repeatedWorker, self).__init__()
        self.interval = 1000.0*interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.prev = 1000.0*time.clock();

    def loop(self):
        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        newinterval = self.interval - ((1000.0*time.clock()) % self.interval)
        self.prev = 1000.0*time.clock()
        if newinterval < 0:
            self.timer.singleShot(0, self._target)
        else:
            self.timer.singleShot(newinterval, self._target)

    def stop(self):
        self.timer.stop()

    def _target(self):
        self.function(*self.args, **self.kwargs)
        newinterval = self.interval - ((1000.0*time.clock()) % self.interval)
        while newinterval < 0.2*self.interval:
            time.sleep(0.01)
            newinterval = self.interval - ((1000.0*time.clock()) % self.interval)
        self.timer.singleShot(newinterval, self._target)

    def setInterval(self, interval):
        self.interval = 1000*interval

class threadedFunction:

    """Repeat `function` every `interval` seconds."""

    def __init__(self, worker):
        self.interval = 1000*interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.thread = QtCore.QThread()
        self.worker = worker
        self.worker.moveToThread(self.thread)
        self.thread.start()

class createSignalTimer(QObject):

    dataReady = QtCore.pyqtSignal(list)

    def __init__(self, name, function, *args):
        # Initialize the signal as a QObject
        QObject.__init__(self)
        self.function = function
        self.args = args
        self.name = name

    def startTimer(self, interval=1):
        self.timer = repeatedTimer(interval, self.update)

    def update(self):
        ''' call signal generating Function '''
        value = self.function(*self.args)
        self.dataReady.emit([round(time.time(),2),value])

class recordWorker(QtCore.QObject):
    def __init__(self, records, signal, name):
        super(recordWorker, self).__init__()
        self.records = records
        self.signal = signal
        self.name = name
        self.list = self.records[self.name]['data']
        self.signal.dataReady.connect(self.updateRecord)

    @QtCore.pyqtSlot(list)
    def updateRecord(self, value):
        # if len(self.records[self.name]['data']) > 1 and value[1] == self.records[self.name]['data'][-1][1] and value[1] == self.records[self.name]['data'][-2][1]:
        #     self.records[self.name]['data'][-1] = value
        # else:
        self.records[self.name]['data'].append(value)
        # print len(self.records[self.name]['data'])

class createSignalRecord(QObject):

    def __init__(self, records, name, timer, function, *args):
        # Initialize the PunchingBag as a QObject
        QObject.__init__(self)
        self.records = records
        self.records[name] = {'name': name, 'pen': 'r', 'timer': timer, 'function': function, 'ploton': True, 'data': []}
        self.name = name
        self.signal = createSignalTimer(name, function, *args)
        self.thread = QtCore.QThread()
        self.worker = recordWorker(self.records, self.signal, name)
        self.worker.moveToThread(self.thread)
        self.thread.start()
        self.signal.startTimer(timer)

    def setInterval(self, newinterval):
        self.signal.timer.setInterval(newinterval)

    def stop(self):
        self.signal.timer.stop()
