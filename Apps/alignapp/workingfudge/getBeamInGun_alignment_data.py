import lasmover as lm

#exit()

import math as ma
import numpy as np
import os, sys
import time
import datetime
timestr = time.strftime("%Y%m%d-%H%M%S")
from epics import caput, caget

sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release')
os.environ["PATH"] = os.environ["PATH"]+";\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release\\root_v5.34.34\\bin\\"

import VELA_CLARA_LLRF_Control as rf
rfinit = rf.init()
therf = rfinit.physical_CLARA_LRRG_LLRF_Controller()

import VELA_CLARA_BPM_Control as bpm 
bpminit = bpm.init()
bpminit.setVerbose()
bpms = bpminit.physical_CLARA_PH1_BPM_Controller()

bpms.setBufferSize(30)

import VELA_CLARA_General_Monitor as mon
monini = mon.init()

#exit()

import VELA_CLARA_Camera_DAQ_Control as daq 
import VELA_CLARA_Camera_IA_Control as camIA
Init = daq.init()
Init.setVerbose()
#Init.setMessage()
#Init.setDebugMessage()
camInit = camIA.init()
#camInit.setVerbose()
camerasIA = camInit.physical_CLARA_Camera_IA_Controller()
cameras = Init.physical_CLARA_Camera_DAQ_Controller()

# new camera controller
#import VELA_CLARA_Camera_Control as cam
#cam_init = cam.init()
#cam_init.setVerbose()
#cam_control = cam_init.physical_Camera_Controller()



#exit()

import VELA_CLARA_Magnet_Control as mag

minit = mag.init()
magnets = minit.physical_CLARA_PH1_Magnet_Controller()

import VELA_CLARA_Shutter_Control as shutc
shutcini = shutc.init()
theshut = shutcini.physical_PIL_Shutter_Controller()

#exit()

charge = monini.connectPV('CLA-S01-DIA-WCM-01:Q')
hwp =  monini.connectPV('EBT-LAS-OPT-HWP-1:ROT:RPOSS')
lintens = monini.connectPV('CLA-VCA-DIA-CAM-01:ANA:Intensity_RBV')

#lintensnow = monini.getValue(lintens)
#print charge, hwp, lintens, lintensnow

#exit()

mylasmove = lm.lasmover()
mylasmove.getposition()

#exit()

#xlo = 5.75
#xhi = 6.75
#ylo = 4.20
#yhi = 5.20
#nx = 5
#ny = 5

xlo = 5.1
xhi = 7.1
ylo = 3.9
yhi = 5.9
nx = 5
ny = 5


#xlo =  5.25
#xhi = 5.25
#ylo = 3.70
#yhi = 3.70
#nx = 1
#ny = 1

xrange = np.linspace(xlo,xhi,nx)
yrange = np.linspace(ylo,yhi,ny)

print xrange
print yrange

print therf.getPhiDEG()



now = datetime.datetime.now()
nowiso = now.isoformat('-').replace(":", "-").split('.', 1)[0]
hwpnow = monini.getValue(hwp)
#lintensnow = monini.getValue(lintens)

#f = open('logfile.txt','a')

#exit()

print 'HELLO !!!!!!!!!!!'

f = open('alignscan'+str(timestr)+'.txt','a')

f.write('This log file created (start time) at '+str(nowiso)+ \
        ' the half phase plate was set to '+str(hwpnow)+ \
        '\n')

theshut.open("SHUT02")
		
for x in xrange:
    for y in yrange:
        print x, y, '\n'
#        caput('EBT-LAS-OPT-HWP-1:ROT:MABSS',135)
        caput('EBT-LAS-OPT-HWP-2:ROT:MABS',120)
        time.sleep(3)
        mylasmove.setposition(x,y,5,0.05)
        caput('EBT-LAS-OPT-HWP-2:ROT:MABS',80)	
        time.sleep(3)
		
        raw_input("Press Enter to continue...")
        # get the VC image
        cameras.setCamera('VC')
        time.sleep(1)
        cameras.startAcquiring()
        time.sleep(1)
        cameras.collectAndSave(1)
        time.sleep(1)
        cameras.stopAcquiring()
        time.sleep(1)        
        chargenow = monini.getValue(charge)
        bpms.reCalAttenuation('S01-BPM01',chargenow)
#        raw_input(" VC Press Enter to continue...")
        phi1 = -160 
        phi2 = -165

        #############################
        # Set RF phase to FIRST VALUE
        #############################
#        therf.setPhiDEG(phi1)
        magnets.setSI('LRG-SOL',110)
