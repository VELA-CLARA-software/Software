import os, sys
import time
from epics import caget,caput

sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release')
os.environ["PATH"] = os.environ["PATH"]+";\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release\\root_v5.34.34\\bin\\"

import VELA_CLARA_Magnet_Control as mag
import VELA_CLARA_BPM_Control as bpm
import VELA_CLARA_LLRF_Control as llrf
import VELA_CLARA_PILaser_Control as pil
import VELA_CLARA_Camera_IA_Control as camIA

class Functions():
    def stepCurrent(self,ctrl,magnet,step):
        MAG = ctrl.getMagObjConstRef(magnet)
        setI = MAG.siWithPol + step
        print('Stepping current to: '+str(setI))
        ctrl.setSI(magnet,setI)
        #self.simulate.run()

    def getXBPM(self,ctrl,bpm,N):
        x=[]
        for i in range(N):
            #print ctrl.getXFromPV(bpm)
            x.append(ctrl.getXFromPV(bpm))
        return sum(x)/N

    def getYBPM(self,ctrl,bpm,N):
        x=[]
        for i in range(N):
            #print ctrl.getYFromPV(bpm)
            x.append(ctrl.getYFromPV(bpm))
        return sum(x)/N

    def getXScreen(self,ctrl,camera,N):
        x=[]
        for i in range(N):
            #print str(camera),', x = ', str(caget(camera+':ANA:X_RBV'))
            x.append(caget(camera+':ANA:X_RBV'))
        return sum(x)/N

    def getYScreen(self,ctrl,camera,N):
        x=[]
        for i in range(N):
            #print str(camera),', y = ', str(caget(camera+':ANA:Y_RBV'))
            x.append(caget(camera+':ANA:Y_RBV'))
        return sum(x)/N

    def alignX(self,hctrl,hcor, bctrl, bpm, off, tol, N=10):
        #DIP = dctrl.getMagObjConstRef(dipole)                                    #create a reference to the dipole
        print 'in align'
        COR = [hctrl.getMagObjConstRef(hcor)]                                        #create a reference to the corrector
        x1= -off+self.getXBPM(bctrl, bpm, N)                                            #get the x position on the BPM
        I1 = COR[0].siWithPol                                                        #x1,x2,I1,I2 are point to determine a straight linear relationship (I=mx+c)
        print 'I1', str(I1)
        x2=x1
        print 'beforehere1, x1:', str(x1), 'x2', str(x2), 'tol', str(tol)
        I2=0
        print 'here1'
        if (COR[0].riWithPol>0.0):                                                    #determine intial step
            print 'polarity>0'
            initialStep = -0.0001
        else:
            print 'polarity<0'
            initialStep = 0.0001
        print 'here2'
        self.stepCurrent(hctrl, hcor, initialStep)
        time.sleep(2)
        #self.simulate.run()                                                        #take inital step
        x2=-off+self.getXBPM(bctrl, bpm, N)
        I2=COR[0].siWithPol
        print 'here3'
        print 'before while, x1:', str(x1), 'x2', str(x2), 'tol', str(tol)
        while(abs(x2)>tol):                                                            # Algorithm loops until the current position is < the tolerance 'tol'
            print 'in while, x1:', str(x1), 'x2', str(x2), 'tol', str(tol)
            I_o = ((I1*x2-I2*x1)/(x2-x1) + I2)/2                                          # find the zero-crossing of straight line mde from positions at currents I1 and I2
            print('Predicted current intercept at '+str(I_o))
            hctrl.setSI(hcor,I_o)
            time.sleep(2)
            #QApplication.processEvents()
            #self.simulate.run()                                                    # set magnet to intercept current
            x1=x2                                                                #Get rid of first set of position and current
            I1=I2
            I2=I_o
            x2=-off+self.getXBPM(bctrl, bpm, N)
            print('Current at'+str(x2))
            time.sleep(2)
        print('Aligned beam using ' + hcor + ' and ' + bpm)

    def alignY(self,hctrl,hcor, bctrl, bpm, off, tol, N=10):
        #DIP = dctrl.getMagObjConstRef(dipole)                                    #create a reference to the dipole
        print 'in align'
        COR = [hctrl.getMagObjConstRef(hcor)]                                        #create a reference to the corrector
        x1= -off+self.getYBPM(bctrl, bpm, N)                                            #get the x position on the BPM
        I1 = COR[0].siWithPol                                                        #x1,x2,I1,I2 are point to determine a straight linear relationship (I=mx+c)
        print 'I1', str(I1)
        x2=x1
        print 'beforehere1, x1:', str(x1), 'x2', str(x2), 'tol', str(tol)
        I2=0
        print 'here1'
        if (COR[0].riWithPol>0.0):                                                    #determine intial step
            print 'polarity>0'
            initialStep = -0.0001
        else:
            print 'polarity<0'
            initialStep = 0.0001
        print 'here2'
        self.stepCurrent(hctrl, hcor, initialStep)
        time.sleep(2)
        #self.simulate.run()                                                        #take inital step
        x2=-off+self.getYBPM(bctrl, bpm, N)
        I2=COR[0].siWithPol
        print 'here3'
        print 'before while, x1:', str(x1), 'x2', str(x2), 'tol', str(tol)
        while(abs(x2)>tol):                                                            # Algorithm loops until the current position is < the tolerance 'tol'
            print 'in while, x1:', str(x1), 'x2', str(x2), 'tol', str(tol)
            I_o = ((I1*x2-I2*x1)/(x2-x1) + I2)/2
            #I_o = (I1*x2-I2*x1)/(x2-x1)                                            # find the zero-crossing of straight line mde from positions at currents I1 and I2
            print('Predicted current intercept at '+str(I_o))
            hctrl.setSI(hcor,I_o)
            time.sleep(2)
            #QApplication.processEvents()
            #self.simulate.run()                                                    # set magnet to intercept current
            x1=x2                                                                #Get rid of first set of position and current
            I1=I2
            I2=I_o
            x2=-off+self.getYBPM(bctrl, bpm, N)
            print('Current at'+str(x2))
            time.sleep(2)
        print('Aligned beam using ' + hcor + ' and ' + bpm)

magInit = mag.init()
bpmInit = bpm.init()
#pilInit = pil.init()
llrfInit = llrf.init()
camInit = camIA.init()
Cmagnets = magInit.physical_CB1_Magnet_Controller()
#self.laser = self.pilInit.physical_PILaser_Controller()
Cbpms = bpmInit.physical_CLARA_PH1_BPM_Controller()
Fns=Functions()
#Cmagnets.setSI('S01-HCOR1',0)
#Cmagnets.setSI('S01-VCOR1',0)
#time.sleep(1)
'''1. Align Beam at BPM-01''' #needs work to scan over set point etc.
Fns.alignX(Cmagnets,'S01-HCOR1',Cbpms,'S01-BPM01',1.0,0.05) # e.g. target x=1mm with 0.05mm tolerance
Fns.alignY(Cmagnets,'S01-VCOR1',Cbpms,'S01-BPM01',0.0,0.05)
'''2. Print to screen all the relevant numbers''' #needs work to print to file etc.
print Fns.getXBPM(Cbpms,'S02-BPM01',10)
print Fns.getYBPM(Cbpms,'S02-BPM01',10)
print Fns.getXBPM(Cbpms,'S02-BPM02',10)
print Fns.getYBPM(Cbpms,'S02-BPM02',10)
print Fns.getXScreen(camInit,'CLA-S02-DIA-CAM-03',10)
print Fns.getYScreen(camInit,'CLA-S02-DIA-CAM-03',10)
