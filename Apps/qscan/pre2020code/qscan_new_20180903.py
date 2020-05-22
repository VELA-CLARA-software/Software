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

for item in sys.path:
	print item

import VELA_CLARA_PILaser_Control as pil
import time

pil_init = pil.init()
pil_init.setVerbose()

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
lasE = monini.connectPV('CLA-LAS-EM-ENERGY')

#mylasmove = lm.lasmover()
#mylasmove.getposition()


#pil_control.setMaskFeedBackOn_VC()
#	
#a = pil_control.setVCPos(7,4)
#
## monitor  this paramter to know when ity has finished 
#
#set_pos_succes = False
#
#while 1:
#	set_pos_state = pil_control.getSetVCPosState()
#	if set_pos_state == pil.VC_SET_POS_STATE.SUCCESS:
#		set_pos_succes = True
#		break
#	else:
#		print set_pos_state
#	time.sleep(1)
#
#print("Set Position Finished",pil_control.getSetVCPosState())

#exit()

# lo, hi and the min and max values of the area on the VC to scan
# values are mm from bottom left of the VC imagecollector
# nx,y is number of points to stop and measure charge at in x,y
xlo = 4
xhi = 4
ylo = 7
yhi = 7
nx = 10
ny = 10

#xlo = 5.25
#xhi = 5.25
#ylo = 3.7
#yhi = 3.7
#nx = 1
#ny = 1
xrange = np.linspace(xlo,xhi,nx)
yrange = np.linspace(ylo,yhi,ny)



print xrange
print yrange

#exit()

print therf.getPhiDEG()

print '***********************************************************'
print '!!!!!!!!!!!!!!!!!!!!!PLEASE READ!!!!!!!!!!!!!!!!!!!!!!!!!!!'
print '***********************************************************\n'
print 'This is a script to scan the laser over the cathode (via VC)'
print 'and measure the charge on the WCM \n'
print 'Please have imagecollector open on the VC and check that the'
print 'mask feedback is switched on, and that the mask follows the VC laser spot'
print 'throughout the scan.\n'

raw_input("Press Enter to continue...")

print 'the x locations where charge will be measured are', xrange, ' mm'
print 'the y locations where charge will be measured are', yrange, ' mm'
print 'the total number of scan points is', nx*ny

raw_input("Press Enter to continue...")

print 'the wcm reading at each point will be recorded in the file qscan.txt'
print 'which is created whereever you run this script from'

f = open('qscan'+str(timestr)+'.txt','a')

#exit()

pil_control.setMaskFeedBackOn_VC()

xrange = [5.5, 5.6]
yrange = [4.5, 4.6]

for x in xrange:
    for y in yrange:
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
        raw_input("Press Enter to continue...")
        chargenow = monini.getValue(charge)
        lasEnow = monini.getValue(lasE)
        f.write('RF phase '+str(therf.getPhiDEG())+' vcx '+str(x)+' vcy '+str(y)+' charge '+str(chargenow)+' laserE '+str(lasEnow)+'\n')
        f.flush()

		
		
f.close()
