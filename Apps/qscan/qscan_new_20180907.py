#***********************************************************'
#!!!!!!!!!!!!!!!!!!!!!PLEASE READ!!!!!!!!!!!!!!!!!!!!!!!!!!!'
#***********************************************************\n'
# This is a script to scan the laser over the cathode (via VC)'
# and measure the charge on the WCM \n'
# Please have imagecollector open on the VC and check that the'
# mask feedback is switched on, and that the mask follows the VC laser spot'
# throughout the scan.\n'
# the x locations where charge will be measured are', xrange, ' mm'
# the y locations where charge will be measured are', yrange, ' mm'
# the total number of scan points is', nx*ny
# the wcm reading at each point will be recorded in the file qscan.txt'
# which is created whereever you run this script from'

import sys

sys.path.append("\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\stage\\")

import VELA_CLARA_PILaser_Control as pil
import time


pil_init = pil.init()
#pil_init.setVerbose()

pil_control = pil_init.physical_PILaser_Controller()



import math as ma
#import numpy as np
import time
timestr = time.strftime("%Y%m%d-%H%M%S")


#import VELA_CLARA_LLRF_Control as rf
#rfinit = rf.init()
#therf = rfinit.physical_CLARA_LRRG_LLRF_Controller()

#import VELA_CLARA_BPM_Control as bpm 
#bpminit = bpm.init()
#bpminit.setVerbose()
#bpms = bpminit.physical_CLARA_PH1_BPM_Controller()


import VELA_CLARA_General_Monitor as mon
monini = mon.init()

charge = monini.connectPV('CLA-S01-DIA-WCM-01:Q')
lasE = monini.connectPV('CLA-LAS-DIA-EM-01:E')
vcposx = monini.connectPV('CLA-VCA-DIA-CAM-01:ANA:X_RBV')
vcposy = monini.connectPV('CLA-VCA-DIA-CAM-01:ANA:Y_RBV')


#print therf.getPhiDEG()

print '***********************************************************'
print '!!!!!!!!!!!!!!!!!!!!!PLEASE READ!!!!!!!!!!!!!!!!!!!!!!!!!!!'
print '***********************************************************\n'


f = open('qscan'+str(timestr)+'.txt','a')

#exit()

pil_control.setMaskFeedBackOn_VC()


xsrange = range(10)
ysrange = range(10)

print xsrange
print ysrange

for xs in xsrange:
     pil_control.moveRight(100)
     if xs % 2 == 0:
        pil_control.moveDown(100)
        pil_control.moveDown(100)
        pil_control.moveDown(100)
        pil_control.moveDown(100)
        pil_control.moveDown(100)
        pil_control.moveDown(100)
     else:
        pil_control.moveUp(100)
        pil_control.moveUp(100)
        pil_control.moveUp(100)
        pil_control.moveUp(100)
        pil_control.moveUp(100)
        pil_control.moveUp(100)
     for ys in ysrange:
        if ys == 0:
           print "pause vertical movement"	
        elif xs % 2 == 0: 
           pil_control.moveUp(100)
           print "moving up"
        else:
           pil_control.moveDown(100)
           print "moving down"			
        chargenow = monini.getValue(charge)
        lasEnow = monini.getValue(lasE)
        vcposxnow = monini.getValue(vcposx)
        vcposynow = monini.getValue(vcposy)
#        hwpnow = monini.getValue(hwp)
        time.sleep(1)
        print " hello ", vcposxnow, vcposynow, chargenow
        f.write('x '+str(vcposxnow)+' y '+str(vcposynow)+' charge '+str(chargenow)+' laserE '+str(lasEnow)+'\n')
#        f.write('RF phase '+str(therf.getPhiDEG())+' vcx '+str(x)+' vcy '+str(y)+' charge '+str(chargenow)+' laserE '+str(lasEnow)+'\n')
        f.flush()		

f.close()