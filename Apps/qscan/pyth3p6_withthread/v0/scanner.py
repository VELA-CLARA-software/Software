from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSignal
#from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import *
import sys,os,time
import numpy as np


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
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


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
        self.kwargs['progress_callback'] = self.signals.progress        

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        
        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done
        





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
        self.kwargs['progress_callback'] = self.signals.progress        

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        
        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done



'''
class ScanWorker(QRunnable):

    
    #Worker thread
    
    changedval = pyqtSignal(float, float, float, float)
    changedlogtxt = pyqtSignal(str)


    @pyqtSlot()
    def run(self):
        
        #Your code goes in this function
        
        print("Thread start") 
        col = 0    
        for i in range(2):
            for j in range(2):
                col = col + 1
                xval = i
                yval = j
                charge = col*10   
                lasE = col*20 
                self.changedval.emit(xval,yval,charge,lasE)
                iterstring = "moving laser beam to "+str(xval)+" "+str(yval)
                print(iterstring)
                #self.changedlogtxt.emit(iterstring) 
                time.sleep(2)
        print("ScanWorker:run() Hello! I've generated some data")    
        print("Thread complete")


'''

#from PyQt5 import QtGui, QtCore
#from PyQt5.QtCore import pyqtSignal
#from PyQt5.QtCore import pyqtSlot
#from PyQt5.QtCore import *
#import sys,os
#import view
import numpy as np

#sys.path.append("\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\stage\\")
#sys.path.append("\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\stage\\Python3_x64\\")
sys.path.append("\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\stage\\Python3_x64\\")


#
#for item in sys.path:
#   print item

#0# import VELA_CLARA_PILaser_Control as pil
import time

#0# pil_init = pil.init()
#pil_init.setVerbose()
#0# pil_control = pil_init.physical_PILaser_Controller()

#import lasmover as lm
import math as ma
import numpy as np
import time
timestr = time.strftime("%Y%m%d-%H%M%S")

import VELA_CLARA_LLRF_Control as rf
rfinit = rf.init()
therf = rfinit.physical_CLARA_LRRG_LLRF_Controller()

import VELA_CLARA_BPM_Control as bpm 
bpminit = bpm.init()
bpminit.setVerbose()
bpms = bpminit.physical_CLARA_PH1_BPM_Controller()

import VELA_CLARA_General_Monitor as mon
monini = mon.init()

charge = monini.connectPV('CLA-S01-DIA-WCM-01:Q')
lasE = monini.connectPV('CLA-LAS-DIA-EM-01:E')
vcsump = monini.connectPV('CLA-VCA-DIA-CAM-01:ANA:Intensity_RBV')

# NEW section to get llrf stuff. Tried copying from Duncan charge app. 
therf2 = rfinit.getLLRFController(rf.MACHINE_MODE.PHYSICAL,rf.LLRF_TYPE.CLARA_LRRG)
##therf2.getCavFwdPwr()
##therf2.getCavRevPwr()
##print("hello!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",therf2.getCavFwdPwr())


#exit()

class ScanWorker(QRunnable):


    @pyqtSlot()
    def run(self):
        print("Thread start") 
        col = 0    
        for i in range(2):
            for j in range(2):
                col = col + 1
                xval = i
                yval = j
                charge = col*10   
                lasE = col*20 
                self.changedval.emit(xval,yval,charge,lasE)
                iterstring = "moving laser beam to "+str(xval)+" "+str(yval)
                print(iterstring)
                self.changedlogtxt.emit(iterstring) 
                time.sleep(2)
        print("mainapptest:generate() Hello! I've generated some data")    
        print("Thread complete")


class chargescanner(QtCore.QObject):

    changedval = pyqtSignal(float, float, float, float)
    changedlogtxt = pyqtSignal(str)
    
    # lo, hi and the min and max values of the area on the VC to scan
    # values are mm from bottom left of the VC imagecollector
    # nx,y is number of points to stop and measure charge at in x,y
    xlo = 3
    xhi = 7
    ylo = 3
    yhi = 7
    nx = 3
    ny = 3
    xrange = np.linspace(xlo,xhi,nx)
    yrange = np.linspace(ylo,yhi,ny)

    def domyscan(self, progress_callback):
        col = 0
        for i in range(2):
            for j in range(2):
                col = col + 1
                xval = i
                yval = j
                charge = col*10   
                lasE = col*20 
                self.changedval.emit(xval,yval,charge,lasE)
                iterstring = "moving laser beam to "+str(xval)+" "+str(yval)
                print(iterstring)
                self.changedlogtxt.emit(iterstring) 
                time.sleep(2)
                

    def generatedummydata(self):
        print("mainapptest:generate()  Hello!!! You've pushed the button")  
        col = 0    
        for i in range(2):
            for j in range(2):
                col = col + 1
                xval = i
                yval = j
                charge = col*10   
                lasE = col*20 
                self.changedval.emit(xval,yval,charge,lasE)
                iterstring = "moving laser beam to "+str(xval)+" "+str(yval)
                print(iterstring)
                self.changedlogtxt.emit(iterstring) 
                time.sleep(2)
        print("mainapptest:generate() Hello! I've generated some data")         
        