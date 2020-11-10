"""
Script for taking a live dark charge measurement, and noting the RF and main SOL settings- USING NOISE TRACE AS THE BASELINE

UPDATED 03.03.2020, adding valve open/close (and turning the rf on and off to do so) at the beginning of each measurement
# RAMPING ADDED TO STABILISE THE GUN... (?)

@author: MFurmaniak
"""

import numpy as np
import csv
from datetime import datetime
import os, sys, time
import matplotlib.pyplot as plt
import pandas as pd

del os.environ["EPICS_CA_AUTO_ADDR_LIST"]
#del os.environ["EPICS_CA_SERVER_PORT"]
os.environ["EPICS_CA_ADDR_LIST"] = "192.168.83.255"
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release')

# creating folders with measurements and noise data
today = datetime.now()
year = today.strftime("%Y")
month = today.strftime("%m")
day = today.strftime("%d")
dirName= 'Measurements/'+year+'/'+month+'/'+day
if not os.path.exists(dirName):
    os.makedirs(dirName)
    print("Directory " , dirName ,  " Created ")
else:    
    print("Directory " , dirName ,  " already exists")
    
dirName2= 'Noise/'+year+'/'+month+'/'+day
if not os.path.exists(dirName2):
    os.makedirs(dirName2)
    print("Directory " , dirName2 ,  " Created ")
else:    
    print("Directory " , dirName2 ,  " already exists")

# specifying the number of shots for each measurement and number of measurements
number_of_shots = 100
number_of_measurements = 5

