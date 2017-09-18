import sys, time, os, datetime
# import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy as np
import threading
from threading import Thread, Event, Timer
# from PyQt4.QtCore import QObject, pyqtSignal, pyqtSlot

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
        super(createSignalTimer, self).__init__()
        self.function = function
        self.args = arg
        self.name = name

    def startTimer(self, interval=1):
        self.timer = repeatedTimer(interval, self.update)

    def update(self):
        ''' call signal generating Function '''
        value = self.function(*self.args)
        if isinstance(value,float) or isinstance(value,int):
            self.dataReady.emit([round(time.time(),2),value])

    def setInterval(self, interval):
        self.timer.stop()
        self.startTimer(interval)

class recordWorker(QObject):

    recordMeanSignal = QtCore.pyqtSignal(float)
    recordStandardDeviationSignal = QtCore.pyqtSignal(float)
    recordMinSignal = QtCore.pyqtSignal(float)
    recordMaxSignal = QtCore.pyqtSignal(float)
    nsamplesSignal = QtCore.pyqtSignal(int)

    def __init__(self, records, signal, name):
        super(recordWorker, self).__init__()
        self.records = records
        self.signal = signal
        self.name = name
        self.nsamples = 0
        self.signal.dataReady.connect(self.updateRecord)

    @QtCore.pyqtSlot(list)
    def updateRecord(self, value):
        self.nsamples += 1
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
        self.nsamplesSignal.emit(self.nsamples)

class createSignalRecord(QObject):

    def __init__(self, records, name, pen, timer, maxlength, function, arg=[], functionForm=None, functionArgument=None, logscale=False, VerticalScale=1, VerticalOffset=0, verticalMeanSubtraction=False):
        super(createSignalRecord, self).__init__()
        self.records = records
        self.name = name
        self.signal = createSignalTimer(name, function, arg=arg)
        self.records[name] = {'name': name, 'record': self, 'pen': pen, 'timer': timer, 'maxlength': maxlength, 'function': function, 'arg': arg, 'ploton': True, 'data': [],
        'functionForm': functionForm, 'functionArgument': functionArgument,
        'logscale': logscale, 'VerticalScale': VerticalScale, 'VerticalOffset': VerticalOffset, 'verticalMeanSubtraction': verticalMeanSubtraction, 'signal': self.signal}
        self.thread = QThread()
        self.worker = recordWorker(self.records, self.signal, name)
        self.worker.moveToThread(self.thread)
        self.records[name]['worker'] = self.worker
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

import tables as tables

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
        if not os.path.exists(filename):
            self.group = self.h5file.create_group("/", 'data', 'Saved Data')
        else:
            self.group = self.h5file.get_node('/data')
            print self.group
        self.tables = []
        self.rows = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.flushTables)
        self.timer.start(1000*flushtime)

    def addSignal(self, name='', pen='', timer=1, maxlength=100, function=None, arg=[], **kwargs):
        sigrec = createSignalRecord(records=self.records, name=name, pen=pen, timer=timer, maxlength=maxlength, function=function, arg=arg, **kwargs)
        if not name in self.group:
            table = self.h5file.create_table(self.group, name, recordData, name)
            self.tables.append(table)
        else:
            table = self.h5file.get_node('/data/'+name)
            sigrec.worker.nsamples = table.nrows
        row = table.row
        self.rows.append(row)
        self.records[name]['signal'].dataReady.connect(lambda x: self.addData(row,x))

    def addData(self, row, x):
        row['time'], row['value'] = x
        row.append()

    def flushTables(self):
        for t in self.tables:
            t.flush()

    def closeEvent(self, event):
        print 'Close event!'
        for n,r in self.records.iteritems():
            r['signal'].close()
        self.flushTables()
