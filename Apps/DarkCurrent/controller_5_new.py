# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 10:40:30 2019

@author: qqi63789
"""
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore
import time, traceback, sys, csv

import view_5 as view
import model_5 as model

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
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(float, float, float, float, float, float)
    result_fn = pyqtSignal(object)
    progress = pyqtSignal(float)
    current_val = pyqtSignal(float, float, float)

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

    def __init__(self, fn1, fn2, arg1, arg2, arg3, out1, out2, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.fn1 = fn1
        self.fn2 = fn2
        self.out1 = out1
        self.out2 = out2
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()    

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress
        self.kwargs['result_callback'] = self.signals.result  
        self.kwargs['current_val_callback'] = self.signals.current_val

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        
        # Retrieve args/kwargs here; and fire processing using them
        try:
            result_fn = self.fn1(self.fn2, self.arg1, self.arg2, self.arg3, self.out1, self.out2, *self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result_fn.emit(result_fn)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done

#=========================================================================================================================================================================
class controller(object):
    
    def __init__(self, view, model):
         # button function
        #self.buttonBox.accepted.connect(self.Dialog.accept)
        #self.view = view
        #self.model = model
        
        #self.v = self.view.MainWindow()
        
        print 'YESSSSS'
        
        app = QApplication([])
        self.window = view.MainWindow()
        self.output = view.classprogress()
        self.model = model.classmachine()
        
        #self.window.buttonBox.accepted.connect(self.window.Dialog.accept)
        self.window.buttonBox.clicked.connect(self.okClicked)
        #self.window.buttonBox.rejected.connect(self.window.Dialog.reject)
        
        #self.window.buttonBox_2.accepted.connect(self.window.Dialog.accept)
        self.window.buttonBox_2.clicked.connect(self.close_window)
        #self.window.buttonBox_2.rejected.connect(self.window.Dialog.reject)
        
        print 'NOOOOOOO'
        
        app.exec_()
        
        
        #self.window.Dialog.show()

    def okClicked(self):
        """cannot take any other imput than self. It's basically a slot """
        #opening the live output GUI
        self.output.show()
        
        # creating arrays with my variables that I'll then feed to my function
        sol_val = [self.window.min_sol.value(), self.window.step_sol.value(), self.window.max_sol.value()]
        bsol_val = [self.window.min_bsol.value(), self.window.step_bsol.value(), self.window.max_bsol.value()]
        rf_val = [self.window.min_rf.value(), self.window.step_rf.value(), self.window.max_rf.value()]
        #self.Dialog.close()
        self.create_logfile()
        self.threadpool = QtCore.QThreadPool.globalInstance()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        self.fn_worker(self.model.loop, self.model.set_sol, sol_val, bsol_val, rf_val)
        
    def create_logfile(self):
        with open(path_csv, 'w') as f :
            fieldnames = ['SOL', 'BSOL', 'CHARGE', 'HCOR01', 'VCOR01', 'RF amp']  
            thewriter = csv.DictWriter(f, fieldnames = fieldnames)
            thewriter.writeheader()
    
    def close_window(self):
        self.window.Dialog.close()
        sys.exit()    
        
    def progress_fn(self, n):
        print("%d%% done" % n)
        self.output.progress_bar(n)

#    def execute_this_fn(self, progress_callback, result_callback):
#        for n in range(0, 5):
#            time.sleep(1)
#            progress_callback.emit(n*100/4)
#        return 7,7,7
        
    def print_output(self, s, t, u, v, w, x):
        #print s, t, u
        #self.output.retranslateUi(s,t)
        with open(path_csv, 'ab') as f:
            thewriter = csv.writer(f)
            thewriter.writerow([s, t, u, v, w, x])
        print 'Data saved'
        print '\n'
    
    def update_text_fn(self, sol, bsol, rf):
        self.output.retranslateUi(sol, bsol, rf)
        
    def thread_complete(self):
        print("THREAD COMPLETE!")
        self.output.finished()
 
    def fn_worker(self, fn_loop, fn_sweep, sol_val, bsol_val, rf_val):
        # Pass the function to execute
#        sol_val = [-1,2,1] 
#        bsol_val = [-1,2,1] 
#        rf_val = [70,1,70]                                                  # closing the window so it doesn't give a 'not responding' error
        
        #model.classmachine()
        #self.model_machine.check_if_ON()
        
        worker = Worker(fn_loop, fn_sweep, sol_val, bsol_val, rf_val, self.output.retranslateUi, self.output.progress_bar) # Any other args, kwargs are passed to the run function
        #worker = Worker(self.execute_this_fn)
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)
        worker.signals.current_val.connect(self.update_text_fn)
        # Execute
        self.threadpool.start(worker) 

#m = classmachine()
#        m.check_if_ON()
#app = QApplication([])
#window = MainWindow()
#app.exec_()
path_csv = ('Documents\\VirtualAccelerator\\app5\\DC_data.csv')      
c = controller(view, model)