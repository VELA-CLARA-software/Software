import os, sys
import time

#sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release')
sys.path.append('C:\\Users\\djd63\\Desktop\\Release')
#os.environ["PATH"] = os.environ["PATH"]+";\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release\\root_v5.34.34\\bin\\"
for i in sys.path:
    print i
print 'here1'
import VELA_CLARA_Screen_Control as scrn
print 'here2'
import VELA_CLARA_Shutter_Control as shut
#exit()
#Init2 = shut.init()
Init = scrn.init()
#camInit = camIA.init()
#
# Cmagnets = magInit.physical_CB1_Magnet_Controller()
# laser = pilInit.physical_PILaser_Controller()
# Cbpms = bpmInit.physical_CLARA_PH1_BPM_Controller()
# gun = llrfInit.physical_CLARA_LRRG_LLRF_Controller()
# LINAC01 = llrfInit.physical_L01_LLRF_Controller()

print 'here'
screens = Init.physical_C2B_Screen_Controller()
#cont = init.physical_C2B_Screen_Controller()
#screens = Init.physical_CLARA_PH1_Screen_Controller()

time.sleep(2)
print 'Is YAG in?'
screen = 'C2V-SCR-01'
a = screens.isYAGIn(screen)
print a

# Insert YAG
screens.insertYAG(screen)
if screens.isYAGIn(screen) is False:
    while True:
        isscreenmoving1 = screens.isScreenMoving(screen)
        print 'Is screen moving?', isscreenmoving1
        time.sleep(1)
        isscreenmoving2 = screens.isScreenMoving(screen)
        if isscreenmoving2 is False and isscreenmoving1 is True:
            print 'Finished Moving!'
            break
else:
    pass


print 'Is YAG in now?'
b = screens.isYAGIn(screen)
print b
time.sleep(3)
print 'try enable'
#?????? don't think this is right:
scrn.setEn(screen,scrn.DRIVER_DIRECTION.VERTICAL)

print 'Move it back out'
#this gives an error:
screens.moveScreenOut(screen)