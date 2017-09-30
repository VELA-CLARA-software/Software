import sys, time, os, signal
try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
except:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
import logging
from signalRecord import *
import scrollingPlot as scrollingplot
import scatterPlot as scatterplot
import fftPlot as fftplot
import plotLegend as plotlegend

logger = logging.getLogger(__name__)

signal.signal(signal.SIGINT, signal.SIG_DFL)

def curveUpdate(self, curve):
    curve.update()

def logthread(caller):
    print('%-25s: %s, %s,' % (caller, threading.current_thread().name,
                              threading.current_thread().ident))

class CustomException(Exception):
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return repr(self.parameter)

class generalPlot(QWidget):

    signalAdded = QtCore.pyqtSignal('QString')
    signalRemoved = QtCore.pyqtSignal('QString')

    def __init__(self, parent = None):
        super(generalPlot, self).__init__(parent)
        self.paused = False
        self.timeOffset = 0

        ''' Create the signalRecord object '''
        self.records = {}

    def start(self, timer=1000):
        for name in self.records:
            self.records[name]['record'].start()

    def addSignal(self, name='', pen='r', timer=1, maxlength=pow(2,20), function=None, args=[], **kwargs):
        if not name in self.records:
            signalrecord = signalRecord(records=self.records, name=name, pen=pen, timer=timer, maxlength=maxlength, function=function, args=args, **kwargs)
            self.records[name]['record'] = signalrecord
            self.records[name]['parent'] = self
            self.signalAdded.emit(name)
            logger.info('Signal '+name+' added!')
        else:
            logger.warning('Signal '+name+' already exists!')

    def removeSignal(self,name):
        self.records[name]['record'].close()
        del self.records[name]
        self.signalRemoved.emit(name)
        logger.info('Signal '+name+' removed!')

    def setDecimateLength(self, value=5000):
        for name in self.records:
            self.records[name]['data'] = collections.deque(self.records[name]['data'], maxlen=value)

    def close(self):
        for name in self.records:
            self.records[name]['record'].close()

    def formatCurveData(self, name):
        # return [(str(time.strftime('%Y/%m/%d', time.localtime(x[0]))),str(datetime.datetime.fromtimestamp(x[0]).strftime('%H:%M:%S.%f')),x[1]) for x in self.records[name]['data']]
        return copy.copy(self.records[name]['data'])

    def saveAllCurves(self, saveFileName=False):
        if not saveFileName:
            saveFileName = str(QtGui.QFileDialog.getSaveFileName(self, 'Save Arrays', '', filter="CSV files (*.csv);; Binary Files (*.bin)", selectedFilter="CSV files (*.csv)"))
        if not saveFileName == None:
            for name in self.records:
                if self.records[name]['parent'] == self:
                    filename, file_extension = os.path.splitext(saveFileName)
                    saveFileName2 = filename + '_' + self.records[name]['name'] + file_extension
                    self.saveCurve(self.records[name]['name'],saveFileName2)

    def saveCurve(self, name, saveFileName=None):
        if saveFileName == None:
            saveFileName = str(QtGui.QFileDialog.getSaveFileName(self, 'Save Array ['+name+']', name, filter="CSV files (*.csv);; Binary Files (*.bin)", selectedFilter="CSV files (*.csv)"))
        filename, file_extension = os.path.splitext(saveFileName)
        saveData = self.formatCurveData(name)
        if file_extension == '.csv':
            # fmt='%s,%s,%.18e'
            fmt='%.11e,%.6e'
            target = open(saveFileName,'w')
            for row in saveData:
                target.write((fmt % tuple(row))+'\n')
            target.close()
        elif file_extension == '.bin':
            np.array(self.records[name]['data']).tofile(saveFileName)
        else:
            np.save(saveFileName,np.array(self.records[name]['data']))

    def scrollingPlot(self):
        self.scrollingplot = scrollingplot.scrollingPlot(generalplot=self)
        return self.scrollingplot

    def fftPlot(self):
        self.fftplot = fftplot.fftPlot(generalplot=self)
        return self.fftplot

    def scatterPlot(self):
        self.scatterplot = scatterplot.scatterPlot(generalplot=self)
        return self.scatterplot

    def legend(self):
        self.legend = plotlegend.plotLegend(generalplot=self)
        return self.legend

    def createAxis(self, *args, **kwargs):
        if hasattr(self,'scrollingplot'):
            self.scrollingplot.createAxis(*args, **kwargs)
        else:
            try:
                raise CustomException("Initialise scrollingPlot before use!")
            except CustomException, (instance):
                print "Caught: " + instance.parameter
