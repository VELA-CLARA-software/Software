"""
Control for the ADC raw live plot

@author: MFurmaniak
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore
import time, traceback, sys, csv
import yaml
import pyqtgraph as pg
from datetime import date

import ADC_raw_view as view
import ADC_raw_model as model

#=========================================================================================================================================================================
class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data
    
    error
        `tuple` (exctype, value, traceback.format_exc() )
    
    result
        `object` data returned from processing, anything

    progress
        `int` indicating % progress 

    '''
    error = pyqtSignal(tuple)
    result = pyqtSignal(object, float)
    result_fn = pyqtSignal(object)

#=========================================================================================================================================================================
class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and 
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()    

        # Add the callback to our kwargs
        self.kwargs['result_callback'] = self.signals.result  

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        
        # Retrieve args/kwargs here; and fire processing using them
        try:
            result_fn = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result_fn.emit(result_fn)  # Return the result of the processing

#=========================================================================================================================================================================
class controller(object):
    myspot = []
    
    def __init__(self):
        # you create your app
        app = QApplication([])
            
        self.model = model.model()
        self.graph = view.graph()
        
        self.graph.show()
        self.graph.closeEvent = self.closeEvent
        self.fn_worker(self.model.run)

        # you execute your app
        app.exec_()   
            
    def closeEvent(self, event):
        #print("event")
        reply = QtGui.QMessageBox.question(self.gui, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
            sys.exit()
        else:
            event.ignore()
            
    def fn_worker(self, function):
        # create global instance of QThreadPool
        self.threadpool = QThreadPool()
        
        # Pass the function to execute
        worker = Worker(function) # Any other args, kwargs are passed to the run function
        
        worker.signals.result.connect(self.print_output)
        
        # Execute
        self.threadpool.start(worker) 
        
    def print_output(self, points, charge):
        self.add_point(points)
        self.graph.retranslateUi_now(charge)

    def add_point(self, points):
        self.graph.s3.setData(points)


c = controller()        
