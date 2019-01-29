from PyQt4.QtCore import (QCoreApplication, QObject, QRunnable, QThread,
                          QThreadPool, pyqtSignal)
from PyQt4.QtGui import QApplication
from epics import caget,caput
import scipy.constants as physics
import os,sys
import time
import math as m
import random as r
import numpy as np
from numpy.polynomial import polynomial as P
import copy
from VELA_CLARA_BPM_Control import BPM_STATUS

# class dummyOM():
#         def __init__(self):
#             print 'made a dummy OM'
#         def run():
#             print 'running NO simulation'


'''This Class contain function to use in a momentum procedure independant '''


class Functions(QObject):
    qctrl_sig = pyqtSignal(float)

    #def __init__(self, OM = dummyOM()):
    def __init__(self, model):
        super(Functions, self).__init__()
        self.model = model
        #QThread.__init__(self)
        #self.simulate = OM

    def stepCurrent(self,ctrl,magnet,step):
        MAG = ctrl.getMagObjConstRef(magnet)
        setI = MAG.siWithPol + step
        print('Stepping current to: '+str(setI))
        ctrl.setSI(magnet,setI)
        #self.simulate.run()

    def getBPMPosition(self, ctrl, bpm):
        return ctrl.getXFromPV(bpm)

    def getXBPM(self,ctrl,bpm,N):
        x=[]
        for i in range(N):
            #21/8/18 changed getXFromPV to getX
            a = ctrl.getX(bpm)
            print ctrl.getBPMStatus(bpm)
            if ctrl.getBPMStatus(bpm) == BPM_STATUS.GOOD:
                x.append(a)
                print a, 'shot ok'
            else:
                N-=1
                print a, 'shot excluded'
            time.sleep(0.1)
        if N > 1:
            return sum(x)/N

    def getYBPM(self,ctrl,bpm,N):
        x=[]
        for i in range(N):
            #21/8/18 changed getYFromPV to getY
            a = ctrl.getY(bpm)
            if ctrl.getBPMStatus(bpm) == BPM_STATUS.GOOD:
                x.append(a)
                print a
            else:
                N-=1
                print a, 'shot excluded'
            time.sleep(0.1)
        return sum(x)/N

    def getXScreen(self,ctrl,camera,N):
        # need to change to use controllers e.g.'x1 = self.model.camerasIA.getSelectedIARef().IA.x' etc.
        x=[]
        for i in range(N):
            print str(camera),', x = ', str(self.model.cam.getX(camera))
            #print str(camera),', x = ', str(caget(camera+':ANA:X_RBV'))
            x.append(self.model.cam.getX(camera))
            time.sleep(0.2)
        return sum(x)/N

    def getSigmaXScreen(self,ctrl,camera,N):
        sX=[]
        for i in range(N):
            pass
            #print str(camera),', sigma_x = ', str(caget(camera+':ANA:SigmaX_RBV'))
            #sX.append(caget(camera+':ANA:SigmaX_RBV'))
        return sum(sX)/N

    def getSigmaYScreen(self,ctrl,camera,N):
        sY=[]
        for i in range(N):
            pass
            #print str(camera),', sigma_y = ', str(caget(camera+':ANA:SigmaY_RBV'))
            #Y.append(caget(camera+':ANA:SigmaY_RBV'))
        return sum(sY)/N

    def isBeamOnScreen(self,screen):
        #this does nothing at the moment
        return True                                            #Add a controller to input

    def isBeamOnBPM(self,ctrl,bpm,N):
        #this does nothing at the moment
        #return True
        x=[]
        for i in range(N):
            a = ctrl.getX(bpm)
            if ctrl.getBPMStatus(bpm) != BPM_STATUS.BAD:
                x.append(a)
                print a, 'shot ok'
            else:
                #N-=1
                print a, 'shot excluded'
            print '# good shots', len(x)
            time.sleep(0.1)
        print 'here...', len(x), N
        if len(x) > N-1 and sum(x)/N > -5:
            return True
        else:
            return False


    def align(self,hctrl,hcor, bctrl, bpm, off, tol, initstep, N=10):
        #DIP = dctrl.getMagObjConstRef(dipole)                                    #create a reference to the dipole
        print 'in align'
        COR = [hctrl.getMagObjConstRef(hcor)]                                        #create a reference to the corrector
        x1= self.getXBPM(bctrl, bpm, N)                                            #get the x position on the BPM
        I1 = COR[0].siWithPol                                                        #x1,x2,I1,I2 are point to determine a straight linear relationship (I=mx+c)
        print 'I1', str(I1)
        x2=x1
        print 'beforehere1, x1:', str(x1), 'x2', str(x2), 'tol', str(tol)
        I2=0
        print 'here1'
        if (COR[0].riWithPol>0.0):                                                    #determine intial step
            print 'polarity>0'
            initialStep = -initstep
        else:
            print 'polarity<0'
            initialStep = initstep
        print 'here2'
        self.stepCurrent(hctrl, hcor, initialStep)
        time.sleep(1)
        #self.simulate.run()                                                        #take inital step
        x2=self.getXBPM(bctrl, bpm, N)
        I2=COR[0].siWithPol
        print 'here3'
        print 'before while, x1:', str(x1), 'x2', str(x2), 'tol', str(tol)
        count = 1
        while (abs(x2-off)>tol) and count<10 and abs(x2-x1)>(tol/10):                                                            # Algorithm loops until the current position is < the tolerance 'tol'
            count+=1
            print 'in while, I1:', str(I1), 'x1', str(x1), 'I2', str(I2), 'x2', str(x2), 'tol', str(tol), 'diff', str(x2-off), 'off', off
            time.sleep(0.1)
            I_o = (I1*(x2-off)-I2*(x1-off))/(x2-x1)
            if abs(I_o) > 5:
                print 'Current over 5 A'
                count = 10                                          # find the zero-crossing of straight line mde from positions at currents I1 and I2
            print('Predicted current intercept at '+str(I_o))
            #I_o = (I_o+I_2)/2
            I_o = (I_o+I2)/2
            hctrl.setSI(hcor,I_o)
            while (abs(hctrl.getSI(hcor) - I_o) > 0.005):
                print 'Waiting for corrector, set=', I_o, 'read=', hctrl.getSI(hcor), 'diff=', abs(hctrl.getSI(hcor) - I_o)
                time.sleep(0.01)
            #time.sleep(1)
            QApplication.processEvents()
            #self.simulate.run()                                                    # set magnet to intercept current
            x1=x2                                                                #Get rid of first set of position and current
            I1=I2
            I2=I_o#(I_o+I1)/2
            x2=self.getXBPM(bctrl, bpm, N)
            #print('Current at'+str(x2))
            time.sleep(0.1)
            print 'Current at ', I2
            time.sleep(0.1)
        if count<10:
            print('Aligned beam using ' + hcor + ' and ' + bpm)
        else:
            print 'Alignment failed'

    def alignOnScreen(self,hctrl,hcor, sctrl, screen, off, tol, initstep, N=10):
        #DIP = dctrl.getMagObjConstRef(dipole)                                    #create a reference to the dipole
        print 'in align screen'
        COR = [hctrl.getMagObjConstRef(hcor)]                                        #create a reference to the corrector
        #x1= self.getXBPM(sctrl, screen, N)                                            #get the x position on the screen
        x1 = self.getXScreen(sctrl, screen, N)
        time.sleep(1)
        I1 = COR[0].siWithPol                                                        #x1,x2,I1,I2 are point to determine a straight linear relationship (I=mx+c)
        print 'I1', str(I1)
        x2=x1
        print 'beforehere1, x1:', str(x1), 'x2', str(x2), 'tol', str(tol)
        I2=0
        print 'here1'
        if (COR[0].riWithPol>0.0):                                                    #determine intial step
            print 'polarity>0'
            initialStep = -initstep
        else:
            print 'polarity<0'
            initialStep = initstep
        print 'here2'
        self.stepCurrent(hctrl, hcor, initialStep)
        time.sleep(3)
        #self.simulate.run()                                                        #take inital step
        x2=self.getXScreen(sctrl, screen, N)
        time.sleep(1)
        I2=COR[0].siWithPol
        print 'here3'
        print 'before while, x1:', str(x1), 'x2', str(x2), 'tol', str(tol)
        count = 0
        while(abs(x2-off)>tol) and count<10:
            count+=1                                                            # Algorithm loops until the current position is < the tolerance 'tol'
            print 'in while, x1:', str(x1), 'x2', str(x2), 'tol', str(tol)
            I_o = (I1*(x2-off)-I2*(x1-off))/(x2-x1)                                           # find the zero-crossing of straight line mde from positions at currents I1 and I2
            I_o = (I_o+I2)/2
            print('Predicted current intercept at '+str(I_o))
            hctrl.setSI(hcor,I_o)
            time.sleep(3)
            QApplication.processEvents()
            #self.simulate.run()                                                    # set magnet to intercept current
            x1=x2                                                                #Get rid of first set of position and current
            I1=I2
            I2=I_o#(I_o+I1)/2
            #I2 = 0.1*I_o+0.9*I1
            x2=self.getXScreen(sctrl, screen, N)
            print('Current at'+str(x2))
            time.sleep(1)
        if count<10:
            print('Aligned beam using ' + hcor + ' and ' + screen)
        else:
            print 'Alignment failed'

    def bendBeamApprox(self,dctrl,dipole,bctrl,bpm,screen, IMin, IMax, tol, N=10):
        DIP = dctrl.getMagObjConstRef(dipole)                                    #create a reference to the dipole
        step = IMax/100                                                    #1% of predicted current
        setI = IMin#0.95*predictedI
        print ('50% of predicted current is: ',setI)
        dctrl.setSI(dipole,setI)
        time.sleep(2)

        while(self.isBeamOnScreen(screen)==False):                                #keep iterration of a 1% current step until beam is on screen
            self.stepCurrent(dctrl,dipole,step)
            time.sleep(0)
        while(self.isBeamOnBPM(bctrl, bpm, N)==False):                                #keep iterration of a 1% current step until beam is on screen
            self.stepCurrent(dctrl,dipole,step)
            QApplication.processEvents()
            time.sleep(0.1)
        # 22/8/18 Put extra steps in here to account for spurious initial BPM reading
        # while(self.isBeamOnBPM(bctrl, bpm, N)==True):                                #keep iterration of a 1% current step until beam is on screen
        #     self.stepCurrent(dctrl,dipole,step)
        #     QApplication.processEvents()
        #     time.sleep(0.1)
        # while(self.isBeamOnBPM(bctrl, bpm, N)==False):                                #keep iterration of a 1% current step until beam is on screen
        #     self.stepCurrent(dctrl,dipole,step)
        #     QApplication.processEvents()
        #     time.sleep(0.1)
        # x_old=0                                                                    #fake start x position

        x=self.getXBPM(bctrl, bpm, N)                                            #All BPM posiotn are fake and based of the previous position
        print 'x = ', str(x), 'tol = ', str(tol)                                                                        #it wont stay this way for the real procedure
        #step = dctrl.getSI(dipole)/100
        #time.sleep(100)
        #for n in range(1,1000):
        #    time.sleep(0.1)
        #    print 'is it updating?', str(n)
        #    QApplication.processEvents()
        while(x<-tol):                                                            #start loop that ramps up dipole current (conitines unitl x<tolerance)
            print 'x = ', str(x), 'tol = ', str(tol)
            print '!!!In bend beam!!!: ', str(caget('CLA-C2V-DIA-BPM-01:X'))
            self.stepCurrent(dctrl, dipole, step)
            time.sleep(1)
            QApplication.processEvents()
            x_old=x                                                                # keep a note of teh last beam position to roughly predict the effect of the next step
            x=self.getXBPM(bctrl, bpm, N)
            print(x)
            time.sleep(0.1)
            if abs(x)<abs(x_old-x):                                                        #if the step size look like it is will over bend the beam, half it.
                step = step*0.1
            if dctrl.getSI(dipole) > IMax:
                break
        print('Centered beam in Spectrometer line using ' + dipole + ' and ' + bpm)
        return dctrl.getSI(dipole)


    def bendBeam(self,dctrl,dipole,bctrl,bpm,screen, IMin, IMax, tol, N=10):
        DIP = dctrl.getMagObjConstRef(dipole)                                    #create a reference to the dipole
        step = (IMin+IMax)/200                                                    #1% of predicted current
        setI = IMin#0.95*predictedI
        #print ('95% of predicted current is: ',setI)
        dctrl.setSI(dipole,setI)
        time.sleep(2)
        print self.getXBPM(bctrl, bpm, N)
        getsi = dctrl.getSI(dipole)
        print getsi
        getri = dctrl.getRI(dipole)
        print getri                                                 #set dipole current to 90% of predicted
        #self.simulate.run()
        print 'Did it set correctly?'
        print 'getsi/setI = ', str(getsi/setI)
        print 'getri/setI = ', str(getsi/setI)
        time.sleep(0.1)
        # check beam on screen does nothing atm
        while(self.isBeamOnScreen(screen)==False):                                #keep iterration of a 1% current step until beam is on screen
            self.stepCurrent(magCtrl,dipole,step)
            time.sleep(0)
        x_old=0                                                                    #fake start x position
        x=self.getXBPM(bctrl, bpm, N)                                            #All BPM posiotn are fake and based of the previous position
        print 'x = ', str(x), 'tol = ', str(tol)                                                                        #it wont stay this way for the real procedure
        #time.sleep(100)
        #for n in range(1,1000):
        #    time.sleep(0.1)
        #    print 'is it updating?', str(n)
        #    QApplication.processEvents()
        while(x<-tol):                                                            #start loop that ramps up dipole current (conitines unitl x<tolerance)
            print 'x = ', str(x), 'tol = ', str(tol)
            print '!!!In bend beam!!!: ', str(caget('CLA-C2V-DIA-BPM-01:X'))
            self.stepCurrent(dctrl, dipole, step)
            time.sleep(1)
            QApplication.processEvents()
            x_old=x                                                                # keep a note of teh last beam position to roughly predict the effect of the next step
            x=self.getXBPM(bctrl, bpm, N)
            print(x)
            time.sleep(0.1)
            if abs(x)<abs(x_old-x):                                                        #if the step size look like it is will over bend the beam, half it.
                step = step*0.1
            if dctrl.getSI(dipole) > IMax:
                break
        print('Centered beam in Spectrometer line using ' + dipole + ' and ' + bpm)
        return dctrl.getSI(dipole)                                        #return the current at which beam has been centered

    def bendBeamScreen(self,dctrl,dipole,screen, IMin, IMax, tol, N=10):
        DIP = dctrl.getMagObjConstRef(dipole)                                    #create a reference to the dipole
        step = (IMin+IMax)/100                                                    #1% of predicted current
        setI = IMin#0.95*predictedI
        print ('95% of predicted current is: ',setI)
        dctrl.setSI(dipole,setI)
        time.sleep(2)
        print self.getXBPM(bctrl, bpm, N)
        getsi = dctrl.getSI(dipole)
        print getsi
        getri = dctrl.getRI(dipole)
        print getri                                                 #set dipole current to 90% of predicted
        #self.simulate.run()
        print 'Did it set correctly?'
        print 'getsi/setI = ', str(getsi/setI)
        print 'getri/setI = ', str(getsi/setI)
        time.sleep(0.1)
        # check beam on screen does nothing atm
        while(self.isBeamOnScreen(screen)==False):                                #keep iterration of a 1% current step until beam is on screen
            self.stepCurrent(magCtrl,dipole,step)
            time.sleep(0)
        x_old=0                                                                    #fake start x position
        x=self.getXBPM(bctrl, bpm, N)                                            #All BPM posiotn are fake and based of the previous position
        print 'x = ', str(x), 'tol = ', str(tol)                                                                        #it wont stay this way for the real procedure
        #time.sleep(100)
        #for n in range(1,1000):
        #    time.sleep(0.1)
        #    print 'is it updating?', str(n)
        #    QApplication.processEvents()
        while(x<-tol):                                                            #start loop that ramps up dipole current (conitines unitl x<tolerance)
            print 'x = ', str(x), 'tol = ', str(tol)
            print '!!!In bend beam!!!: ', str(caget('CLA-C2V-DIA-BPM-01:X'))
            self.stepCurrent(dctrl, dipole, step)
            time.sleep(1)
            QApplication.processEvents()
            x_old=x                                                                # keep a note of teh last beam position to roughly predict the effect of the next step
            x=self.getXBPM(bctrl, bpm, N)
            print(x)
            time.sleep(0.1)
            if abs(x)<abs(x_old-x):                                                        #if the step size look like it is will over bend the beam, half it.
                step = step*0.1
            if dctrl.getSI(dipole) > IMax:
                break
        print('Centered beam in Spectrometer line using ' + dipole + ' and ' + bpm)
        return dctrl.getSI(dipole)                                        #return the current at which beam has been centered



    """NEED TO TEST MINIMIZE BETA ON REAL MACHINE"""
    def minimizeBeta2D(self,qctrl,quad1,quad2,quad1max,quad2max,steps,sctrl,screen,init_step,N=10):
        QUAD1 = qctrl.getMagObjConstRef(quad1)
        QUAD2 = qctrl.getMagObjConstRef(quad2)
        xrange = np.linspace(-quad1max,quad1max,steps)
        yrange = np.linspace(-quad2max,quad2max,steps)
        for xnum, x in enumerate(xrange, start=0):
            for ynum, y in enumerate(yrange, start=0):
                print xnum, ynum, x, y
                qctrl.setSI(quad1, x)
                qctrl.setSI(quad2, y)
                time.sleep(2)


    def minimizeBeta(self,qctrl,quad,sctrl,screen,init_step,N=10):
        QUAD = qctrl.getMagObjConstRef(quad)
        minimisingInX = False
        if(init_step>0):
            minimisingInX=True

        # '''Quick scan to find rough minimum'''
        # if(minimisingInX):
        #     print 'Rough scan in X'
        #     sX_scan = []
        #     xrange = np.arange(-50,50,10)
        #     for x in xrange:
        #         qctrl.setSI(quad, x)
        #         self.simulate.run()
        #         time.sleep(1)
        #         print(qctrl.getSI(quad))
        #         sX_scan.append(self.getSigmaXScreen(sctrl,screen,N))
        #     print sX_scan
        #     sX_approxmin = xrange[np.argmin(sX_scan)]
        #     print sX_approxmin
        # else:
        #     print 'Rough scan in Y'
        #     sY_scan = []
        #     yrange = np.arange(-50,50,10)
        #     for y in yrange:
        #         qctrl.setSI(quad, y)
        #         self.simulate.run()
        #         time.sleep(1)
        #         print(qctrl.getSI(quad))
        #         sY_scan.append(self.getSigmaYScreen(sctrl,screen,N))
        #     print sY_scan
        #     sY_approxmin = yrange[np.argmin(sY_scan)]
        #     print sY_approxmin

        if(minimisingInX):
            qctrl.setSI(quad, 0.3)    #depends if +tine or -tive                #set a fake start current
            print 'Minimising in x'
            time.sleep(1)
        else:
            qctrl.setSI(quad, -0.3)
            print 'Minimising in y'
            time.sleep(1)
        #self.simulate.run()
        step  = init_step
        I3_1 = 0                                                                #I3_1 is the first value that is 3 time the size of the inita current
        I3_2 = 0
        sX_initial = 0
        if(minimisingInX):
            sX_initial =self.getSigmaXScreen(sctrl,screen,N)
        else:
            sX_initial =self.getSigmaYScreen(sctrl,screen,N)
        I_initial = QUAD.siWithPol
        sX_1 = sX_initial
        I_1 = QUAD.siWithPol
        sX_2 = sX_initial
        I_2 = QUAD.siWithPol

        while (sX_2<3*sX_initial):                                                #step 'left', i.e reduce current
            'Entering Loc1'
            sX_1 = sX_2
            I_1 = I_2
            self.stepCurrent(qctrl, quad, step)
            time.sleep(1)
            I_2 = QUAD.siWithPol
            if(minimisingInX):
                print 'Minimising in x'
                sX_2 =self.getSigmaXScreen(sctrl,screen,N)
            else:
                print 'Minimising in y'
                sX_2 =self.getSigmaYScreen(sctrl,screen,N)
            print 'Loc1Current: ', str(I_2)
            print('Loc1Sigma: '+str(sX_2)+' Initial sigma: '+str(sX_initial))                            #At this point we have gone higher than 3*initial_size. Assume straight line and find prediction for 3*
            time.sleep(0.1)
        I3_1 = (3*sX_initial*(I_2 - I_1) + (sX_2*I_1 - sX_1*I_2))/(sX_2 - sX_1)

        self.stepCurrent(qctrl, quad, 2*(I_initial - I3_1))                        #predict where the the other location of the size being 3*the initial_size and go there
        I_1 = QUAD.siWithPol
        if(minimisingInX):
            sX_1 =self.getSigmaXScreen(sctrl,screen,N)
        else:
            sX_1 =self.getSigmaYScreen(sctrl,screen,N)

        print 'Sigma: ', sX_1
        sX_2 = sX_1
        if (sX_1<3*sX_initial):
            while (sX_2<3*sX_initial):
                sX_1 = sX_2
                I_1 = I_2
                self.stepCurrent(qctrl, quad, -step)
                time.sleep(1)
                I_2 = QUAD.siWithPol
                if(minimisingInX):
                    sX_2 =self.getSigmaXScreen(sctrl,screen,N)
                else:
                    sX_2 =self.getSigmaYScreen(sctrl,screen,N)

                print 'Loc2Current: ', str(I_2)
                print('Loc2Sigma: '+str(sX_2)+' Initial sigma: '+str(sX_initial))
                time.sleep(0.1)
        else:
            while (sX_2>3*sX_initial):
                sX_1 = sX_2###MAKE ZERO!!!
                I_1 = I_2
                self.stepCurrent(qctrl, quad, step)
                time.sleep(1)
                I_2 = QUAD.siWithPol
                if(minimisingInX):
                    sX_2 =self.getSigmaXScreen(sctrl,screen,N)
                else:
                    sX_2 =self.getSigmaYScreen(sctrl,screen,N)

                print 'Loc3Current: ', str(I_2)
                print('Loc3Sigma: '+str(sX_2)+' Initial sigma: '+str(sX_initial))
                time.sleep(0.1)

        I3_2 = (3*sX_initial*(I_2 - I_1) + (sX_2*I_1 - sX_1*I_2))/(sX_2 - sX_1)

        qctrl.setSI(quad,0.5*(I3_1 + I3_2))            #assume minimum is half way in between these places so set magnet current to that
        #self.simulate.run()
        print('Minimised Beta with '+quad+' on '+screen)

    def fixDispersion(self,qctrl,quad,sctrl,screen,step_size,N=1):
        #THis needs work!!!!self.finished.emit()
        qctrl.setSI(quad, 0.0)                                                    #set a fake start current
        #self.simulate.run()                                                        #assumes beam is on screen
        sX = self.getSigmaXScreen(sctrl, screen, N)
        sX_old = sX
        targetBeamSigma = 0.0005
        while (abs(sX-targetBeamSigma)>0.00001):
            self.stepCurrent(qctrl, quad, step_size)
            sX_old = sX
            sX = self.getSigmaXScreen(sctrl, screen, N)
            print('Sigma of Beam: '+str(sX))
            time.sleep(0.1)

            if (abs(sX-targetBeamSigma)>abs(sX_old-targetBeamSigma)):
                step_size=-step_size
                step_size = 0.5*step_size

            if (abs(sX-targetBeamSigma)<abs(sX-sX_old)):
                step_size = 0.5*step_size

    def findDispersion(self,dctrl,dipole,sctrl,screen,centering_I,points,leveloff_threshold,N=10):
        currents = np.zeros(points)
        positions = np.zeros(points)
        dCurrents=[]
        dPositions=[]
        fCurrents=[]
        fPositions=[]
        DIP = dctrl.getMagObjConstRef(dipole)
        #position of beam
        sX=0
        dctrl.setSI(dipole,centering_I)                                    #set dipole current to 90% of predicted
        #self.simulate.run()
        time.sleep(1)

        #set dipole current to 95% of centering current
        setI = 0.99*centering_I
        print setI
        for a in reversed(np.linspace(setI,centering_I, 10)): #slowly set offset to allow image collector to keep up
            print 'Moving to starting position (0.98*I_0)'
            #dctrl.setSI(dipole,setI)
            dctrl.setSI(dipole,a)
            #self.simulate.run()
            time.sleep(2)
        #I = totalIntensity(screen)
        #I_old = I/2
        #while(I/I_old-1>leveloff_threshold):
        #self.stepCurrent(dipole,step)
        currents[0] = DIP.siWithPol
        #positions[0] = self.getXScreen(sctrl,screen,N)
        positions[0] = self.model.cam.getX('C2V-CAM-01')
        print centering_I
        print currents[0]
        print points-1
        I_diff = 2*(centering_I-currents[0])/(points-1)

        for i in range(1,points):
            print 'i', str(i)
            print 'I_diff', str(I_diff)
            self.stepCurrent(dctrl, dipole, I_diff)
            time.sleep(3)
            currents[i] = DIP.siWithPol
            #positions[i] = self.getXScreen(sctrl,screen,N)
            positions[i] = self.model.cam.getX('C2V-CAM-01')
            dCurrents=currents
            dPositions= positions
            if i==(points-1)/2:
                #sX = self.getSigmaXScreen(sctrl,screen,N)
                sX = self.model.cam.getSigX('C2V-CAM-01')

        c, stats = P.polyfit(currents,positions,1,full=True)
        fCurrents=[0.90*centering_I,1.1*centering_I]
        fPositions=[(c[1]*0.90*centering_I)+c[0],(c[1]*1.10*centering_I)+c[0]]
        print(c)
        print('Determined Dispersion with '+dipole+' and '+screen)
        print('dispersion'+str(c[1])+' and  beamsigma is'+str(sX))
        print 'dCurrents', str(dCurrents)
        print 'fCurrents', str(fCurrents)
        return c[1],sX,dCurrents,dPositions,fCurrents,fPositions

    '''The following has been altered to work with the online model (400.0033)'''
    def calcMomSpread(self,dctrl,dipole, Is, I):
        D = dctrl.getMagObjConstRef(dipole)
        #mom1= (400.0033/D.magneticLength)*(np.polyval(D.fieldIntegralCoefficients, abs(I-Is))*physics.c*180)/(45*physics.pi*1000000000)
        #mom2= (400.0033/D.magneticLength)*(np.polyval(D.fieldIntegralCoefficients, abs(Is+I))*physics.c*180)/(45*physics.pi*1000000000)
        mom1= (np.polyval(D.fieldIntegralCoefficients, abs(I-Is))*physics.c*180)/(45*physics.pi*1000000000)
        mom2= (np.polyval(D.fieldIntegralCoefficients, abs(Is+I))*physics.c*180)/(45*physics.pi*1000000000)
        print(mom1-mom2)/2
        return abs(mom1-mom2)/2

    def calcMom(self, dctrl,dipole, I):
        D = dctrl.getMagObjConstRef(dipole)
        #return (400.0033/D.magneticLength)*(np.polyval(D.fieldIntegralCoefficients, abs(I))*physics.c*180)/(45*physics.pi*1000000000)
        return (np.polyval(D.fieldIntegralCoefficients, abs(I))*physics.c*180)/(45*physics.pi*1000000000)

    def mom2I(self,dctrl,dipole,mom):
        D = dctrl.getMagObjConstRef(dipole)
        coeffs = list(D.fieldIntegralCoefficients)
        #print coeffs
        #print(1000000000*(mom*physics.pi*45)/(physics.c*180))
        #coeffs[-1] -= (D.magneticLength/400.0033)*(1000000000*(mom*physics.pi*45)/(physics.c*180))
        coeffs[-1] -= (1000000000*(mom*physics.pi*45)/(physics.c*180))
        roots = np.roots(coeffs)
        current = roots[-1].real
        return current

    def get_qctrl_sig(self):
        print 'in get_qctrl_sig'

    def startBPMTimer(self, crester):
        self.qctrl_sig.connect(crester.update_qctrl_sig)
        self.timer = QTimer()
        self.timer.timeout.connect(lambda : self.getBPMPosition(self.parameters['bpm']))
        self.timer.start(100)

    def using_move_to_thread(self,qctrl,quad,sctrl,screen,init_step,N=1):
        #self.qctrl = qctrl
        #self.qctrl = copy.deepcopy(qctrl)
        print('Function using_move_to_thread')
        print qctrl
        print quad
        print 'did it work??'
        self.qctrl_sig.emit(0.1)
        print 'in between'
        self.get_qctrl_sig()
        self.cresterObject = self.crestingMethod(self, minimisebetaclass, qctrl,quad,sctrl,screen,init_step,self.simulate)
        #self.cresterObject = self.crestingMethod(self, self.startWCMTimer, self.gunPhaser, minimisebetaclass)

    class crestingMethod(QObject):
		def __init__(self, parent, minimisebetaclass, *args, **kwargs):
			#parent.disableButtons()
			self.crester = minimisebetaclass(parent, *args, **kwargs)
			#self.crester.setPhase.connect(parent.setPhase)
			#timer(self.crester)
			self.thread = QThread()  # no parent!
			self.crester.moveToThread(self.thread)
			self.thread.started.connect(self.crester.minimizeBeta2)
			#self.crester.finished.connect(parent.printFinished)
			#self.crester.finished.connect(parent.timer.stop)
			#self.crester.finished.connect(parent.enableButtons)
			#self.crester.finishedSuccesfully.connect(lambda : phaser(offset=False))
			self.crester.finished.connect(self.thread.quit)
			self.thread.start()

