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
#import pandas as pd
import svd_module

del os.environ["EPICS_CA_AUTO_ADDR_LIST"]
#del os.environ["EPICS_CA_SERVER_PORT"]
os.environ["EPICS_CA_ADDR_LIST"] = "192.168.83.255"
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release')


import VELA_CLARA_LLRF_Control as llrf
init = llrf.init()
gun = init.getLLRFController(llrf.MACHINE_MODE.PHYSICAL,llrf.LLRF_TYPE.CLARA_LRRG)     
cavrevpwr = gun.getCavRevPwr()
cavfwdpwr = gun.getCavFwdPwr()
klysrevpwr = gun.getKlyRevPwr()
klysfwdpwr = gun.getKlyFwdPwr()


#today = datetime.now()
#current_date = today.strftime("%d%m%Y_%H-%M-%S")

#np.savetxt('gunFW_'+current_date+'.csv', cavfwdpwr)
#np.savetxt('gunRV_'+current_date+'.csv', cavrevpwr)
#np.savetxt('klyFW_'+current_date+'.csv', klysfwdpwr)
#np.savetxt('klyRV_'+current_date+'.csv', klysrevpwr)


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
number_of_shots = 200
number_of_measurements = 3


class WCM(object):
    def __init__(self):
        
        import VELA_CLARA_General_Monitor as monx
#        import VELA_CLARA_Vac_Valve_Control as valve
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

 #       import VELA_CLARA_LLRF_Control as llrf
 #       init = llrf.init()
 #       gun = init.getLLRFController(llrf.MACHINE_MODE.PHYSICAL,llrf.LLRF_TYPE.CLARA_LRRG)        
        
        # initialize the rf ccontroller
        rfinit = rfx.init()
        self.rf_control = rfinit.physical_CLARA_LRRG_LLRF_Controller()
        
 #       gun = rfinit.getLLRFController(rfx.MACHINE_MODE.PHYSICAL,rfx.LLRF_TYPE.CLARA_LRRG)
        # initialise the valve controller
 #       fvalveInit = valve.init()
 #       self.vv = valveInit.physical_Vac_Valve_Controller()
        
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
 #       rf_control.lockAmpFF()
 #      clock1=0
 #       while rf_control.isFFLocked()==False:
 #           time.sleep(1)
 #           clock1+=1
 #           if clock1>10:
 #               print 'Error: FF cannot be locked'
 #               exit()
 #       self.rf_nominal = rf_control.getAmpFF()
        
        # getting charge from the general monitor several times to get a more accurate val and error
        self.charge_list=[]
        self.rf_list = []
        self.FF_list = []
        self.sol_list = []
        self.bsol_list = []
               
        # Open log file  
        savetoworkfolder=True
        self.dir = '\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Work\\'+time.strftime("%Y\\%m\\%d")+'\\' if savetoworkfolder else '.'
        self.rfdir = '\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Work\\'+time.strftime("%Y\\%m\\%d")+'\\RFtraces\\' if savetoworkfolder else '.\\RFtraces\\'
        self.svddir = '\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Work\\'+time.strftime("%Y\\%m\\%d")+'\\SVD\\' if savetoworkfolder else '.\\SVD\\'
        self.wcmdir = '\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Work\\'+time.strftime("%Y\\%m\\%d")+'\\WCM\\' if savetoworkfolder else '.\\WCM\\'

        try:
            os.makedirs(self.rfdir)
            os.makedirs(self.svddir) 
            os.makedirs(self.wcmdir)             
        except OSError:
            if not os.path.isdir(self.rfdir):
                print('Error creating directory - saving to local directory')
                self.dir = '.'
        self.outF = open(self.dir+"/darkCmeasts"+self.current_date+".txt", "w")
        line = "--------------------Dark Current Measurement:---------------------------" 
        self.outF.write(line)
        self.outF.write("\n")
        line = "Measurement started at: "+self.current_date 
        self.outF.write(line)
        self.outF.write("\n")        
        line = "number of WCM measurements: "+str(number_of_measurements)+" \n"
        self.outF.write(line)
        line = "number of shots in WCM measurement: "+str(number_of_shots)+" \n"
        self.outF.write(line)
        line = "number of shots in WCM measurement: "+str(number_of_shots)+" \n"
