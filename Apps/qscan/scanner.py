from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtCore import pyqtSlot
import sys,os
import view
import numpy as np

sys.path.append("\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\stage\\")
#
#for item in sys.path:
#	print item

import VELA_CLARA_PILaser_Control as pil
import time

pil_init = pil.init()
#pil_init.setVerbose()
pil_control = pil_init.physical_PILaser_Controller()

import lasmover as lm
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

#exit()

class chargescanner(QtCore.QObject):

    changedval = pyqtSignal(float, float, float, float)

    # lo, hi and the min and max values of the area on the VC to scan
    # values are mm from bottom left of the VC imagecollector
    # nx,y is number of points to stop and measure charge at in x,y
    xlo = 3
    xhi = 7
    ylo = 3
    yhi = 7
    nx = 12
    ny = 12
    xrange = np.linspace(xlo,xhi,nx)
    yrange = np.linspace(ylo,yhi,ny)

    
    def doscan(self): 
        print self.xrange
        print self.yrange
        print therf.getPhiDEG()

        print '***********************************************************'
        print '!!!!!!!!!!!!!!!!!!!!!PLEASE READ!!!!!!!!!!!!!!!!!!!!!!!!!!!'
        print '***********************************************************\n'
        print 'This is a script to scan the laser over the cathode (via VC)'
        print 'and measure the charge on the WCM \n'
        print 'Please have imagecollector open on the VC and check that the'
        print 'mask feedback is switched on, and that the mask follows the VC laser spot'
        print 'throughout the scan.\n'

        print 'the x locations where charge will be measured are', self.xrange, ' mm'
        print 'the y locations where charge will be measured are', self.yrange, ' mm'
        print 'the total number of scan points is', self.nx*self.ny

        print 'the wcm reading at each point will be recorded in the file qscan.txt'
        print 'which is created whereever you run this script from'

        f = open('qscan'+str(timestr)+'.txt','a')

#exit()
        pil_control.setMaskFeedBackOn_VC()

        #xrange = [5.5]
        #yrange = [4.5]

        ix = 0
        for x in self.xrange:
            if ix % 2 == 0:
                dumyrange = self.yrange
                print 'going up', dumyrange 
            else:
                dumyrange = self.yrange[::-1] 
                print 'going up', dumyrange 
            ix = ix + 1            
            for y in dumyrange:
                print x, y, '\n'
               
                a = pil_control.setVCPos(x,y)
                # monitor  this paramter to know when ity has finished 
                set_pos_succes = False
#        exit()
		
                while 1:
                    set_pos_state = pil_control.getSetVCPosState()
                    print 'success status', set_pos_state
                    if set_pos_state == pil.VC_SET_POS_STATE.SUCCESS:
                        set_pos_succes = True
                        break
                    else:
                        print set_pos_state
                    time.sleep(1)
                print("Set Position Finished",pil_control.getSetVCPosState())
#        exit()
#        mylasmove.setposition(x,y,5,0.1)
#                raw_input("Press Enter to continue...")
                chargenow = monini.getValue(charge)
                lasEnow = monini.getValue(lasE)
                vcsumpnow = monini.getValue(vcsump)
                f.write('RF phase '+str(therf.getPhiDEG())+' vcx '+str(x)+' vcy '+str(y)+' charge '+str(chargenow)+' laserE '+str(lasEnow)+' VCintens '+str(vcsumpnow)+'\n')
                f.flush()
                self.changedval.emit(x,y,chargenow,lasEnow)
		
        f.close()