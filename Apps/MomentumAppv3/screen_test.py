import sys
sys.path.append('//apclara1/ControlRoomApps/Controllers/bin/stage')
#sys.path.append('//apclara1/ControlRoomApps/Controllers/bin/release')

import time
import VELA_CLARA_Screen_Control as scrn
scrnInit = scrn.init()
screens = scrnInit.physical_C2B_Screen_Controller()

time.sleep(1)
#screen='S02-SCR-01'
screen='S02-SCR-02'
#screen='C2V-SCR-01'

print '\n',screen
#print 'Screen set state is: ', screens.getScreenSetState(screen)
print 'Screen state is: ', screens.getScreenState(screen)
print 'Is YAG in? ', screens.isYAGIn(screen)
print 'ACTPOS = ', screens.getACTPOS(screen)
print 'YAG pos = ', screens.getDevicePosition(screen, scrn.SCREEN_STATE.V_YAG)
print 'RF cage pos = ', screens.getDevicePosition(screen, scrn.SCREEN_STATE.V_RF)
#print getScreenSetState
