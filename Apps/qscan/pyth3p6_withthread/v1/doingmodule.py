from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSignal
#from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import *
import sys,os,time
import numpy as np

#sys.path.append("\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\stage\\")
#sys.path.append("\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\stage\\Python3_x64\\")
sys.path.append("\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\stage\\Python3_x64\\")

# threading mechanics copied exactly from 
# https://www.learnpyqt.com/courses/concurrent-execution/multithreading-pyqt-applications-qthreadpool/
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

# threading mechanics copied exactly from 
# https://www.learnpyqt.com/courses/concurrent-execution/multithreading-pyqt-applications-qthreadpool/
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
        


# keep this stuff as template code for interacting with clara machine. 
'''
#0# pil_init = pil.init()
#pil_init.setVerbose()
#0# pil_control = pil_init.physical_PILaser_Controller()

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
'''


class doingclass(QtCore.QObject):

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
    xlow = 999

    def setparams(self, dumxl, dumxh, nx, dumyl, dumyh, ny):
    # set the scan parameters 
        self.xlow = dumxl
        self.xhi = dumxh
        self.nx = nx
        self.ylow = dumyl
        self.yhi = dumyh
        self.ny = ny
        self.xrange = np.linspace(self.xlow,self.xhi,self.nx)
        self.yrange = np.linspace(self.ylow,self.yhi,self.ny)
        
    def domystuff(self, progress_callback):
    ##########################################################################
    # THE CONCRETE PLACE WHERE YOU FINALLY PUT CODE 'DO STUFF' !!!!!!
    ##########################################################################
        col = 0
        #gg = targ1
        print(self.xrange)
        #input() 
        for i in self.xrange:
            for j in self.yrange:
                col = col + 1
                xval = i
                yval = j
                charge = col*10   
                lasE = col*20 
                self.changedval.emit(xval,yval,charge,lasE)
                iterstring = "moving laser beam to "+str(xval)+" "+str(yval)
                print(iterstring)
                self.changedlogtxt.emit(iterstring) 
                time.sleep(2) # this could represent the time spent moving a laser beam, ramping a magnet, RF etc.      

