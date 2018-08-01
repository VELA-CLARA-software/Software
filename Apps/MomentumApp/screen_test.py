import os, sys
import time

sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release')
os.environ["PATH"] = os.environ["PATH"]+";\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release\\root_v5.34.34\\bin\\"

import VELA_CLARA_Screen_Control as scrn

Init = scrn.init()
#camInit = camIA.init()
#
# Cmagnets = magInit.physical_CB1_Magnet_Controller()
# laser = pilInit.physical_PILaser_Controller()
# Cbpms = bpmInit.physical_CLARA_PH1_BPM_Controller()
# gun = llrfInit.physical_CLARA_LRRG_LLRF_Controller()
# LINAC01 = llrfInit.physical_L01_LLRF_Controller()

print 'here'
screens = Init.physical_CLARA_PH1_Screen_Controller()


time.sleep(2)
print 'Is YAG in?'
a = screens.isYAGIn('S02-SCR-01')
print a

# Insert YAG
screens.insertYAG('S02-SCR-01')
if screens.isYAGIn('S02-SCR-01') is False:
    while True:
        isscreenmoving1 = screens.isScreenMoving('S02-SCR-01')
        print 'Is screen moving?', isscreenmoving1
        time.sleep(1)
        isscreenmoving2 = screens.isScreenMoving('S02-SCR-01')
        if isscreenmoving2 is False and isscreenmoving1 is True:
            print 'Finished Moving!'
            break
else:
    pass

print 'Is YAG in now?'
b = screens.isYAGIn('S02-SCR-01')
print b

print 'Move it back out'
screens.moveScreenOut('S02-SCR-01')
