"""
Model for the ADC raw live plot

@author: MFurmaniak
"""

import os, sys, time
from PyQt4 import QtCore
import numpy as np
from datetime import datetime
import pandas as pd

del os.environ["EPICS_CA_AUTO_ADDR_LIST"]
#del os.environ["EPICS_CA_SERVER_PORT"]
os.environ["EPICS_CA_ADDR_LIST"] = "192.168.83.255"
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"

sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release')


#=========================================================================================================================================================================

class model(QtCore.QObject):
    def run(self, result_callback):
        '''Running the app and getting the charge'''
        # define number of shots that you want to have in a buffer
        number_of_shots = 30
        
        print '\n'
        print '                               LOADING CONTROLLERS                                  '
        print '==================================================================================='
        
        import VELA_CLARA_General_Monitor as monx

        # initialize the WCM
        charge_control = monx.init()
        charge_control.setVerbose()
        self.id = charge_control.connectPV('CLA-C09-IOC-CS-04:FMC_1_ADC_0_READ')
        #self.id = charge_control.connectPV('CLA-S01-DIA-DC-01:IN1_DATA_MONITOR')
        
        # setting the size of the buffer
        charge_control.setBufferSize(self.id, number_of_shots)
        print("Connected with id = ", charge_control)
        
        # infinite loop
        while 1<=2:
            self.getWCMCharge(charge_control, result_callback)
                    
        return 'CONGRATS!'
    
    def getWCMCharge(self, charge_control, result_callback):
        '''Getting the charge by loading the buffer and calculating the charge'''
        # to get an buffer you need to clear it first as it fills itself automatically
        charge_control.clearBuffer(self.id)
        # filling the buffer
        while charge_control.isBufferFull(self.id) == False:
               time.sleep(1)
        #print(datetime.now())
        
        # getting the array of arrays (ADC counts)
        array_dict = charge_control.getBuffer(self.id)
        raw_points= np.copy(array_dict.values())
        
        # passing the raw ADC points to the chargeCalc function that calculates charge
        charge = self.chargeCalc(raw_points)
        
        # averaging the points and emitting them as results to plot them live
        points = np.mean(raw_points, axis=0)
        result_callback.emit(points, charge)
    
    def chargeCalc(self, array):                                               
        '''Calculating the charge fromm the ADC counts'''
        mean_array = np.mean(array, axis=0)
        array = np.zeros(len(mean_array))
        for i in range(len(mean_array)):
            if mean_array[i]<0:
                array[i] = (((mean_array[i]+(2^16))*5.630826788717575e-05 - 1.851376732757830)*0.16845)  #always make sure that these scaling factors are correct and up to date
            else:
                array[i] = ((mean_array[i]*5.630826788717575e-05 - 1.851376732757830)*0.16845)

        # new baseline (21/04/2020)-0
        array_avrg = np.mean(array[:300])
        
        # calculatigng charge by integrating (w.r.t. the baseline) only the points that are above the baseline and before the minimum of the signal (overshoot)
        charge = 0
        for i in range(len(array)):
            if array[i]>array_avrg and i<np.argmin(array):
                charge+=(array[i]-array_avrg)*4e-09*1e12
                
        final_charge = charge
        
        return final_charge