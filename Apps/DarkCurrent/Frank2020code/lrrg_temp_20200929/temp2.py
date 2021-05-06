

import numpy as np
import csv
from datetime import datetime
import os, sys, time
import matplotlib.pyplot as plt
#import pandas as pd
import svd_module

del os.environ["EPICS_CA_AUTO_ADDR_LIST"]
#del os.environ["EPICS_CA_SERVER_PORT"]
os.environ["EPICS_CA_ADDR_LIST"] = "192.168.83.255"
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release')

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
