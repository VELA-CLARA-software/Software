from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
import sys,os
#import view
import numpy as np

#sys.path.append("\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\stage\\")
#sys.path.append("\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\stage\\Python3_x64\\")
sys.path.append("\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\stage\\Python3_x64\\")


#
#for item in sys.path:
#	print item

#0# import VELA_CLARA_PILaser_Control as pil
import time

#0# pil_init = pil.init()
#pil_init.setVerbose()
#0# pil_control = pil_init.physical_PILaser_Controller()

#import lasmover as lm
import math as ma
import numpy as np
import time
timestr = time.strftime("%Y%m%d-%H%M%S")

import VELA_CLARA_LLRF_Control as rf
rfinit = rf.init()
therf = rfinit.physical_CLARA_LRRG_LLRF_Controller()

import VELA_CLARA_BPM_Control as bpm 
bpminit = bpm.init()
bpminit.setVerbose()
bpms = bpminit.physical_CLARA_PH1_BPM_Controller()

import VELA_CLARA_General_Monitor as mon
monini = mon.init()

charge = monini.connectPV('CLA-S01-DIA-WCM-01:Q')
lasE = monini.connectPV('CLA-LAS-DIA-EM-01:E')
vcsump = monini.connectPV('CLA-VCA-DIA-CAM-01:ANA:Intensity_RBV')

# NEW section to get llrf stuff. Tried copying from Duncan charge app. 
therf2 = rfinit.getLLRFController(rf.MACHINE_MODE.PHYSICAL,rf.LLRF_TYPE.CLARA_LRRG)
##therf2.getCavFwdPwr()
##therf2.getCavRevPwr()
##print("hello!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",therf2.getCavFwdPwr())


#exit()

