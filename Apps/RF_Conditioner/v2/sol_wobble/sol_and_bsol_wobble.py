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
mean_current_sol = 105 # the nominal setting of the solenoid Max 250, (or maybe 300)
Amplitude_sol  = 105# +- Amps from nominal_current (peak of sin wave)
mean_current_bsol = -1.0*0.9*mean_current_sol # the nominal setting of the solenoid Max 250, (or maybe 300) 
#mean_current_bsol = -100 # the nominal setting of the solenoid Max 250, (or maybe 300) 
Amplitude_bsol  = 0.9*Amplitude_sol # +- Amps from nominal_current (peak of sin wave)
#Amplitude_bsol  = 75# +- Amps from nominal_current (peak of sin wave)
numPoints_sol = 133 # number of points per period
numPoints_Bsol = 131 # number of points per period
wait_time = 1 # time in seconds between set points
# magnet to wobble, name as defined in mag_control 
solenoid = 'LRG-SOL'
bsolenoid = 'LRG-BSOL'


current_changes_sol = []
current_changes_bsol = []
for point in range(0, numPoints_sol):
	current_changes_sol.append ( mean_current_sol +  Amplitude_sol * np.sin( ( 2*np.pi / numPoints_sol) * point ) )
for point in range(0, numPoints_Bsol):
	current_changes_bsol.append( mean_current_bsol -  Amplitude_bsol * np.sin( ( 2*np.pi / numPoints_Bsol) * point ) )
	#print current_changes[point]
# set the tolerance for the magnet  curparent readi = seti
mag_control.setRITolerance(solenoid,5.0)
mag_control.setRITolerance(bsolenoid,5.0)

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
print('Main-Solenoid Amplitude range +-' + str(Amplitude_sol)  + ', time period = ' + str(numPoints_sol*wait_time) + ' seconds')
print('Buck-Solenoid Amplitude range +-' + str(Amplitude_bsol) + ', time period = ' + str(numPoints_Bsol*wait_time) + ' seconds')
print(solenoid + '  read I Tolerance = ' + str(mag_control.getRITolerance(solenoid) ) )
print(bsolenoid + ' read I Tolerance = ' + str(mag_control.getRITolerance(bsolenoid) ) )
print('')

# main loop
i = j =0
while 1: 
    # start timer
    time_0 = time.time();
    # set currnet in solenoid
    
    #raw_input()
    
    mag_control.setSI(solenoid,current_changes_sol[i])
    mag_control.setSI(bsolenoid,current_changes_bsol[j])
    # while set value is not equal (to within RItolerance) wait
    while not mag_control.isRIequalSI(solenoid):
        pass
    while not mag_control.isRIequalSI(bsolenoid):
        pass
    # while the time elapsed is not 
    while time.time() - time_0 < wait_time:
        time.sleep(0.1)
    
    # reset counters if we have done a full wobble
    i += 1
    if i == len(current_changes_sol):
        i = 0
    j += 1
    if j == len(current_changes_bsol):
        j = 0
    
    # update display
    a = "\rMain-Solenoid I = %d" % + mag_control.getSI(solenoid) + ", Buck-Solenoid I = %d    " % + mag_control.getSI(bsolenoid)
    sys.stdout.write(a)
    sys.stdout.flush()
    
    
print "you shouldn't really see this"
raw_input()