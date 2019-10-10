"""
Created on Wed Sep 18 11:22:21 2019

@author: qqi63789
"""

import os, sys, time, csv
from PyQt4 import QtGui, QtCore
import numpy as np

os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12"
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
os.environ["EPICS_CA_SERVER_PORT"]="6000" 
sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release')

#=========================================================================================================================================================================

class classmachine(QtCore.QObject):
    
    #result = pyqtSignal(float, float, float)
    
    def check_if_ON(self, mag_control):
        print 'Checking if magnets are on...'
        if str(mag_control.getMagPSUState('SOL')) == 'MAG_PSU_OFF' or str(mag_control.getMagPSUState('SOL')) == 'MAG_PSU_ERROR' or str(mag_control.getMagPSUState('SOL')) == 'MAG_PSU_NONE':
            mag_control.switchONpsu('SOL')
            print 'SOL is now ON:    ', mag_control.getMagPSUState('SOL')
        else: 
            print 'SOL was already ON:', mag_control.getMagPSUState('SOL')
        if str(mag_control.getMagPSUState('QUAD01')) == 'MAG_PSU_OFF' or str(mag_control.getMagPSUState('QUAD01')) == 'MAG_PSU_ERROR' or str(mag_control.getMagPSUState('QUAD01')) == 'MAG_PSU_NONE':
            mag_control.switchONpsu('QUAD01')
            print 'BSOL is now ON:    ', mag_control.getMagPSUState('QUAD01')
        else:
            print 'BSOL was already ON:', mag_control.getMagPSUState('QUAD01')
        if str(mag_control.getMagPSUState('HCOR01')) == 'MAG_PSU_OFF' or str(mag_control.getMagPSUState('HCOR01')) == 'MAG_PSU_ERROR' or str(mag_control.getMagPSUState('HCOR01')) == 'MAG_PSU_NONE':
            mag_control.switchONpsu('HCOR01')
            print 'HCOR01 is now ON:    ', mag_control.getMagPSUState('HCOR01')
        else: 
            print 'HCOR01 was already ON:', mag_control.getMagPSUState('HCOR01')
        if str(mag_control.getMagPSUState('VCOR01')) == 'MAG_PSU_OFF' or str(mag_control.getMagPSUState('VCOR01')) == 'MAG_PSU_ERROR' or str(mag_control.getMagPSUState('VCOR01')) == 'MAG_PSU_NONE':
            mag_control.switchONpsu('VCOR01')
            print 'VCOR01 is now ON:    ', mag_control.getMagPSUState('VCOR01')
        else:
            print 'VCOR01 was already ON:', mag_control.getMagPSUState('VCOR01')
        print '\n'
        
    def set_sol(self, mag_control, cam_control, charge_control, rf_control, sol, bsol, rf):
        
        #setting rf amp
        rf_control.setAmpMVM(rf)
        while rf_control.getAmpMVM() != rf:                                                                # on a PHYSICAL machine add tolerance- beacuse it will never give an accurate value
            print 'Setting RF Amplitude...'
            time.sleep(1)
        rf_val = rf_control.getAmpMVM()
        print 'RF Amplitude set!'
        print 'RF Amp = ', rf_val
        
        # changing SOL and BSOL values
        print 'Settings: SOL=', sol, 'BSOL=', bsol
        print '\n'
        mag_control.setSI('SOL', sol)
        mag_control.setSI('QUAD01', bsol)
        print 'SOL', 'BSOL'
        while mag_control.getRI('SOL') != sol or mag_control.getRI('QUAD01') != bsol:                        # on a PHYSICAL machine add tolerance- beacuse it will never give an accurate value
            print mag_control.getRI('SOL'), mag_control.getRI('QUAD01')
            time.sleep(1)
        print 'Finished!'
        print '\n'
        print 'New SOL = ', mag_control.getRI('SOL')
        print 'New BSOL = ', mag_control.getRI('QUAD01')
        
        # getting value from the WCM 
        chargenow = np.random.random()*100
        #chargenow = charge_control.getWCMCharge()
        print 'Charge = ', chargenow
        
        # getting an image from a camera
        mycam = 'S01-CAM-01'
        cam_control.startAcquiring(mycam)                                                                    # remember to save the path to the photo in your csv file
        while cam_control.isAcquiring(mycam):
            print 'Camera aquiring...'
            time.sleep(2)
        else:
            print "CAMERA NOT ACQUIRING"
            
        # getting the HCOR01 and VCOR01 values
        hcor01_val = mag_control.getRI('HCOR01')
        vcor01_val = mag_control.getRI('VCOR01')
        
        print 'HCOR01 = ', hcor01_val
        print 'VCOR01 = ', vcor01_val
         
        print 'Saving data...'
