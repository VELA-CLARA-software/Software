import os, time
import sys
sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\release')


import numpy as np
import VELA_CLARA_Magnet_Control as mag
from VELA_CLARA_Magnet_Control import MACHINE_MODE
from VELA_CLARA_Magnet_Control import MACHINE_AREA


#initiliase the magnet control
init=mag.init()
init.setQuiet()
# get a physical CLARA PH1 magnet controller
mag_control = init.getMagnetController(MACHINE_MODE.PHYSICAL,MACHINE_AREA.CLARA_PH1)


# sine wave paramters
mean_current_sol_1 = 0 # the nominal setting of the solenoid Max 250, (or maybe 300) 
mean_current_sol_2 = 0 # the nominal setting of the solenoid Max 250, (or maybe 300) 
Amplitude_sol_1  = 150 # +- Amps from nominal_current (peak of sin wave)
Amplitude_sol_2  = 150 # +- Amps from nominal_current (peak of sin wave)
#Amplitude_bsol  = 75# +- Amps from nominal_current (peak of sin wave)
numPoints_sol_1 = 200 # number of points per period 
numPoints_sol_2 = 200 # number of points per period 
wait_time = 1 # time in seconds between set points
# magnet to wobble, name as defined in mag_control 
solenoid_1 = 'L01-SOL1'
solenoid_2 = 'L01-SOL2'


current_changes_sol_1 = []
current_changes_sol_2 = []
for point in range(0, numPoints_sol_1):
	current_changes_sol_1.append ( mean_current_sol_1 +  Amplitude_sol_1 * np.sin( ( 2*np.pi / numPoints_sol_1) * point ) )
for point in range(0, numPoints_sol_2):
	current_changes_sol_2.append( mean_current_sol_2 +  Amplitude_sol_2 * np.sin( ( 2*np.pi / numPoints_sol_2) * point ) )
	#print current_changes[point]
# set the tolerance for the magnet  current readi = seti
mag_control.setRITolerance(solenoid_1,5.0)
mag_control.setRITolerance(solenoid_2,5.0)

# get a reference to the solenoid object, from this we can access all solenoid data (not used atm)
#sol_obj = [ mag_control.getMagObjConstRef(solenoid)]
#bsol_obj = [ mag_control.getMagObjConstRef(bsolenoid)]

# print something helpful to the screen
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
print('Linac-Solenoid-1 Amplitude range +-' + str(Amplitude_sol_1)  + ', time period = ' + str(numPoints_sol_1*wait_time) + ' seconds')
print('Linac-Solenoid-2 Amplitude range +-' + str(Amplitude_sol_2) + ', time period = ' + str(numPoints_sol_2*wait_time) + ' seconds')
print(solenoid_1 + ' read I Tolerance = ' + str(mag_control.getRITolerance(solenoid_1) ) )
print(solenoid_2 + ' read I Tolerance = ' + str(mag_control.getRITolerance(solenoid_2) ) )
print('')

# main loop
i = j =0
while 1: 
    # start timer
    time_0 = time.time();
    # set currnet in solenoid
    
    #raw_input()
    
    mag_control.setSI(solenoid_1,current_changes_sol_1[i])
    mag_control.setSI(solenoid_2,current_changes_sol_2[j])
    # while set value is not equal (to within RItolerance) wait
    while not mag_control.isRIequalSI(solenoid_1):
        pass
    while not mag_control.isRIequalSI(solenoid_2):
        pass
    # while the time elapsed is not 
    while time.time() - time_0 < wait_time:
        time.sleep(0.1)
    
    # reset counters if we have done a full wobble
    i += 1
    if i == len(current_changes_sol_1):
        i = 0
    j += 1
    if j == len(current_changes_sol_2):
        j = 0
    
    # update display
    a = "\rLinac-Solenoid-1 = %d" % + mag_control.getSI(solenoid_1) + ", Linac-Solenoid-2 I = %d    " % + mag_control.getSI(solenoid_2)
    sys.stdout.write(a)
    sys.stdout.flush()
    
    
print "you shouldn't really see this"
raw_input()