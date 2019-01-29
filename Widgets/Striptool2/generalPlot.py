import time, signal, copy, sys
import os
import xlsxwriter
import datetime as dt
sys.path.append("../../../")
import Software.Procedures.qt as qt
import logging
import tables as tables
import signalRecord as signalRecord
import scrollingPlot as scrollingplot
import scatterPlot as scatterplot
import fftPlot as fftplot
import histogramPlot as histogramplot
import plotLegend as plotlegend
import numpy as np
logger = logging.getLogger(__name__)

class recordData(tables.IsDescription):
    time  = tables.Float64Col()     # double (double-precision)
    value  = tables.Float64Col()

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

class generalPlot(qt.QWidget):

    signalAdded = qt.pyqtSignal(str)
    signalRemoved = qt.pyqtSignal(str)

    def __init__(self, parent = None):
        super(generalPlot, self).__init__(parent)
        self.paused = False
        self.timeOffset = 0

        ''' Create the signalRecord object '''
        self.records = {}

    def start(self):
        for name in self.records:
            self.records[name]['record'].start()

    def addSignal(self, name='', pen='r', timer=1, maxlength=pow(2,16), function=None, args=[], **kwargs):
        if not name in self.records:
            signalrecord = signalRecord.signalRecord(records=self.records, name=name, pen=pen, timer=timer, maxlength=maxlength, function=function, args=args, **kwargs)
            self.records[name]['record'] = signalrecord
            self.records[name]['parent'] = self
            self.signalAdded.emit(str(name))
            logger.info('Signal '+name+' added!')
        else:
            logger.warning('Signal '+name+' already exists!')

    def removeRecord(self, name):
        del self.records[name]

    def removeSignal(self,name):
        self.records[name]['record'].close()
        self.signalRemoved.emit(str(name))
        qt.QTimer.singleShot(0, lambda: self.removeRecord(name))
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

    def saveAllData(self,saveFileName=False):
        if not saveFileName:
            today = dt.datetime.today()
            datetuple = today.timetuple()
            year, month, day, hour, minute = datetuple[0:5]
            month = str(month) if month >= 10 else '0' + str(month)
            day = str(day) if day >= 10 else '0' + str(day)
            hour = str(hour) if hour >= 10 else '0' + str(hour)
            minute = str(minute) if minute >= 10 else '0' + str(minute)
            suggestedfilename = str(year)+'_'+str(month)+'_'+str(day)+'_'+str(hour)+str(minute)+'_striptool_data'
            try:
                saveFileName = str(qt.QFileDialog.getSaveFileName(self, 'Save Data', suggestedfilename,
                filter="HDF5 files (*.h5);;XLSX files (*.xlsx);;CSV files (*.csv);; Binary Files (*.bin)", selectedFilter="HDF5 files (*.h5)"))
            except:
                saveFileName = str(qt.QFileDialog.getSaveFileName(self, 'Save Data', suggestedfilename,
                filter="HDF5 files (*.h5);;XLSX files (*.xlsx);;CSV files (*.csv);; Binary Files (*.bin)", initialFilter="HDF5 files (*.h5)")[0])
        _, file_extension = os.path.splitext(saveFileName)
        if file_extension == '.csv' or file_extension == '.bin':
            self.saveDataCSVBin(saveFileName)
        if file_extension == '.xlsx':
            self.saveDataXLSX(saveFileName)
        else:
            if not file_extension in ['.h5','.hdf5']:
                file_extension = '.h5'
                saveFileName = saveFileName+file_extension
            self.saveDataH5(saveFileName)

    def saveCurve(self, name):
        name = str(name)
        today = dt.datetime.today()
        datetuple = today.timetuple()
        year, month, day, hour, minute = datetuple[0:5]
        month = str(month) if month >= 10 else '0' + str(month)
        day = str(day) if day >= 10 else '0' + str(day)
        hour = str(hour) if hour >= 10 else '0' + str(hour)
        minute = str(minute) if minute >= 10 else '0' + str(minute)
        suggestedfilename = str(year)+'_'+str(month)+'_'+str(day)+'_'+str(hour)+str(minute)+'_'+name
        saveFileName = str(qt.QFileDialog.getSaveFileName(self, 'Save Data', suggestedfilename,
        filter="HDF5 files (*.h5);;XLSX files (*.xlsx);;CSV files (*.csv);; Binary Files (*.bin)", selectedFilter="HDF5 files (*.h5)"))
        _, file_extension = os.path.splitext(saveFileName)
        if file_extension == '.csv' or file_extension == '.bin':
            print ('file_extension = ', file_extension)
            self.saveCurveCSVBin(saveFileName, name)
        elif file_extension == '.xlsx':
            self.saveDataXLSX(saveFileName, name)
        else:
            if not file_extension in ['.h5','.hdf5']:
                file_extension = '.h5'
                saveFileName = saveFileName+file_extension
            self.saveDataH5(saveFileName, name)

    def saveDataH5(self, saveFileName, name=False):
        print ('saveFileName = ', saveFileName)
        self.h5file = tables.open_file(saveFileName, mode = "w", title = saveFileName)
        self.rootnode = self.h5file.get_node('/')
        self.group = self.h5file.create_group('/', 'data', 'Saved Data')
        if not name:
            records = self.records
        else:
            records = [name]
        for name in records:
            saveData = self.formatCurveData(name)
            table = self.h5file.create_table(self.group, name, recordData, name)
            row = table.row
            for x in saveData:
                row['time'], row['value'] = x
                row.append()
        self.h5file.close()

    def saveDataXLSX(self, saveFileName, name=False):
        workbook = xlsxwriter.Workbook(saveFileName)
        date_format = workbook.add_format({'num_format': 'dd/mm/yyyy'})
        time_format = workbook.add_format({'num_format': 'hh:mm:ss.000'})
        if not name:
            records = self.records
        else:
            records = [name]
        for name in records:
            saveData = self.formatCurveData(name)
            worksheet = workbook.add_worksheet(name)
            # Start from the first cell. Rows and columns are zero indexed.
            row = 0
            col = 0
            # Iterate over the data and write it out row by row.
            for time, val in (saveData):
                datetimetime = dt.datetime.fromtimestamp(time)
                worksheet.write_datetime(row, col, datetimetime, date_format)
                worksheet.write_datetime(row, col + 1, datetimetime, time_format)
                worksheet.write(row, col + 2, val)
                row += 1
        workbook.close()

    def saveDataCSVBin(self, saveFileName):
        for name in self.records:
            if self.records[name]['parent'] == self:
                filename, file_extension = os.path.splitext(saveFileName)
                saveFileName2 = filename + '_' + self.records[name]['name'] + file_extension
                self.saveCurveCSVBin(saveFileName2, self.records[name]['name'])

    def saveCurveCSVBin(self, saveFileName, name=False):
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

    def fftselectionchange(self, name, value):
        if hasattr(self,'fftplot'):
            self.fftplot.selectionChange(name, value)

    def histogramPlot(self):
        self.histogramplot = histogramplot.histogramPlot(generalplot=self)
        return self.histogramplot

    def histogramplotselectionchange(self, name, value):
        if hasattr(self,'histogramplot'):
            self.histogramplot.selectionChange(name, value)

    def scatterPlot(self):
        self.scatterplot = scatterplot.scatterPlot(generalplot=self)
        return self.scatterplot

    def legend(self):
        self.legend = plotlegend.plotLegend(generalplot=self)
        self.legend.tree.fftselectionchange.connect(self.fftselectionchange)
        self.legend.tree.histogramplotselectionchange.connect(self.histogramplotselectionchange)
        self.legend.tree.savecurve.connect(self.saveCurve)
        self.legend.pausePlottingSignal.connect(self.pausePlotting)
        return self.legend

    def pausePlotting(self, value):
        if hasattr(self,'histogramplot'):
            self.histogramplot.pausePlotting(value)
        if hasattr(self,'fftplot'):
            self.fftplot.pausePlotting(value)
        if hasattr(self,'scrollingplot'):
            self.scrollingplot.pausePlotting(value)


    def createAxis(self, *args, **kwargs):
        if hasattr(self,'scrollingplot'):
            self.scrollingplot.createAxis(*args, **kwargs)
