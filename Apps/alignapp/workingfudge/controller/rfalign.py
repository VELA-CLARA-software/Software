import numpy as np
import os,sys

sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release')
os.environ["PATH"] = os.environ["PATH"]+";\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release\\root_v5.34.34\\bin\\"
import VELA_CLARA_Camera_Control as cam


class gunrfaligner(object):
    def __init__(self,argv):
        # startup view
        print "rfaligner constructor"
        self.xmin = 0 
        self.xmax = 0
        self.nx = 0 
        self.xrange = np.linspace(self.xmin,self.xmax,self.nx)
        self.ymin = 0 
        self.ymax = 0
        self.ny = 0
        self.yrange = np.linspace(self.ymin,self.ymax,self.ny)
        self.rfphs1 = 0
        self.rfphs2 = 0
        self.nrfp = 0
        self.solval = 0
        self.cam_init = cam.init()
        self.cam_init.setVerbose()
        self.cam_control = self.cam_init.physical_Camera_Controller()
        
        
    def setscangrid(self,xl,xh,numx,yl,yh,numy):
        self.xmin = xl    
        self.xmax = xh
        self.nx = numx
        self.ymin = yl    
        self.ymax = yh
        self.ny = numy
        self.xrange = np.linspace(self.xmin,self.xmax,self.nx)
        self.yrange = np.linspace(self.ymin,self.ymax,self.ny)
        
    def setrfphases(self,p1,p2):
        self.rfphs1 = p1
        self.rfphs2 = p2
        print "to set the rf phases"
        
    def setsolval(self,sv):
        self.solval = sv   
    
    def printtheparams(self):
        print "laser x range", self.xmin, self.xmax, "steps", self.nx
        print "laser y range", self.ymin, self.ymax, "steps", self.ny
        print "laser x range", self.xrange
        print "laser y range", self.yrange
        print "RF vals for RF steer", self.rfphs1, self.rfphs2
        print "Sol value during RF steer", self.solval
        
    def sethwp():   
        print "to set the hwp"
        
    def doscan(self):
        for x in self.xrange:
            for y in self.yrange:
                print 'VC position', x, y, '\n'
                self.cam_control.startAcquiring('S01-CAM-01')
                self.cam_control.collectAndSave('S01-CAM-01',1)
            """
#           caput('EBT-LAS-OPT-HWP-1:ROT:MABSS',135)
            caput('EBT-LAS-OPT-HWP-2:ROT:MABS',120)
            time.sleep(3)
            mylasmove.setposition(x,y,5,0.05)
            caput('EBT-LAS-OPT-HWP-2:ROT:MABS',80)  
            time.sleep(3)
        
            raw_input("Press Enter to continue...")
            # get the VC image
            cameras.setCamera('VC')
            time.sleep(1)
            cameras.startAcquiring()
            time.sleep(1)
            cameras.collectAndSave(1)
            time.sleep(1)
            cameras.stopAcquiring()
            time.sleep(1)        
            chargenow = monini.getValue(charge)
            bpms.reCalAttenuation('S01-BPM01',chargenow)
#        raw_input(" VC Press Enter to continue...")
            phi1 = -160 
            phi2 = -165

            #############################
            # Set RF phase to FIRST VALUE
            #############################
#        therf.setPhiDEG(phi1)
            magnets.setSI('LRG-SOL',110)
#       vsol = magnets.getRI('LRG-SOL')
#       vbsol = magnets.getRI('LRG-BSOL')
            time.sleep(10)
            xbuff =  bpms.getBPMXPVBuffer('S01-BPM01')
            ybuff =  bpms.getBPMYPVBuffer('S01-BPM01')
        #print ' xbuff ', xbuff, ' y buff ', ybuff 
        #raw_input("Press Enter to continue...")
            sx1 = np.std(xbuff)
            mx1 = np.mean(xbuff)
            sy1 = np.std(ybuff)
            my1 = np.mean(ybuff)
            # take screen data 
            cameras.setCamera('S01-CAM-01')
            time.sleep(1)
            cameras.startAcquiring()
            time.sleep(1)
            cameras.collectAndSave(1)
            time.sleep(1)
            cameras.stopAcquiring()
            time.sleep(1)
            camerasIA.setCamera('S01-CAM-01')
            selectedCameraIA = camerasIA.getSelectedIARef()
            camx1 = selectedCameraIA.IA.x
            camy1 = selectedCameraIA.IA.y
            print ' camx1 ', camx1
#           theshut.close("SHUT02")
#           time.sleep(1)
#           cameras.startAcquiring()
#           time.sleep(1)
#           cameras.collectAndSave(1)
#           time.sleep(1)
#           cameras.stopAcquiring()
#           time.sleep(1)       
#       #raw_input("Press Enter to continue...")
#        theshut.open("SHUT02")


            ##############################
            # Set RF phase to SECOND VALUE
            ##############################
    #        therf.setPhiDEG(phi2)
            magnets.setSI('LRG-SOL',-110)
            time.sleep(10)       
            vsol     = magnets.getRI('LRG-SOL')
            vbsol = magnets.getRI('LRG-BSOL')
            xbuff =  bpms.getBPMXPVBuffer('S01-BPM01')
            ybuff =  bpms.getBPMYPVBuffer('S01-BPM01')
    #        print ' xbuff2 ', xbuff, ' y buff2 ', ybuff 
    #       raw_input("Press Enter to continue...")
            sx2 = np.std(xbuff)
            mx2 = np.mean(xbuff)
            sy2 = np.std(ybuff)
            my2 = np.mean(ybuff)
            cameras.setCamera('S01-CAM-01')
            time.sleep(1)
            cameras.startAcquiring()
            time.sleep(1)
            cameras.collectAndSave(1)
            time.sleep(1)
            cameras.stopAcquiring()
            time.sleep(1)
            selectedCameraIA = camerasIA.getSelectedIARef()
            camx2 = selectedCameraIA.IA.x
            camy2 = selectedCameraIA.IA.y
            print ' camx2 ', camx2
            theshut.close("SHUT02")
            time.sleep(1)
            cameras.startAcquiring()
            time.sleep(1)
            cameras.collectAndSave(1)
            time.sleep(1)
            cameras.stopAcquiring()
            time.sleep(1)
            #raw_input("Press Enter to continue...")
            theshut.open("SHUT02")

            # process the net BPM movement 
            delx = mx2-mx1
            dely = my2-my1
            delr = ma.sqrt(delx**2 + dely**2)

            # process the net camera movement
            delcamx = camx2-camx1
            delcamy = camy2-camy1
            delcamr = ma.sqrt(delcamx**2 + delcamy**2)


            # write all the data to a file 
            f.write('RF phase '+str(therf.getPhiDEG())+' vcx '+str(x)+' vcy '+str(y)+ \
                ' charge '+str(chargenow)+ \
                ' x1  '+str(mx1)+' sx1 '+str(sx1)+' x2 '+str(mx2)+' sx2 '+str(sx2)+ \
                ' y1  '+str(my1)+' sy1 '+str(sy1)+' y2 '+str(my2)+' sy2 '+str(sy2)+ \
                ' delx '+str(delx)+' dely '+str(dely)+' delr '+str(delr)+ \
                ' camx1  '+str(camx1)+' camx2 '+str(camx2)+ \
                ' camy1  '+str(camy1)+' camx2 '+str(camy2)+ \
                ' delcamx '+str(delcamx)+' delcamy '+str(delcamy)+ \
                ' delcamr '+str(delcamr)+ \
                ' bsol '+str(vbsol)+' sol '+str(vsol)+ \
                '\n')
            f.flush()
    """