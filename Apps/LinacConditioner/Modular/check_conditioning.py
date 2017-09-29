import time, epics, numpy
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class check_conditioning(QObject):

    alarm_Signal = pyqtSignal(bool)

    def __init__(self, pv=None, frequency=10, parent=None, alarm_value=None):
        super(check_conditioning, self).__init__()
        self.pv_to_monitor = epics.PV(pv)
        self.alarm = alarm_value
        self.inAlarmState = False
        self.timer = QTimer()
        self.setFrequency(frequency)

    def setFrequency(self, frequency):
        self.frequency = frequency
        self.timeout = 1000.0/self.frequency
        self.timer.start(self.timeout)

    def setAlarm(self, output=None):
        if not output == None:
            print time.strftime("%a, %d %b %Y %H:%M:%S") + ' alarm = ' + output
        self.inAlarmState = True
        self.alarm_Signal.emit(self.inAlarmState)
        self.alarmStart = time.time()

    def clearAlarm(self):
        if self.inAlarmState:
            self.inAlarmState = False
            self.alarm_Signal.emit(self.inAlarmState)

    def getLatestValue(self):
        self.latest_values = self.pv_to_monitor.get()
        if len(self.latest_values) > 1:
            self.max = max(self.latest_values)
            self.min = min(self.latest_values)

    def updateMean(self):
        pass

    def keyPressEvent(self, event):
        key = event.key()
        modifiers = QtGui.QApplication.keyboardModifiers()
        print 'key = ', key
        if modifiers == Qt.ControlModifier and key == Qt.Key_C:
            exit()

class check_conditioning_buffer(check_conditioning):

    def __init__(self, bufferLength=10, *args, **kwargs):
        super(check_conditioning_buffer, self).__init__(*args, **kwargs)
        self.bufferlength = bufferLength
        self.buffer = []
        self.getInitialValues()

    def getInitialValues(self):
        self.mean = self.pv_to_monitor.get()
        self.maxmean = numpy.max(self.mean)
        for i in range(11):
            self.buffer.append(self.mean)

    def trimBuffer(self):
        if len(self.buffer) > self.bufferlength:
           self.buffer.pop(0)

    def updateMean(self):
        self.buffer.append(self.latest_values)
        self.trimBuffer()
        self.mean = numpy.mean(self.buffer)
        self.maxmean = numpy.max(self.mean)
