from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtCore import pyqtSlot
import sys,os
import numpy as np
import time


sys.path.append("\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\stage\\")

import VELA_CLARA_General_Monitor as mon
monini = mon.init()


#lasE = monini.connectPV('CLA-LAS-DIA-EM-01:E') # laser pulse E from diode next to ophir

lasE = monini.connectPV('EBT-B03-IOC-CS-04:FMC_2_CH_0_SUM_out') # sum of waveform of CLA-LAS-DIA-EM-01 

lasEnow = []

while True:

    if not lasE == 'FAILED':
        for l in range(100):
            lasEnow.append(monini.getValue(lasE))
            time.sleep(0.11)
    else:
        lasEnow.append(-999.0)
      
   

    lasenowmean = np.mean(lasEnow)
    lasenowsdev = np.std(lasEnow)        
    lasenowmax = np.max(lasEnow)
    lasenowmin = np.min(lasEnow)        



    print 'values ', lasEnow
    print ' '   
    print ' max ', lasenowmax, ' min ', lasenowmin
    print ' mean ',   lasenowmean, ' err ', lasenowsdev, ' err/mean ',  lasenowsdev/lasenowmean   
   
   
    del lasEnow[:]   
    
    raw_input()