class WCM(object):
    def __init__(self):
        
        import VELA_CLARA_General_Monitor as monx
        import VELA_CLARA_Vac_Valve_Control as valve
        import VELA_CLARA_LLRF_Control as rfx
        import VELA_CLARA_Camera_Control as camx
        
        # noting the current date and time
        self.current_date = today.strftime("%d%m%Y_%H-%M-%S")
        
        # initialize cameras
        cam_init = camx.init()
        cam_control = cam_init.physical_Camera_Controller()
        cam_init.setVerbose()
        mycam = 'S01-CAM-01'
        cam_control.startAcquiring(mycam) 
        
        # initialize the rf ccontroller
        rfinit = rfx.init()
        rf_control = rfinit.physical_CLARA_LRRG_LLRF_Controller()
        
        # initialise the valve controller
        valveInit = valve.init()
        self.vv = valveInit.physical_Vac_Valve_Controller()
        
        # initialize the general monitor to monitor charge, rf and sol
        general_monitor = monx.init()
        general_monitor.setVerbose()
        
        #PVs needed
        self.id = general_monitor.connectPV('CLA-C09-IOC-CS-04:FMC_1_ADC_0_READ')
        self.rf = general_monitor.connectPV('CLA-GUN-LRF-CTRL-01:ad1:ch1:Power:Wnd:Avg')
        self.sol = general_monitor.connectPV('CLA-GUN-MAG-SOL-02:READI')
        self.bsol = general_monitor.connectPV('CLA-LRG1-MAG-SOL-01:READI')
        
        print '==============================================================================================='
        print '\n'
        print "Connected with id = ", general_monitor 
        print '\n'
        
        # setting the buffer size for the ADC counts
        general_monitor.setBufferSize(self.id, number_of_shots)

        # first locking the feed foward (FF) and then checking the rf setting
        rf_control.lockAmpFF()
        clock1=0
        while rf_control.isFFLocked()==False:
            time.sleep(1)
            clock1+=1
            if clock1>10:
                print 'Error: FF cannot be locked'
                exit()
        self.rf_nominal = rf_control.getAmpFF()
        
        # getting charge from the general monitor several times to get a more accurate val and error
        charge_list=[]
        rf_list = []
        FF_list = []
        sol_list = []
        bsol_list = []
        
        for i in range(number_of_measurements):
            
            count = i+1
            print '---------------------', count, ' out of ', number_of_measurements, '---------------------'
            
            # measuring the noise
            self.closeValve('S01-VALV1', rf_control)
            self.noise100= self.measureNoise(general_monitor)
            self.openValve('S01-VALV1', rf_control)
            
            # checking the feed forward settings
            FF = rf_control.getAmpFF()
            
            # calculating the charge
            result = self.getWCMCharge(general_monitor)
            
            # appending the lists with results
            charge_list.append(result[0])
            rf_list.append(result[1])
            FF_list.append(FF)
            sol_list.append(result[2])
            bsol_list.append(result[3])
        
        # getting an image from a camera        
        if cam_control.isAcquiring(mycam):
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
        
        # averaged charge value and error on the mean
        mean_charge = np.mean(charge_list)
        error_charge = np.std(charge_list)/(np.sqrt(number_of_measurements))
        
        mean_rf = np.mean(rf_list)
        mean_FF = np.mean(FF_list)
        mean_sol = np.mean(sol_list)
        mean_bsol = np.mean(bsol_list)
        
        txtFile = open(dirName+"/charge_"+self.current_date+".txt","w+")
        str1 = 'Number of measurements averaged: '+str(number_of_measurements)
        str2 = '\n'
        str3 = 'Mean Charge:'+str(mean_charge)+' +-'+str(error_charge)+'pC'
        str4 = '\n'
        str5 = 'Mean RF Avrg Pwr:'+str(mean_rf)+'MW'
        str6 = '\n'
        str7 = 'Mean FF:'+str(mean_FF)+' Crocodiles'
        str8 = '\n'
        str9 = 'Mean Sol:'+str(mean_sol)+'A'
        str10 = '\n'
        str11= 'Mean BSol:'+str(mean_bsol)+'A'
        L = [str1, str2, str3, str4, str5, str6, str7, str8, str9, str10, str11]
        txtFile.writelines(L)
        txtFile.close()
        
        # one can save the final plot with the current date
        plt.ylabel('Current [A]')
        plt.title(self.current_date+' (noise subtracted)')
        plt.axhline(y=0, color='r', linestyle=(0,(5,5)), label='Baseline')
        plt.legend(loc='upper right')
        plt.savefig(dirName+'/plot_'+self.current_date+'.png')
        
        print '==============================================================================================='
        print '\n'
        print 'Mean Charge:'+str(mean_charge)+' +-'+str(error_charge)+'pC'
        print '\n'
        
        # finally showing the plot
        plt.show()
        
    def getWCMCharge(self, general_monitor):
        print '--------------------Measuring Signal--------------------------'
        
        '''Getting the charge by loading the buffer and calculating the charge'''
        # to get an buffer you need to clear it first as it fills itself automatically
        general_monitor.clearBuffer(self.id)
        # filling the buffer
        while general_monitor.isBufferFull(self.id) == False:
               time.sleep(1)
               print("Buffer not full")
        # getting the values for RF and Sol at the time when the buffer is full- approximation, should use 3 parallel running buffers to get the most accurate values for all 3       
        rf_avg_power = general_monitor.getValue(self.rf)/1000000
        sol = general_monitor.getValue(self.sol)
        bsol = general_monitor.getValue(self.bsol)
        
        # getting the array of arrays (ADC counts)
        points = general_monitor.getBuffer(self.id)
        
        # passing the raw ADC points to the chargeCalc function that calculates charge
        charge = self.chargeCalc(points)
        print '\n'
        print '#############################################################'
        print 'Total charge (noise subtracted) : ', charge, 'pC'
        print 'RF Avrg Pwr: ', rf_avg_power, 'MW'
        print 'Solenoid strength: ', sol, 'A'
        print 'Bsol strength: ', bsol, 'A'

        return charge, rf_avg_power, sol, bsol
        
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


        # calculatigng charge by integrating (w.r.t. the baseline) only the points that are above the baseline and before the minimum of the signal (overshoot)
        #charge = 0
        #for i in range(len(array)):
        #    if array[i]>self.avrg_array and i<np.argmin(array):
        #        charge+=(array[i]-self.avrg_array)*4e-09*1e12
                
        # calculating charge due to the noise in order to then subtract it from the signal charge; integrating w.r.t. the baseline all the points that are above the baseline and before the signal minimum
        #charge_noise100 = 0
        #for j in range(len(noise100)):
        #    if self.noise100[j]>self.avrg_array  and j<np.argmin(array): 
         #       charge_noise100+=(self.noise100[j]-self.avrg_array)*4e-09*1e12
        
        #final_charge = charge-charge_noise100
        
        # plotting the results
        plt.plot(array_wrt_0, label='Signal: '+str(final_charge)+'pC')
        #plt.plot(array, label='Raw signal')
        #plt.plot(array_wrt_0, label='Signal-noise: '+str(final_charge)+'pC')
        #plt.plot(self.noise100, label='Noise')
        #plt.legend(loc='upper right')
        #plt.show()
        
        return final_charge

    def openValve(self, name, rf_control):
        rf_control.setAmpSP(0)
        clock5=0
        while rf_control.getAmpFF()>1:
            time.sleep(1)
            clock5+=1
            if clock5>10:
                print 'Error: RF cannot be set to 0'
                exit()
        
        self.vv.open(name)
        clock6=0
        while self.vv.isOpen(name)==False:
            time.sleep(1)
            clock6+=1
            if clock6>10:
                print 'Error: Valve is not opening'
                exit()
                        
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
                    exit()
        
    def closeValve(self, name, rf_control):
        rf_control.setAmpSP(0)
        clock2 = 0
        while rf_control.getAmpFF()>1:
            time.sleep(1)
            clock2+=1
            if clock2>10:
                print 'Error: RF cannot be set to 0'
                exit()
        
        self.vv.close(name)
        clock3=0
        while self.vv.isClosed(name)==False:
            time.sleep(1)
            clock3+=1
            if clock3>10:
                print 'Error: Valve is not closing'
                exit()
        
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
                    exit()
        
        
    def measureNoise(self, general_monitor):
        print '--------------------Measuring Noise--------------------------'
        print '/n'
        # to get an buffer you need to clear it first as it fills itself automatically
        general_monitor.clearBuffer(self.id)
        # filling the buffer
        while general_monitor.isBufferFull(self.id) == False:
               time.sleep(1)
               print("Buffer not full")

        # getting the array of arrays (ADC counts)
        points = general_monitor.getBuffer(self.id)
        
        # caluclating noise
        noise = self.noiseCalc(points)
        avrg_array=np.mean(noise)

        # one san save the parameters as a text file with the date and time when the measurement was taken
        np.savetxt(dirName2+'/noise_'+self.current_date+'.csv', noise)
        
        # check if noise shape looks reasonable
        #plt.plot(noise, label='Noise')
        #plt.ylabel('Current [A]')
        #plt.title(self.current_date)
        #plt.axhline(y=avrg_array, color='gray', linestyle=(0,(5,5)), label='Baseline')
        #plt.legend(loc='upper right')
        #plt.show()
        
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

WCM()
        