class chargescanner(QtCore.QObject):

    changedval = pyqtSignal(float, float, float, float)
    changedlogtxt = pyqtSignal(str)
    
    # lo, hi and the min and max values of the area on the VC to scan
    # values are mm from bottom left of the VC imagecollector
    # nx,y is number of points to stop and measure charge at in x,y
    xlo = 3
    xhi = 7
    ylo = 3
    yhi = 7
    nx = 3
    ny = 3
    xrange = np.linspace(xlo,xhi,nx)
    yrange = np.linspace(ylo,yhi,ny)

    def setxrange(self,dumxlo,dumxhi,dumnx):
        self.xrange = np.linspace(dumxlo,dumxhi,dumnx)  
	
    def setyrange(self,dumylo,dumyhi,dumyx):
        self.yrange = np.linspace(dumylo,dumyhi,dumny)
	
    def doscan(self,xxlo,xxhi,xxn,yylo,yyhi,yyn):
		
        self.xrange = np.linspace(xxlo,xxhi,xxn)
        self.yrange = np.linspace(yylo,yyhi,yyn)
		
        print('IN DOSCAN',self.xrange)
        print('IN DOSCAN',self.yrange)
        print(therf.getPhiDEG())

        print('***********************************************************')
        print('!!!!!!!!!!!!!!!!!!!!!PLEASE READ!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print('***********************************************************\n')
        print('This is a script to scan the laser over the cathode (via VC)')
        print('and measure the charge on the WCM \n')
        print('Please have imagecollector open on the VC and check that the')
        print('mask feedback is switched on, and that the mask follows the VC laser spot')
        print('throughout the scan.\n')

        print('the x locations where charge will be measured are', self.xrange, ' mm')
        print('the y locations where charge will be measured are', self.yrange, ' mm')
        print('the total number of scan points is', self.nx*self.ny)

        print('the wcm reading at each point will be recorded in the file qscan.txt')
        print('which is created whereever you run this script from')


# write results to work folder. 
        timestr = time.strftime("%H%M%S")
        dir = '\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Work\\'+time.strftime("%Y\\%m\\%d")+'\\'
        try:
            os.makedirs(dir)
        except OSError:
            if not os.path.isdir(dir):
                self.logger.emit('Error creating directory - saving to local directory')
                dir = '.'

        filename = dir+'qscan'+str(timestr)+'.txt'
        f = open(filename,'a')
		
#        f = open('qscan'+str(timestr)+'.txt','a')
#exit()
#0#        pil_control.setMaskFeedBackOn_VC()
        #xrange = [5.5]
        #yrange = [4.5]
		

		# # next section of code to access data from PI Contoller (code c/o Duncan)
        # # from this we can get individual peices of hardware, let's store them in a dictionary called hardware
        # hardware = {}
        # # VC camera image object object
        # vc_image = "vc_image"
        # hardware[vc_image] = pil_control.getImageObj()
        # # to access the vc_image object just call: hardware[vc_image]
        # # image data / anmalaysis 
        # vc_image_data= "vc_image_data"
        # hardware[vc_image_data] = pil_control.getVCDataObjConstRef()
        # # the VC camera
        # vc_cam= "vc_cam"
        # hardware[vc_cam] = pil_control.getCameraObj()
        # # laser mirror object 
        # mirror = "mirror"
        # # the PI laser object (from here you can get Q, laser energy ...)
        # pil = "pil"
        # hardware[pil] = pil_control.getPILObjConstRef()
        # #number of shots:
        # num_shots_to_average = 12
        # pil_control.setAllRSBufferSize(num_shots_to_average)
        # # Check the buffer size for the Q
        # print("getRSBufferSize = ",hardware[pil].max_buffer_count)

        # # some constants, (probably should save once for each run )
        # x_pix_scale_factor = hardware[vc_image].x_pix_scale_factor
        # y_pix_scale_factor = hardware[vc_image].y_pix_scale_factor
        # x_pix_to_mm = hardware[vc_image].x_pix_to_mm
        # y_pix_to_mm = hardware[vc_image].y_pix_to_mm
        # num_pix_x = hardware[vc_image].num_pix_x
        # num_pix_y =  hardware[vc_image].num_pix_y
        # # ++ others?? 


        ix = 0
        chargebest = 0
        for x in self.xrange:
            if ix % 2 == 0:
                dumyrange = self.yrange
                print('going up', dumyrange) 
            else:
                dumyrange = self.yrange[::-1] 
                print('going up', dumyrange) 
            ix = ix + 1            
            for y in dumyrange:
                print(x, y, '\n')
               
#l                a = pil_control.setVCPos(x,y)
#l                # monitor  this paramter to know when ity has finished 
#l                set_pos_succes = False
#l#        exit()
#l		
#l                while 1:
#l                    set_pos_state = pil_control.getSetVCPosState()
#l                    print 'success status', set_pos_state
#l                    if set_pos_state == pil.VC_SET_POS_STATE.SUCCESS:
#l                        set_pos_succes = True
#l                        break
#l                    else:
#l                        print set_pos_state
#l                    time.sleep(1)
#l                print("Set Position Finished",pil_control.getSetVCPosState())
#        exit()
#        mylasmove.setposition(x,y,5,0.1)
#                raw_input("Press Enter to continue...")0

# # get the qscan quantities at this point (c.o Duncan for the code)
                # # set next-position 
                # # when at next position 
                # print("At next_positoin, getting some data")	
                # pil_control.clearRunningValues()
                # # wait for buffer to fill, we will just check against the Q buffer
                # while hardware[pil].Q_full == False: # suggest for pil_control, we could do with a isRFBufferNOTFull function(!)
                    # print("Waiting for running stat buffer to fill, ", hardware[pil].Q_n)
                    # time.sleep(0.5)
                # print("Buffer Is Full, ",hardware[pil].Q_n," getting data")
                # # mean and (standard deviation) sd for Q
                # Q_mean = hardware[pil].Q_mean
                # Q_sd = hardware[pil].Q_sd
                # # mean and sd for energy
                # energy_mean = hardware[pil].energy_mean
                # energy_sd = hardware[pil].energy_sd
                # # laser x position mean and sd 
                # x_pix_mean = hardware[vc_image_data].x_pix_mean	
                # x_pix_sd = hardware[vc_image_data].x_pix_sd	
                # # laser y position mean and sd 
                # y_pix_mean = hardware[vc_image_data].y_pix_mean	
                # y_pix_sd = hardware[vc_image_data].y_pix_sd	
                # # laser x width mean and sd 
                # sig_x_pix_mean = hardware[vc_image_data].sig_x_pix_mean	
                # sig_x_pix_sd = hardware[vc_image_data].sig_x_pix_sd	
                # # y position mean and sd 
                # sig_y_pix_mean = hardware[vc_image_data].sig_y_pix_mean	
                # sig_y_pix_sd = hardware[vc_image_data].sig_y_pix_sd	




                chargenow = 1.1
#                chargenow = monini.getValue(charge)
                lasEnow = 1.1 
#                lasEnow = monini.getValue(lasE)
                vcsumpnow = monini.getValue(vcsump)
#                f.write('str(x)+' '+str(x_pix_mean)+' '+str(x_pix_sd)+' '+str(y)+' '+str(y_pix_mean)+' '+str(y_pix_sd)+' '+str(Q_mean)+' '+str(Q_sd)+' ' '+'str(Q_mean)+' '+str(Q_sd)')
#                f.write('RF phase '+str(therf.getPhiDEG())+' vcx '+str(x)+' vcy '+str(y)+' charge '+str(chargenow)+' laserE '+str(lasEnow)+' VCintens '+str(vcsumpnow)+'\n')
                f.flush()
                self.changedval.emit(x,y,chargenow,lasEnow)
                iterstring = "hello string signal"
                print(iterstring)
                self.changedlogtxt.emit(iterstring)
                
                print("charge now", chargenow, " best charge ", chargebest)
                if chargenow > chargebest:
                    chargebest = chargenow
                    print("got a higher charge")     
                
                
        print('finished the scan, the higher charge was', chargebest)         
        f.close()
