############################################################
# Template for cathode charge map. 
# Basically, raster scans laser over the cathode and gets the WCM change, the VC image
#
# -The raster scan/iterator code, will be heavily dependent on implementation of how mirror movement works in CATAP. 
# use mirror move fns, or or if there be a CATAP.PILaserSystem::SetVCps(x,y) function, the iterator could be quite different. 
# -this iterator/loop will take the laser beam in a raster scan all over a (?user defined?) area of 'mirror position phase space'.
# -at each point in the scan the following code gathers the required info.  

import sys
import time
import numpy as np
sys.path.append(r'\\claraserv3.dl.ac.uk\claranet\packages\CATAP\bin\python38')
from CATAP.PILaserSystem import *

PIL = PILaserSystem(STATE.VIRTUAL)
PIL.setup()
mirror = PIL.getMirror()
em = PIL.getEnergyMeter()
# if you camonitor VM-CLA-LAS-OPT-PICO-4C-PM-4:H:MREL while doing this you should see updates
# current mirror functions
# 'getVerticalPosition',  'getHorizontalPosition', 'moveDown', 'moveLeft', 'moveRight', 'moveUp', 'setHStep', 'setVStep'

from CATAP.Camera import *
cameraF = CameraFactory(STATE.VIRTUAL)
cameraF.setup("nominal", ["VIRTUAL_CATHODE"])
cameraF.startAcquiring('VIRTUAL_CATHODE')

from CATAP.EPICSTools import *
ET = EPICSTools(STATE.VIRTUAL)
# EPICS PV for bunch charge
ET.monitor("PV FOR WCM BUNCH CHARGE") # Could the PV be something like CLA-C09-IOC-CS-04:FMC_1_ADC_0_READ
mon = ET.getMonitor("PV FOR WCM BUNCH CHARGE")
mon.setBufferSize(20)
mon.setArrayBufferSize(20)


#user defined inputs 
#these are all in 'encoded mirror units' which can be found empirically
xstart = 68686
ystart = 33387
xsteps = 10
ysteps = 10
xstepsize = 555
ystepsize = 555
ix = 0 

########################################################################
# put the laser in the right place to start the scan
# which is bottom left
# currently can't see a mirror fn to SET laser position, only to GET it. 
########################################################################

#mirror.SetHStep(xstepsize)
#mirror.SetVStep(ystepsize)
for x in range(1,xsteps+1):
    if x % 2 == 0: # if x is even, 2,4,6 ... move mirror down
        for y in range(1,ysteps):
            mirror.moveDown()
            time.sleep(5)
            print("AT POSITION",x," ",y)
            mirror.moveDown()  
            ########################################################
            # Some code to check if mirror is where you think it is
            ########################################################
            #
            ########################################################
            # Some code to get the needed data at a scan point HERE
            ########################################################  
            cameraF.collectAndSave('VIRTUAL_CATHODE')
            q = mon.getValue() # should probab get a buffer of values and take mean stdev.
    else: # if x is odd, 1,3,5 ... move mirror up
        for y in range(1,ysteps+1):
            mirror.moveUp()        
            time.sleep(5)
            print("AT POSITION",x," ",y)
            mirror.moveDown()  
            ########################################################
            # Some code to check if mirror is where you think it is
            ########################################################
            #
            ########################################################
            # Some code to get the needed data at a scan point HERE
            ########################################################  
            cameraF.collectAndSave('VIRTUAL_CATHODE')
            q = mon.getValue() # should probab get a buffer of values and take mean stdev.
            elas = em.getEnergy()
    mirror.moveRight()

