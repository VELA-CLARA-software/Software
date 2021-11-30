import numpy as np
import csv
from datetime import datetime
import os, sys, time
import matplotlib.pyplot as plt
#import pandas as pd

print 'press enter to continue'
#raw_input()

del os.environ["EPICS_CA_AUTO_ADDR_LIST"]
#del os.environ["EPICS_CA_SERVER_PORT"]
os.environ["EPICS_CA_ADDR_LIST"] = "192.168.83.255"
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release')

today = datetime.now()
year = today.strftime("%Y")
month = today.strftime("%m")
day = today.strftime("%d")
dirName= 'Measurements/'+year+'/'+month+'/'+day

'''
import VELA_CLARA_General_Monitor as monx
general_monitor = monx.init()

general_monitor.setVerbose()      
#PVs needed
rf = general_monitor.connectPV('CLA-GUN-LRF-CTRL-01:ad1:ch1:Power:Wnd:Avg')
rfff = general_monitor.connectPV('CLA-GUN-LRF-CTRL-01:ARCH:FF_AMP')
sol = general_monitor.connectPV('CLA-GUN-MAG-SOL-02:READI')
bsol = general_monitor.connectPV('CLA-LRG1-MAG-SOL-01:READI')
bcharge = general_monitor.connectPV('CLA-S01-DIA-WCM-01:Q')

charge_list=[]
rf_list = []
FF_list = []
sol_list = []
bsol_list = []

solv = 0

for x in range(5):
    time.sleep(1)
    rfv = general_monitor.getValue(rf)
    rfffv = general_monitor.getValue(rfff)
    solv = general_monitor.getValue(sol)
    bsolv = general_monitor.getValue(bsol)
    bchargev = general_monitor.getValue(bcharge)

    charge_list.append(bchargev)
    rf_list.append(rfv)
    FF_list.append(rfffv)
    sol_list.append(solv)
    bsol_list .append(bsolv)
    

mean_charge = np.mean(charge_list)
error_charge = np.std(charge_list)
        
mean_rf = np.mean(rf_list)
mean_FF = np.mean(FF_list)
mean_sol = np.mean(sol_list)
mean_bsol = np.mean(bsol_list)
 




import VELA_CLARA_LLRF_Control as llrf
import time
from datetime import datetime
init = llrf.init()
init.setVerbose()
# FOR THE GUN specify which line and cavity, SO:  
gun = init.getLLRFController(llrf.MACHINE_MODE.PHYSICAL,llrf.LLRF_TYPE.CLARA_LRRG)
# gun = init.getLLRFController(llrf.MACHINE_MODE.PHYSICAL,llrf.LLRF_TYPE.VELA_HRRG)

# monitoring of traces happens automatically
tr1 = gun.getCavRevPwr()
tr2 = gun.getCavFwdPwr()
tr3 = gun.getKlyRevPwr()
tr4 = gun.getKlyFwdPwr()
#print(tr1)
#print(tr2)
#print(tr3)
#print(tr4)
today = datetime.now()
current_date = today.strftime("%d%m%Y_%H-%M-%S")
np.savetxt('gunRV_'+current_date+'.csv', tr1)
np.savetxt('gunFW_'+current_date+'.csv', tr2)
np.savetxt('klyRV_'+current_date+'.csv', tr3)
np.savetxt('klyFW_'+current_date+'.csv', tr4)
plt.plot(tr4, label='Klys Fwd')
plt.show()
raw_input()
'''


import VELA_CLARA_Camera_Control as camx

cam_init = camx.init()
cam_init.setVerbose()
cam_control = cam_init.physical_Camera_Controller()


#mycam = 'S01-CAM-01' # clara S01 YAG 01
#mycam = 'INJ-SCR-02' # VELA YAG 01 # for names see: https://github.com/VELA-CLARA-software/VELA-CLARA-Controllers/blob/master/Config/velaCam.config
#mycam = 'S01-CAM-01' 
mycam = 'CAM02'
#mycam = 'BA1-SCR-01'
#mycam = 'BA1-SCR-02'

cam_control.startAcquiring(mycam)
cam_control.collectAndSave(1)

'''
for x in range(1):
    time.sleep(4) #needs to be at least 4 secinds if issuing collectandsave(1) in a loop
    print "hi **************************************************************" 
    cam_control.collectAndSave(1)
'''


#cam_control.collectAndSave(100)



'''
raw_input()
print "RF power ",  mean_rf
print "RF power ",  mean_FF
print "Charge ",  mean_charge, " +- ", error_charge, " ", charge_list  
print "sol  ",  mean_sol
print "bsol  ",  mean_bsol
'''

raw_input()


