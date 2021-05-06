import numpy as np
import csv
from datetime import datetime
import os, sys, time
import matplotlib.pyplot as plt
#import pandas as pd


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

#if not os.path.exists(dirName):
#    os.makedirs(dirName)
#    print("Directory " , dirName ,  " Created ")
#else:    
#    print("Directory " , dirName ,  " already exists")
    
#dirName2= 'Noise/'+year+'/'+month+'/'+day
#if not os.path.exists(dirName2):
#    os.makedirs(dirName2)
#    print("Directory " , dirName2 ,  " Created ")
#else:    
#    print("Directory " , dirName2 ,  " already exists")
	
import VELA_CLARA_General_Monitor as monx


general_monitor = monx.init()
general_monitor.setVerbose()
        
#PVs needed
#CLA-C09-IOC-CS-04:FMC_1_ADC_0_READ is CLARA WCM
#EBT-B03-IOC-CS-04:FMC_1_ADC_0_READ is VELA WCM 
id = general_monitor.connectPV('CLA-C09-IOC-CS-04:FMC_1_ADC_0_READ') # LRG
#id = general_monitor.connectPV('EBT-B03-IOC-CS-04:FMC_1_ADC_0_READ') # HRG
#rf = general_monitor.connectPV('CLA-GUN-LRF-CTRL-01:ad1:ch1:Power:Wnd:Avg')
#sol = general_monitor.connectPV('CLA-GUN-MAG-SOL-02:READI')
#bsol = general_monitor.connectPV('CLA-LRG1-MAG-SOL-01:READI')      

number_of_shots = 10
general_monitor.setBufferSize(id, number_of_shots)

number_of_measurements = 1
for i in range(number_of_measurements):
    count = i+1
    print '---------------------', count, ' out of ', number_of_measurements, '---------------------'
	
    while general_monitor.isBufferFull(id) == False:
        time.sleep(1)
        print("Buffer not full")
		
    points = general_monitor.getBuffer(id)
	
    print points
	
    
	
    array = np.copy(points.values())
	
    np.savetxt('points.csv', array)

    mean_array = np.mean(array, axis=0)
    array = np.zeros(len(mean_array))
        
    for i in range(len(mean_array)):
        if mean_array[i]<0:
            array[i] = (((mean_array[i]+(2^16))*5.630826788717575e-05 - 1.851376732757830)*0.16845)         #always make sure that these scaling factors are correct and up to date
        else:
            array[i] = ((mean_array[i]*5.630826788717575e-05 - 1.851376732757830)*0.16845)
			
    print "The array shape is ", len(points) 			
    np.savetxt('pointsaveraged.csv', array)	
    plt.plot(array, label='Signal')
    plt.savefig('plot.png')
        
    plt.show()