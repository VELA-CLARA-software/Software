import sys, time, os, datetime
# import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
# import numpy as np
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

class recordWorker(QtCore.QObject):
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
            del self.records[self.name]['data'][0:cutlength]
        self.records[self.name]['data'].append(value)
        # print len(self.records[self.name]['data'])

class createSignalRecord(QObject):

    def __init__(self, records, name, pen, timer, maxlength, function, arg=[], functionForm=None, functionArgument=None, logscale=False, VerticalScale=1, VerticalOffset=0, verticalMeanSubtraction=False):
        # Initialize the PunchingBag as a QObject
        QObject.__init__(self)
        self.records = records
        self.records[name] = {'name': name, 'pen': pen, 'timer': timer, 'maxlength': maxlength, 'function': function, 'arg': arg, 'ploton': True, 'data': [], 'functionForm': functionForm, 'functionArgument': functionArgument, 'logscale': logscale, 'VerticalScale': VerticalScale, 'VerticalOffset': VerticalOffset, 'verticalMeanSubtraction': verticalMeanSubtraction}
        self.name = name
        self.signal = createSignalTimer(name, function, arg=arg)
        self.thread = QtCore.QThread()
        self.worker = recordWorker(self.records, self.signal, name)
        self.worker.moveToThread(self.thread)
        self.thread.start()
        self.signal.startTimer(timer)

    def setInterval(self, newinterval):
        self.signal.timer.setInterval(newinterval)

    def stop(self):
        self.signal.timer.stop()

    def close(self):
        self.stop()
        self.thread.quit()
        self.thread.wait()