#        outF.close()
#        raw_input()
#        exit()
        
        if cam_control.isAcquiring(mycam):
            print 'Camera aquiring...'
            time.sleep(1)
            cam_control.collectAndSave(1)
            time.sleep(5)
        
        self.getmeasurement(general_monitor)
        self.outF.close()

    def getmeasurement(self,general_monitor): 
        print('Starting the measurement **************** getmeasurement()')
        sol = general_monitor.getValue(self.sol)
        bsol = general_monitor.getValue(self.bsol)
        line1 = "Main Sol: "+str(sol)+" \n"
        line2 = "Bucking Sol: "+str(bsol)+" \n"
        lines = [line1,line2]
        self.outF.writelines(lines)

        for i in range(number_of_measurements):               
            count = i+1
            print '---------------------', count, ' out of ', number_of_measurements, '---------------------' 
            line = "**Measurement: "+str(count)+" \n"
            self.outF.write(line)
            
            # checking and writing the RF settings 
            #today = datetime.now()
            self.current_date_i = str(self.current_date+"_"+str(count))
            FF = self.rf_control.getAmpFF()
            line = "RF amplitude: "+str(FF)+" \n"
            self.outF.write(line)
            rf_avg_power = general_monitor.getValue(self.rf)/1000000
            line1 = "RF power: "+str(rf_avg_power)+" \n"
            self.outF.write(line1)
            line1 = "RF traces at: "+str(self.rfdir+"..."+self.current_date_i+" \n")
            self.outF.write(line1)
            cavrevpwr = gun.getCavRevPwr()
            cavfwdpwr = gun.getCavFwdPwr()
            klysrevpwr = gun.getKlyRevPwr()
            klysfwdpwr = gun.getKlyFwdPwr()
#            np.savetxt(self.dir+'test.csv', cavfwdpwr)
            np.savetxt(self.rfdir+'gunFW_'+self.current_date_i+'.csv', cavfwdpwr)
            np.savetxt(self.rfdir+'gunRV_'+self.current_date_i+'.csv', cavrevpwr)
            np.savetxt(self.rfdir+'klyFW_'+self.current_date_i+'.csv', klysfwdpwr)
            np.savetxt(self.rfdir+'klyRV_'+self.current_date_i+'.csv', klysrevpwr)

 
            # calculating the charge
            result = self.getWCMCharge(general_monitor)
            line1 = "WCM traces at: "+str(self.wcmdir+"WCM..."+self.current_date_i+" \n")
            self.outF.write(line1)
            line1 = "Charge averaged over shots: "+str(result[0])+" +- "+str(result[1])+"pC\n"
            self.outF.write(line1)
            line1 = "Charge results at: "+str(self.svddir+"..."+self.current_date_i)+" \n"
            self.outF.write(line1)
            
            
            # appending the lists with results
            self.charge_list.append(result)
            self.rf_list.append(rf_avg_power)
            self.FF_list.append(FF)                      
                      
        # averaged charge value and error on the mean
        mean_charge = np.mean(self.charge_list)
        error_charge = np.std(self.charge_list)/(np.sqrt(number_of_measurements))
        
        mean_rf = np.mean(self.rf_list)
        mean_FF = np.mean(self.FF_list)
        mean_sol = np.mean(self.sol_list)
        mean_bsol = np.mean(self.bsol_list)
        
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
        # getting the array of arrays (ADC counts)
        points = general_monitor.getBuffer(self.id)
        np.savetxt(self.wcmdir+'WCMraw_'+self.current_date_i+'.txt', np.mean(points.values(),axis=0))
        
        #print(points),
        # passing the raw ADC points to the chargeCalc function that calculates charge
        charge = self.chargesvdcalc(points)
        

        
        tcharge = 999 
        print '\n'
        print '#############################################################'
        print 'Total charge (noise subtracted) : ', tcharge, 'pC'
#        print 'RF Avrg Pwr: ', rf_avg_power, 'MW'
#        return charge, rf_avg_power
        return charge[0],charge[1]
        
    def chargesvdcalc(self, array_dict):
        print '--------------------SVD calc--------------------------'
        print '/n'
        # to get an buffer you need to clear it first as it fills itself automatically
        values = []       
        array = np.copy(array_dict.values())     
        np_values = np.array(values, dtype=np.float)       
        np_values = (array*5.63083E-5)-1.8514 
        
        np.savetxt(self.wcmdir+'WCMscaled_'+self.current_date_i+'.txt', np.mean(np_values,axis=0))
#        np.savetxt(dirName+'/WCMdata_'+self.current_date+'.csv', np_values)

        
        mean_array = np.mean(np_values, axis=0)
        final_charge = 999
        plt.plot(mean_array, label='Signal: '+str(final_charge)+'pC')
        
        # Get the charge via svd calculation.  
        #print(np_values)         
        noiseRemover = svd_module.svdNoiseRemover()
        noiseRemover.SVD(values=np_values, dim=1)
        noiseRemover.genModes(values = np_values, freq_s = 250e6, n_modes = 11)
        chresult = noiseRemover.calculateDarkCharge()
#        noiseRemover.writeToCSV()
        noiseRemover.writesvdresults(self.svddir,self.current_date_i)
        return chresult
        
        
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
        