class crestingObject(QObject):
	finished = pyqtSignal()
	finishedSuccesfully = pyqtSignal()
	setPhase = pyqtSignal(str, float)
	data = []
	_isRunning = True
	_finish = False

	def stop(self):
		print 'stopping worker!'
		self._isRunning = False

	def finish(self):
		print 'finishing worker!'
		self._finish = True

class minimisebetaclass(crestingObject):
    def __init__(self, parent,qctrl,quad,sctrl,screen,init_step,simulate,N=1):
        super(minimisebetaclass, self).__init__()
        self.parent = parent
        #self.resetDataArray()
        #self.offset = 0
        #self.qctrl = copy.deepcopy(qctrl)
        print('minimisebetaclass')
        #print self.qctrl
        #print 'did it work2??'
        self.qctrl = qctrl
        self.quad = quad
        self.sctrl = sctrl
        self.screen = screen
        self.init_step = init_step
        self.simulate = simulate
        self.N = N
        print self.qctrl
        print self.quad
        print 'did it work2??'

    def minimizeBeta3(self):
        print('minimizeBeta3fn')
        print self.qctrl
        print self.quad
        print 'did it work4??'

    def minimizeBeta2(self):
        #self.qctrl = qctrl
        print('minimizeBeta2fn')
        print self.qctrl
        print self.quad
        print 'did it work3??'
        QUAD = self.qctrl.getMagObjConstRef(self.quad)
        minimisingInX = False
        if(self.init_step>0):
            minimisingInX=True

        '''Quick scan to find rough minimum'''
        if(minimisingInX):
            print 'Rough scan in X'
            sX_scan = []
            xrange = np.arange(-50,50,5)
            for x in xrange:
                self.qctrl.setSI(self.quad, x)
                self.simulate.run()
                time.sleep(0.1)
                print(self.qctrl.getSI(self.quad))
                sX_scan.append(Functions.getSigmaXScreen(self.sctrl,self.screen,self.N))
            print sX_scan
            sX_approxmin = xrange[np.argmin(sX_scan)]
            print sX_approxmin

            print 'Fine scan in X'
            sX_scan2 = []
            xrange2 = np.arange(sX_approxmin-10,sX_approxmin+10,1)
            for x in xrange2:
                self.qctrl.setSI(self.quad, x)
                self.simulate.run()
                time.sleep(0.1)
                print(self.qctrl.getSI(self.quad))
                sX_scan2.append(Functions.getSigmaXScreen(self.sctrl,self.screen,self.N))
            print sX_scan2
            sX_min = xrange2[np.argmin(sX_scan2)]
            print sX_min
            self.qctrl.setSI(self.quad,sX_min)
        else:
            print 'Rough scan in Y'
            sY_scan = []
            yrange = np.arange(-50,50,10)
            for y in yrange:
                self.qctrl.setSI(self.quad, y)
                self.simulate.run()
                time.sleep(0.1)
                print(self.qctrl.getSI(self.quad))
                sY_scan.append(Functions.getSigmaYScreen(self.sctrl,self.screen,self.N))
            print sY_scan
            sY_approxmin = yrange[np.argmin(sY_scan)]
            print sY_approxmin

            print 'Fine scan in Y'
            sY_scan2 = []
            yrange2 = np.arange(sY_approxmin-10,sY_approxmin+10,2)
            for y in yrange2:
                self.qctrl.setSI(self.quad, y)
                self.simulate.run()
                time.sleep(0.1)
                print(self.qctrl.getSI(self.quad))
                sY_scan2.append(Functions.getSigmaYScreen(self.sctrl,self.screen,self.N))
            print sY_scan2
            sY_min = yrange2[np.argmin(sY_scan2)]
            print sY_min
            self.qctrl.setSI(self.quad,sY_min)

        self.simulate.run()
        print('Minimised Beta with '+self.quad+' on '+self.screen)
        #self.finished.emit()
