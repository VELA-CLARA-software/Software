# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 10:40:30 2019

@author: qqi63789
"""
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore
import time, traceback, sys, csv
import yaml
import pyqtgraph as pg
from datetime import date

import view as view
import model as model

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
    result = pyqtSignal(float, float, float, float, float, float, str)
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

    def __init__(self, fn1, fn2, arg1, arg2, arg3, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.fn1 = fn1
        self.fn2 = fn2
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
            result_fn = self.fn1(self.fn2, self.arg1, self.arg2, self.arg3, *self.args, **self.kwargs)
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
    
    myspot = []
    counter_runs = 0
    
    def __init__(self, view, model):
        app = QApplication([])
        self.window = view.MainWindow()
        self.output = view.classprogress()
        self.model = model.classmachine()
        self.graph = view.graph()
        
        
        #self.window.buttonBox.accepted.connect(self.window.Dialog.accept)
        self.window.buttonBox.clicked.connect(self.okClicked)
        #self.window.buttonBox.rejected.connect(self.window.Dialog.reject)
        
        self.window.buttonBox_2.accepted.connect(self.window.Dialog.accept)
        self.window.buttonBox_2.clicked.connect(self.close_window)
        self.window.buttonBox_2.rejected.connect(self.window.Dialog.reject)
        
        app.exec_()

    def okClicked(self):
        """cannot take any other imput than self. It's basically a slot """
        
        #opening the live output GUI
        self.output.show()
        
        if self.window.step_rf.value()==1:
            self.graph.show()
        
        # creating arrays with my variables that I'll then feed to my function
        sol_val = [self.window.min_sol.value(), self.window.step_sol.value(), self.window.max_sol.value()]
        bsol_val = [self.window.min_bsol.value(), self.window.step_bsol.value(), self.window.max_bsol.value()]
        rf_val = [self.window.min_rf.value(), self.window.step_rf.value(), self.window.max_rf.value()]
        #self.close_window()
        
        self.create_logfile()
        
        self.threadpool = QtCore.QThreadPool.globalInstance()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        self.fn_worker(self.model.loop, self.model.set_sol, sol_val, bsol_val, rf_val)
        
    def create_logfile(self):
        dict_file = []
        with open(path_yaml,'w') as file:
            document = yaml.safe_dump(dict_file, file)

#        with open(path_csv, 'w') as f :
#            fieldnames = ['SOL', 'BSOL', 'CHARGE', 'HCOR01', 'VCOR01', 'RF amp']  
#            thewriter = csv.DictWriter(f, fieldnames = fieldnames)
#            thewriter.writeheader()
   
    def close_window(self):
        self.window.Dialog.close()
        sys.exit()    
        
    def progress_fn(self, n):
        print("%d%% done" % n)
        self.output.progress_bar(n)
        
    def print_output(self, s, t, u, v, w, x, y):
        self.counter_runs += 1
        self.add_point(s,t,u)
        
        new_dict_file = [{'run%d' % self.counter_runs: {'parameters': {'sol_strength': s,'bsol_strength': t,'charge': u,'HCOR01': v,'VCOR01': w,'RF_amplitude': x, 'Image path': str(y)}}}]         # remember to save the path to the photo in your yaml file
        with open(path_yaml,'r') as yamlfile:
            cur_yaml = yaml.safe_load(yamlfile)
            cur_yaml.extend(new_dict_file)
        
        with open(path_yaml,'w') as yamlfile:
            yaml.safe_dump(cur_yaml, yamlfile)
        
        print 'Data saved'
        print '\n'

#        with open(path_csv, 'ab') as f:
#            thewriter = csv.writer(f)
#            thewriter.writerow([s, t, u, v, w, x])
   
    def update_text_fn(self, sol, bsol, rf):
        self.output.retranslateUi(sol, bsol, rf)
        
    def thread_complete(self):
        print("THREAD COMPLETE!")
        self.output.finished()
 
    def fn_worker(self, fn_loop, fn_sweep, sol_val, bsol_val, rf_val):
        # Pass the function to execute        
        worker = Worker(fn_loop, fn_sweep, sol_val, bsol_val, rf_val) # Any other args, kwargs are passed to the run function

        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)
        worker.signals.current_val.connect(self.update_text_fn)
        
        # Execute
        self.threadpool.start(worker) 
    
    def add_point(self, sol, bsol, charge):
        
        # range of charge that you want to resolve
        min_charge = 0
        max_charge = 500
        
        if charge <= min_charge:
            self.myspot.append({'pos': (sol, bsol), 'size': 0.5, 'pen': {'color': 'w', 'width': 2}, 'brush': 'b'})
        elif charge >= max_charge:
            self.myspot.append({'pos': (sol, bsol), 'size': 0.5, 'pen': {'color': 'w', 'width': 2}, 'brush': 'r'})
        else:
            charge_norm = (charge-min_charge)*10/(max_charge-min_charge)
            self.myspot.append({'pos': (sol, bsol), 'size': 0.5, 'pen': {'color': 'w', 'width': 2}, 'brush':pg.intColor(charge_norm, hues=11, values=1, maxValue=255, minValue=150, maxHue=320, minHue=600, sat=255, alpha=255)}) 
        self.graph.s3.addPoints(self.myspot)

# dd/mm/YY
today = date.today()
current_date = int(today.strftime("%d%m%Y"))

# choosing where to save the YAML file 
path_yaml = (r'C:\Users\qqi63789\OneDrive - Science and Technology Facilities Council\VirtualAccelerator\app6\yaml_%d.yaml' % current_date)      
c = controller(view, model)