#       vsol = magnets.getRI('LRG-SOL')
#       vbsol = magnets.getRI('LRG-BSOL')
        time.sleep(10)
        xbuff =  bpms.getBPMXPVBuffer('S01-BPM01')
        ybuff =  bpms.getBPMYPVBuffer('S01-BPM01')
        #print ' xbuff ', xbuff, ' y buff ', ybuff 
        #raw_input("Press Enter to continue...")
        sx1 = np.std(xbuff)
        mx1 = np.mean(xbuff)
        sy1 = np.std(ybuff)
        my1 = np.mean(ybuff)
        # take screen data 
        cameras.setCamera('S01-CAM-01')
        time.sleep(1)
        cameras.startAcquiring()
        time.sleep(1)
        cameras.collectAndSave(1)
        time.sleep(1)
        cameras.stopAcquiring()
        time.sleep(1)
        camerasIA.setCamera('S01-CAM-01')
        selectedCameraIA = camerasIA.getSelectedIARef()
        camx1 = selectedCameraIA.IA.x
        camy1 = selectedCameraIA.IA.y
        print ' camx1 ', camx1
#        theshut.close("SHUT02")
#        time.sleep(1)
#        cameras.startAcquiring()
#        time.sleep(1)
#        cameras.collectAndSave(1)
#        time.sleep(1)
#        cameras.stopAcquiring()
#        time.sleep(1)		
#		#raw_input("Press Enter to continue...")
#        theshut.open("SHUT02")


        ##############################
        # Set RF phase to SECOND VALUE
        ##############################
#        therf.setPhiDEG(phi2)
        magnets.setSI('LRG-SOL',-110)
        time.sleep(10)       
        vsol = magnets.getRI('LRG-SOL')
        vbsol = magnets.getRI('LRG-BSOL')
        xbuff =  bpms.getBPMXPVBuffer('S01-BPM01')
        ybuff =  bpms.getBPMYPVBuffer('S01-BPM01')
#        print ' xbuff2 ', xbuff, ' y buff2 ', ybuff 
#       raw_input("Press Enter to continue...")
        sx2 = np.std(xbuff)
        mx2 = np.mean(xbuff)
        sy2 = np.std(ybuff)
        my2 = np.mean(ybuff)
        cameras.setCamera('S01-CAM-01')
        time.sleep(1)
        cameras.startAcquiring()
        time.sleep(1)
        cameras.collectAndSave(1)
        time.sleep(1)
        cameras.stopAcquiring()
        time.sleep(1)
        selectedCameraIA = camerasIA.getSelectedIARef()
        camx2 = selectedCameraIA.IA.x
        camy2 = selectedCameraIA.IA.y
        print ' camx2 ', camx2
        theshut.close("SHUT02")
        time.sleep(1)
        cameras.startAcquiring()
        time.sleep(1)
        cameras.collectAndSave(1)
        time.sleep(1)
        cameras.stopAcquiring()
        time.sleep(1)
        #raw_input("Press Enter to continue...")
        theshut.open("SHUT02")

        # process the net BPM movement 
        delx = mx2-mx1
        dely = my2-my1
        delr = ma.sqrt(delx**2 + dely**2)

        # process the net camera movement
        delcamx = camx2-camx1
        delcamy = camy2-camy1
        delcamr = ma.sqrt(delcamx**2 + delcamy**2)


        # write all the data to a file 
        f.write('RF phase '+str(therf.getPhiDEG())+' vcx '+str(x)+' vcy '+str(y)+ \
                ' charge '+str(chargenow)+ \
                ' x1  '+str(mx1)+' sx1 '+str(sx1)+' x2 '+str(mx2)+' sx2 '+str(sx2)+ \
                ' y1  '+str(my1)+' sy1 '+str(sy1)+' y2 '+str(my2)+' sy2 '+str(sy2)+ \
                ' delx '+str(delx)+' dely '+str(dely)+' delr '+str(delr)+ \
                ' camx1  '+str(camx1)+' camx2 '+str(camx2)+ \
                ' camy1  '+str(camy1)+' camx2 '+str(camy2)+ \
                ' delcamx '+str(delcamx)+' delcamy '+str(delcamy)+ \
                ' delcamr '+str(delcamr)+ \
                ' bsol '+str(vbsol)+' sol '+str(vsol)+ \
                '\n')
        f.flush()
    

##for x in xrange:
##    for y in yrange:
##        print x, y, '\n'
###        set posiiotn(x,y,5,0.05)
### vary RF phase or solenoid strength
##        for var in [5, 15]:
##          therf.setPhiDEG(var)
### Get BPM readings and stddev
#xbuff =  bpms.getBPMXPVBuffer('S01-BPM01')
#ybuff =  bpms.getBPMYPVBuffer('S01-BPM01')
#sx = np.std(xbuff)
#mx = np.mean(xbuff)
#sy = np.std(ybuff)
#my = np.mean(ybuff)
### Get Screen images and readings
### Get WCM reading
### Get RF phase
### print all the above into a log file. 
##f.write('hello')
#chargenow = monini.getValue(charge)
#f.write('RF phase '+str(therf.getPhiDEG())+' bpmx '+str(mx)+' +- '+str(sx)+' bpmy '+str(my)+' +- '+str(sy)+' charge '+str(chargenow)+'\n')
#f.flush()

cameras.startAcquiring()