#        # saving data to a csv file
##        with open('Documents\\VirtualAccelerator\\app3\\DC_data.csv', 'ab') as f:
##            thewriter = csv.writer(f)
##            thewriter.writerow([sol, bsol, chargenow, hcor01_val, vcor01_val, rf_val])
#        print 'Data saved'
#        print '\n'
#        
        #self.result.emit(sol, bsol, chargenow)
        
        return sol, bsol, chargenow, hcor01_val, vcor01_val, rf_val
       # raw_input("hit any key to exit")
    
    def loop(self, function, sol, bsol, rf, update_text, progress_bar, progress_callback, result_callback, current_val_callback):
        
        #starting sol values
        sol_start = sol[0]
        bsol_start = bsol[0]
        rf_start = rf[0]

        #w = WorkerSignals()
        #self.signals = WorkerSignals() 
        
        # I initiallize the controllers within my for loop because otherwise it takes ages to set them to a particular value
        print '\n'
        print '                               LOADING CONTROLLERS                                  '
        print '==================================================================================='
        
        import VELA_CLARA_Magnet_Control as magx
        import VELA_CLARA_General_Monitor as monx
        import VELA_CLARA_Camera_Control as camx
        import VELA_CLARA_Charge_Control as chargex
        import VELA_CLARA_LLRF_Control as rfx

        
        # initialize magnet controller
        mag_init = magx.init()
        mag_control = mag_init.virtual_VELA_INJ_Magnet_Controller()
                
        # initialize cameras
        cam_init = camx.init()
        cam_control = cam_init.virtual_Camera_Controller()
        cam_init.setVerbose()
        
        # initialize the WCM
        #mon_init = monx.init()
        #charge = mon_init.connectPV('VM-CLA-S01-DIA-WCM-01:Q')
        
        # initialize the charge                         
        charge_init = chargex.init()
        charge_control = charge_init.virtual_Charge_Controller()
        
        # initialize the rf ccontroller
        rfinit = rfx.init()
        rf_control = rfinit.virtual_CLARA_LRRG_LLRF_Controller()
        
        print '==================================================================================='
        print '\n'
        
        # set rf to a cetrain MV/m value
        rf_amp = 50
        rf_control.setAmpMVM(rf_amp)
        
        self.check_if_ON(mag_control)
        
        measurement = 0
        
        #creating a table with all the values that we'll later append
#        with open('Documents\\VirtualAccelerator\\app3\\DC_data.csv', 'w') as f :
#            fieldnames = ['SOL', 'BSOL', 'CHARGE', 'HCOR01', 'VCOR01', 'RF amp']  
#            thewriter = csv.DictWriter(f, fieldnames = fieldnames)
#            thewriter.writeheader()
            
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
                    
                    #update_text(sol_val, bsol_val)
                    #progress_bar(percent)
                    progress_callback.emit(percent)
                    current_val_callback.emit(sol_val, bsol_val, rf_val)
                    
                    
                    result_sweep = function(mag_control, cam_control, charge_control, rf_control, sol_val,bsol_val, rf_val)
                    #print result_sweep
                    #w.progress.emit(percent)
                    result_callback.emit(result_sweep[0], result_sweep[1], result_sweep[2], result_sweep[3], result_sweep[4], result_sweep[5])
                    
                   #time.sleep(1)
                    #self.changedval.emit(sol_val, bsol_val, charge)

       
        return 'CONGRATS MARTA!'
        #print '\n'