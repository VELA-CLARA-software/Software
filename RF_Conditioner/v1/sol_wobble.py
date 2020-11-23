import os, time
import sys
sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\release')

import numpy as np
import VELA_CLARA_Magnet_Control as mag
from VELA_CLARA_Magnet_Control import MACHINE_MODE
from VELA_CLARA_Magnet_Control import MACHINE_AREA


#initiliase the magnet control
init=mag.init()
init.setQuiet()
# get a physical CLARA PH1 magnet controller
mag_control = init.getMagnetController( MACHINE_MODE.PHYSICAL,MACHINE_AREA.CLARA_PH1)

# sine wave paramters
mean_current = 150 # the nominal setting of the solenoid Max 250, (or maybe 300) 
Amplitude  = 50 # +- Amps from nominal_current (peak of sin wave)
numPoints = 100 # number of points per period 
wait_time = 2 # time in seconds between set points
# magnet to wobble, name as defined in mag_control 
solenoid = 'LRG-SOL'


current_changes = []
for point in range(0, numPoints):
	current_changes.append( mean_current +  Amplitude * np.sin( ( 2*np.pi / numPoints) * point ) )
	#print current_changes[point]
mag_control.setRITolerance(solenoid,5.0)

# get a reference to the solenoid object, from this we can access all solenoid data 
sol_obj = [ mag_control.getMagObjConstRef(solenoid)]

# print something to the screen
os.system('cls' if os.name == 'nt' else 'clear')
print('')
print('')
print('')
print('**********************************************')
print('**********************************************')
print('')
print('This is an automatic Solenoid Wobbling Script')
print('')
print('**********************************************')
print('**********************************************')
print('')
print('Solenoid Wobbler Active:') 
print('Amplitude range +-' + str(Amplitude) + ', time period = ' + str(numPoints*wait_time) + ' seconds')
print(solenoid + ' read I Tolerance = ' + str(mag_control.getRITolerance(solenoid) ) )
print('')

# main loop
i = 0
while 1: 
    # start timer
    time_0 = time.time();
    # set currnet in solenoid
    mag_control.setSI(solenoid,current_changes[i])
    # while set value is not equal (to within RItolerance) wait
    while not mag_control.isRIequalSI(solenoid):
        pass
    # while the time elapsed is not 
    while time.time() - time_0 < wait_time:
        time.sleep(0.1)
    i += 1
    if i == len(current_changes):
        i = 0
    a = "\rCurrent Solenoid Current = %d" % + mag_control.getSI(solenoid)
    sys.stdout.write(a)
    sys.stdout.flush()
    
    
print "you shouldn't really see this"
raw_input()