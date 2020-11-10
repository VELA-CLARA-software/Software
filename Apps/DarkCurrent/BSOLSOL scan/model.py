"""
Script for data acquisition and charge calculation

@author: MFurmaniak
"""

import os, sys, time
from PyQt4 import QtCore
import numpy as np
import pandas as pd
import csv
from datetime import datetime
import matplotlib.pyplot as plt

del os.environ["EPICS_CA_AUTO_ADDR_LIST"]
#del os.environ["EPICS_CA_SERVER_PORT"]
os.environ["EPICS_CA_ADDR_LIST"] = "192.168.83.255"
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release')

# importing the noise trace from Feb 2020- valve closed; 100 shots averaged
#noise100 = np.array(pd.read_csv('noise12022020.csv', sep=','))

#=========================================================================================================================================================================

class classmachine(QtCore.QObject):
    
    def check_if_ON(self, mag_control):
        '''Function which checks that 
            all magnets are on '''
        
        print 'Checking if magnets are on...'
        if str(mag_control.getMagPSUState('SOL')) == 'MAG_PSU_OFF' or str(mag_control.getMagPSUState('SOL')) == 'MAG_PSU_ERROR' or str(mag_control.getMagPSUState('SOL')) == 'MAG_PSU_NONE':
            mag_control.switchONpsu('SOL')
            print 'SOL is now ON:    ', mag_control.getMagPSUState('SOL')
        else: 
            print 'SOL was already ON:', mag_control.getMagPSUState('SOL')
        if str(mag_control.getMagPSUState('BSOL')) == 'MAG_PSU_OFF' or str(mag_control.getMagPSUState('BSOL')) == 'MAG_PSU_ERROR' or str(mag_control.getMagPSUState('BSOL')) == 'MAG_PSU_NONE':
            mag_control.switchONpsu('BSOL')
            print 'BSOL is now ON:    ', mag_control.getMagPSUState('BSOL')
        else:
            print 'BSOL was already ON:', mag_control.getMagPSUState('BSOL')
        
        # same thing can be applied to correctors
        #if str(mag_control.getMagPSUState('HCOR01')) == 'MAG_PSU_OFF' or str(mag_control.getMagPSUState('HCOR01')) == 'MAG_PSU_ERROR' or str(mag_control.getMagPSUState('HCOR01')) == 'MAG_PSU_NONE':
        #    mag_control.switchONpsu('HCOR01')
        #    print 'HCOR01 is now ON:    ', mag_control.getMagPSUState('HCOR01')
        #else: 
        #    print 'HCOR01 was already ON:', mag_control.getMagPSUState('HCOR01')
        #if str(mag_control.getMagPSUState('VCOR01')) == 'MAG_PSU_OFF' or str(mag_control.getMagPSUState('VCOR01')) == 'MAG_PSU_ERROR' or str(mag_control.getMagPSUState('VCOR01')) == 'MAG_PSU_NONE':
        #    mag_control.switchONpsu('VCOR01')
        #    print 'VCOR01 is now ON:    ', mag_control.getMagPSUState('VCOR01')
        #else:
        #    print 'VCOR01 was already ON:', mag_control.getMagPSUState('VCOR01')
        print '\n'
        
    def set_sol(self, mag_control, cam_control, charge_control, rf_control, valve_control, sol, bsol, rf):
        '''Function which sets the sol, bsol and rf values 
            and then takes photos and saves the charge from WCM '''
        
        #setting rf amp to 0 before we change sols, prevents gun from tripping
        rf_control.setAmpSP(0)
        clock1=0
        while abs(rf_control.getAmpFF())>0.1:                                                                # on a PHYSICAL machine add tolerance- beacuse it will never give an accurate value
            print 'Setting RF Amplitude...'
            time.sleep(1)
            clock1+=1
            if clock1>10:
                print 'Error: RF cannot be set to 0'
                sys.exit()
        rf_val = rf_control.getAmpFF()
        print 'RF Amplitude set to 0!'
        print 'RF Amp = ', rf_val
        print '\n'
        
        # changing SOL and BSOL values
        print 'Settings: SOL=', sol, 'BSOL=', bsol
        print '\n'
        mag_control.setSI('SOL', sol)
        mag_control.setSI('BSOL', bsol)                                                                   # remember to change to BSOL on a PHYSICAL machine
        print 'SOL', 'BSOL'
        while abs(mag_control.getRI('SOL') - sol) > 0.1 or  abs(mag_control.getRI('BSOL') - bsol) > 0.1:                        # for a PHYSICAL machine added tolerance- beacuse it will never give an accurate value; within 0.1A
            print mag_control.getRI('SOL'), mag_control.getRI('BSOL')
            time.sleep(1)
        print 'Finished!'
        print '\n'
        print 'New SOL = ', mag_control.getRI('SOL')
        print 'New BSOL = ', mag_control.getRI('BSOL')
        print '\n'
        
        #setting rf amp
        rf_control.setAmpSP(rf)
        clock1=0
        while abs(rf_control.getAmpFF()-rf)>0.1:                                                                # on a PHYSICAL machine add tolerance- beacuse it will never give an accurate value
            print 'Setting RF Amplitude...'
            time.sleep(1)
            clock1+=1
            if clock1>10:
                print 'Error: RF cannot be set'
                sys.exit()
        rf_val = rf_control.getAmpFF()
        print 'RF Amplitude set!'
        print 'RF Amp = ', rf_val
        
        # getting value from the WCM 
        #chargenow = np.random.random()*1000                                                                   # for now use a random number
        result = self.DarkCurrentValve(charge_control, rf_control, valve_control)
        charge = result[0] 
        rf_avrg_pwr = result[1] 
        print 'Charge = ', charge
        
        # getting an image from a camera
        if cam_control.isAcquiring(self.mycam):
            print 'Camera aquiring...'
            time.sleep(1)
            cam_control.collectAndSave(1)
            time.sleep(5)
        else:
            print 'xxx'
            print 'xxx'
            print 'xxx'
            print "CAMERA NOT ACQUIRING"
            print 'xxx'
            print 'xxx'
            print 'xxx'
        
            
        # getting the HCOR01 and VCOR01 values
        hcor01_val = mag_control.getRI('HCOR01')
        vcor01_val = mag_control.getRI('VCOR01')
        
        print 'HCOR01 = ', hcor01_val
        print 'VCOR01 = ', vcor01_val
         
        print 'Saving data...'

        return sol, bsol, chargenow, hcor01_val, vcor01_val, rf_val, rf_avg_power
    
    def loop(self, function, sol, bsol, rf, progress_callback, result_callback, current_val_callback):
        '''Loop function'''
        
        # specifying the number of shots for each measurement and number of measurements
        self.number_of_shots = 100
        self.number_of_measurements = 10
        
        #starting sol values
        sol_start = sol[0]
        bsol_start = bsol[0]
        rf_start = rf[0]
        
        # I initiallize the controllers within my for loop because otherwise it takes ages to set them to a particular value
        print '\n'
        print '                               LOADING CONTROLLERS                                  '
        print '==================================================================================='
        
        import VELA_CLARA_Magnet_Control as magx
        import VELA_CLARA_General_Monitor as monx
        import VELA_CLARA_Camera_Control as camx
        import VELA_CLARA_Charge_Control as chargex
        import VELA_CLARA_LLRF_Control as rfx
        import VELA_CLARA_Vac_Valve_Control as valve

        # initialise the valve controller
        valveInit = valve.init()
        valve_control = valveInit.physical_Vac_Valve_Controller()
        
        # initialize magnet controller
        mag_init = magx.init()
        mag_control = mag_init.physical_VELA_INJ_Magnet_Controller()
                
        # initialize cameras
        cam_init = camx.init()
        cam_control = cam_init.physical_Camera_Controller()
        cam_init.setVerbose()
        self.mycam = 'S01-CAM-01'
        cam_control.startAcquiring(self.mycam) 
        
        # initialize the WCM
        charge_control = monx.init()
        self.ADC = 'CLA-C09-IOC-CS-04:FMC_1_ADC_0_READ'
        self.id = charge_control.connectPV(self.ADC)
        # setting the buffer size for the ADC counts
        charge_control.setBufferSize(self.id, self.number_of_shots)
        
        # initialize the rf ccontroller
        rfinit = rfx.init()
        rf_control = rfinit.physical_CLARA_LRRG_LLRF_Controller()
        # first locking the feed foward (FF) and then checking the rf setting
        rf_control.lockAmpFF()
        clock1=0
        while rf_control.isFFLocked()==False:
            time.sleep(1)
            clock1+=1
            if clock1>10:
                print 'Error: FF cannot be locked'
                sys.exit()
        self.rf = charge_control.connectPV('CLA-GUN-LRF-CTRL-01:ad1:ch1:Power:Wnd:Avg')
        
        print '==================================================================================='
        print '\n'
        
        self.check_if_ON(mag_control)
        
        measurement = 0
            
        for i in range(rf[1]):
            if rf[1]==1:
                rf_val = rf_start
            else:
                rf_val = (rf[2]-rf[0])/(rf[1]-1)*i+ rf_start
            for j in range(sol[1]):
                for k in range(bsol[1]):
                    if sol[1]==1:
                        sol_val = sol_start
                    else:
                        sol_val = (sol[2]-sol[0])/(sol[1]-1)*j+ sol_start
                         
                    if bsol[1]==1:
                        bsol_val = bsol_start
                    else:
                        bsol_val = (bsol[2]-bsol[0])/(bsol[1]-1)*k+ bsol_start
                    
                    measurement = measurement + 1
                    percent = float(measurement*100/(bsol[1]*sol[1]*rf[1]))
                    print '-----------------------------------------------------------------------------------'
                    print '#', measurement, '-----Percent: ', percent

                    progress_callback.emit(percent)
                                      
                    result_sweep = function(mag_control, cam_control, mon_init, rf_control, valve_control, sol_val, bsol_val, rf_val)
                    current_val_callback.emit(result_sweep[2], sol_val, bsol_val, result_sweep[6])
                    result_callback.emit(result_sweep[0], result_sweep[1], result_sweep[2], result_sweep[3], result_sweep[4], result_sweep[5], result_sweep[6])
                    
        return 'CONGRATS!'
     
    def DarkCurrentValve(self, charge_control, rf_control, valve_control):
        
        # getting charge from the general monitor several times to get a more accurate val and error
        charge_list=[]
        rf_list = []
        
        for i in range(self.number_of_measurements):
            
            count = i+1
            print '---------------------', count, ' out of ', number_of_measurements, '---------------------'
            
            # measuring the noise
            self.closeValve('S01-VALV1',valve_control, rf_control)
            self.noise100= self.measureNoise(charge_control)
            self.openValve('S01-VALV1',valve_control, rf_control)
            
            # calculating the charge
            result = self.getWCMCharge(charge_control)
            
            # appending the lists with results
            charge_list.append(result[0])
            rf_list.append(result[1])

        # averaged charge value and error on the mean
        mean_charge = np.mean(charge_list)
        error_charge = np.std(charge_list)/(np.sqrt(number_of_measurements))
        
        mean_rf = np.mean(rf_list)
        
        print '==============================================================================================='
        print '\n'
        print 'Mean Charge:'+str(mean_charge)+' +-'+str(error_charge)+'pC'
        print '\n'
        
        return charge, mean_rf

        
    def getWCMCharge(self, charge_control):
        print '--------------------Measuring Signal--------------------------'
        
        '''Getting the charge by loading the buffer and calculating the charge'''
        # to get an buffer you need to clear it first as it fills itself automatically
        charge_control.clearBuffer(self.id)
        # filling the buffer
        while charge_control.isBufferFull(self.id) == False:
               time.sleep(1)
               print("Buffer not full")
        # getting the values for RF and Sol at the time when the buffer is full- approximation, should use 3 parallel running buffers to get the most accurate values for all 3       
        rf_avg_power = charge_control.getValue(self.rf)/1000000
        
        # getting the array of arrays (ADC counts)
        points = charge_control.getBuffer(self.id)
        
        # passing the raw ADC points to the chargeCalc function that calculates charge
        charge = self.chargeCalc(points)
        print '\n'
        print '#############################################################'
        print 'Total charge (noise subtracted) : ', charge, 'pC'
        print 'RF Avrg Pwr: ', rf_avg_power, 'MW'

        return charge, rf_avg_power
        
    def chargeCalc(self, array_dict):                                
        '''Calculating the charge fromm the ADC counts'''
        array = np.copy(array_dict.values())


        mean_array = np.mean(array, axis=0)
        array = np.zeros(len(mean_array))
        
        for i in range(len(mean_array)):
            if mean_array[i]<0:
                array[i] = (((mean_array[i]+(2^16))*5.630826788717575e-05 - 1.851376732757830)*0.16845)         #always make sure that these scaling factors are correct and up to date
            else:
                array[i] = ((mean_array[i]*5.630826788717575e-05 - 1.851376732757830)*0.16845)


        # baseline 0!
        array_wrt_0 = np.subtract(array,self.noise100)
        
        # calculatigng charge by integrating (w.r.t. the baseline) only the points that are above the baseline and before the minimum of the signal (overshoot)
        final_charge = 0
        for i in range(len(array_wrt_0)):
            if array_wrt_0[i]>0 and i<np.argmin(array_wrt_0):
                final_charge+=(array_wrt_0[i])*4e-09*1e12

        return final_charge

    def openValve(self, name, valve_control, rf_control):
        rf_control.setAmpSP(0)
        clock5=0
        while rf_control.getAmpFF()>1:
            time.sleep(1)
            clock5+=1
            if clock5>10:
                print 'Error: RF cannot be set to 0'
                sys.exit()
        
        valve_control.open(name)
        clock6=0
        while valve_control.isOpen(name)==False:
            time.sleep(1)
            clock6+=1
            if clock6>10:
                print 'Error: Valve is not opening'
                sys.exit()
                        
        for i in range(4):
            factor = 0.25*(i+1)
            setValue = self.rf_nominal*factor
            rf_control.setAmpSP(setValue)
            time.sleep(1)
            clock7 = 0
            while (rf_control.getAmpFF()-setValue)>setValue*0.01:    #1% tolerance
                time.sleep(1)
                clock7+=1
                if clock7>10:
                    print 'Error: RF cannot be set'
                    sys.exit()
        
    def closeValve(self, name, valve_control, rf_control):
        rf_control.setAmpSP(0)
        clock2 = 0
        while rf_control.getAmpFF()>1:
            time.sleep(1)
            clock2+=1
            if clock2>10:
                print 'Error: RF cannot be set to 0'
                sys.exit()
        
        valve_control.close(name)
        clock3=0
        while valve_control.isClosed(name)==False:
            time.sleep(1)
            clock3+=1
            if clock3>10:
                print 'Error: Valve is not closing'
                sys.exit()
        
        for i in range(4):
            factor = 0.25*(i+1)
            setValue = self.rf_nominal*factor
            rf_control.setAmpSP(setValue)
            time.sleep(1)
            clock4 = 0
            while (rf_control.getAmpFF()-setValue)>setValue*0.01:    #1% tolerance
                time.sleep(1)
                clock4+=1
                if clock4>10:
                    print 'Error: RF cannot be set'
                    sys.exit()
        
        
    def measureNoise(self, charge_control):
        print '--------------------Measuring Noise--------------------------'
        print '/n'
        # to get an buffer you need to clear it first as it fills itself automatically
        charge_control.clearBuffer(self.id)
        # filling the buffer
        while charge_control.isBufferFull(self.id) == False:
               time.sleep(1)
               print("Buffer not full")

        # getting the array of arrays (ADC counts)
        points = charge_control.getBuffer(self.id)
        
        # caluclating noise
        noise = self.noiseCalc(points)

        print 'DONE!'
        return noise
    
    def noiseCalc(self, array_dict):                                
        '''Calculating the current due to noise from the ADC counts'''
        array = np.copy(array_dict.values())

        mean_array = np.mean(array, axis=0)
        array = np.zeros(len(mean_array))
        
        for i in range(len(mean_array)):
            if mean_array[i]<0:
                array[i] = (((mean_array[i]+(2^16))*5.630826788717575e-05 - 1.851376732757830)*0.16845)         #always make sure that these scaling factors are correct and up to date
            else:
                array[i] = ((mean_array[i]*5.630826788717575e-05 - 1.851376732757830)*0.16845)      
        return array
    