import time, copy, sys, math
from epics import caget, caput, cainfo, PV
import numpy as np
sys.path.append("../../../")
import Software.Procedures.qt as qt
from collections import deque, OrderedDict
from six import string_types

def tablePrint(**kwargs):
    print ("{:<8} {:<15}".format('Key','Value'))
    for k, v in kwargs.items():
        print ("{:<8} {:<15}".format(k, v))

class PVObject(qt.QObject):

    newValue = qt.pyqtSignal(float, 'PyQt_PyObject', str)
    # newValue = pyqtSignal(float, list)
    # newValue = pyqtSignal(float, np.ndarray)

    def __init__(self, pv, readback=None, parent=None):
        super(PVObject, self).__init__()
        self.name = pv
        # print ('name = ', self.name)
        self.pv = PV(self.name, callback=self.callback)
        # print ('pv = ', self.pv)
        self.dict = OrderedDict()
        self._value = [time.time(), self.pv.get()]
        self.writeAccess = False
        self.readBackName = readback
        if not self.readBackName is None:
            self.readBackPV = PV(self.readBackName)

    def callback(self, **kwargs):
        self.dict = OrderedDict(kwargs)
        if 'status' in kwargs and 'value' in kwargs and self.dict['status'] is 0:
            if not 'timestamp' in kwargs:
                self.dict['timestamp'] = time.time()
            self._value = [self.dict['timestamp'], self.dict['value'], self.name]
            self.newValue.emit(*self._value)

    def setValue(self, value):
        self.value = value

    @property
    def value(self):
        if self._value[1] is None:
            return self.pv.get() if self.pv.get() is not None else 0
        else:
            return self._value[1]
    @value.setter
    def value(self, val):
        if self.writeAccess:
            self.put(val)

    @property
    def time(self):
        return self._value[0]

    def get(self):
        return self._value

    def getTime(self):
        return self._value[0]

    def getValue(self):
        return self._value[1] if self._value[1] is not None else 0

    def put(self, value):
        ntries = 0
        if self.writeAccess:
            self.pv.put(value)
            if not self.readBackName is None:
                rbkValue = self.readBackPV.get()
                while abs(rbkValue - self.value) > 0.001 and ntries < 10:
                    time.sleep(0.05)
                    rbkValue = self.readBackPV.get()
                    ntries += 1

class PVWaveform(PVObject):

    newValue = qt.pyqtSignal(float, list)
    length = 100

    def __init__(self, pv, readback=None, length=None, parent=None):
        super(PVWaveform, self).__init__(pv, readback, parent)
        self.length = length

    def callback(self, **kwargs):
        self.dict = OrderedDict(kwargs)
        if 'status' in kwargs and 'value' in kwargs and self.dict['status'] is 0:
            if not 'timestamp' in kwargs:
                timestamp = time.time()
            if self.length is None:
                self._value = [self.dict['timestamp'], list(self.dict['value'])]
            else:
                self._value = [self.dict['timestamp'], list(self.dict['value'][:self.length])]
            self.newValue.emit(*self._value)

class PVBuffer(PVObject):

    listFull = qt.pyqtSignal(str)

    def __init__(self, pv, maxlen=1024, parent=None):
        super(PVBuffer, self).__init__(pv=pv, parent = parent)
        self.maxlen = maxlen
        self._length = 0
        self.buffer = deque(maxlen=self.maxlen)
        self._count = 0
        self.reset()
        # self.buffer.append(self.pv.get())

    def callback(self, **kwargs):
        self.dict = OrderedDict(kwargs)
        if hasattr(self, 'sum_x1') and 'status' in kwargs and 'value' in kwargs and self.dict['status'] == 0:
            if not 'timestamp' in kwargs:
                timestamp = time.time()
            self._value = [self.dict['timestamp'], self.dict['value'], self.name]
            self.newValue.emit(*self._value)
            time, val, name = self._value
            self.buffer.append(self._value)
            self.length += 1
            if self.length % self.maxlen == 0:
                self.listFull.emit(self.name)
            self.sum_x1 += val
            self.sum_x2 += val**2
            if self._value[1] < self.minValue:
                self.minValue = float(self._value[1])
            if self._value[1] > self.maxValue:
                self.maxValue = float(self._value[1])

    def lastValue(self):
        return self._value[1]

    def get(self):
        return self.buffer

    @property
    def values(self):
        values = [a[1] for a in self.buffer]
        return values

    @property
    def length(self):
        return self._length
    @length.setter
    def length(self, val):
        self._length = val

    @property
    def mean(self):
        return self.sum_x1/self.length if self.length > 0 else 0

    @property
    def std(self):
        return math.sqrt((self.sum_x2 / self.length) - (self.mean*self.mean)) if self.length > 0 else 0

    @property
    def min(self):
        return self.minValue

    @property
    def max(self):
        return self.maxValue

    def reset(self):
        self.buffer = deque(maxlen=self.maxlen)
        self._length = 0
        self.minValue = sys.maxsize
        self.maxValue = -1*sys.maxsize
        self.sum_x1 = 0
        self.sum_x2 = 0

    @property
    def bufferLength(self):
        return self.maxlen
    @bufferLength.setter
    def bufferLength(self, value):
        self.maxlen = value
        _buffer = copy.deepcopy(self.buffer)
        self.buffer = deque(maxlen=self.maxlen)
        for i in _buffer:
            self.buffer.append(i)
