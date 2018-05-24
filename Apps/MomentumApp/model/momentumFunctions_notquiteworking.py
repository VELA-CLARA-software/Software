from PyQt4.QtCore import (QCoreApplication, QObject, QRunnable, QThread,
                          QThreadPool, pyqtSignal)
from epics import caget,caput
import scipy.constants as physics
import os,sys
import time
import math as m
import random as r
import numpy as np
from numpy.polynomial import polynomial as P



class dummyOM():
        def __init__(self):
            print 'made a dummy OM'
        def run():
            print 'running NO simulation'


'''This Class contain function to use in a momentum procedure independant '''


class Functions():
    def __init__(self, OM = dummyOM() ):
        #QThread.__init__(self)
        self.simulate = OM

    def stepCurrent(self,ctrl,magnet,step):
        MAG = ctrl.getMagObjConstRef(magnet)
        setI = MAG.siWithPol + step
        print('Stepping current to: '+str(setI))
        ctrl.setSI(magnet,setI)
        self.simulate.run()

    def getXBPM(self,ctrl,bpm,N):
        x=[]
        for i in range(N):
            print bpm
            x.append(ctrl.getXFromPV(bpm))
        return sum(x)/N

    def getXScreen(self,ctrl,camera,N):
        x=[]
        for i in range(N):
            x.append(caget(camera+':ANA:X_RBV'))
        return sum(x)/N

    def getSigmaXScreen(self,ctrl,camera,N):
        sX=[]
        for i in range(N):
            sX.append(caget(camera+':ANA:SigmaX_RBV'))
        return sum(sX)/N

    def getSigmaYScreen(self,ctrl,camera,N):
        sY=[]
        for i in range(N):
            sY.append(caget(camera+':ANA:SigmaY_RBV'))
        return sum(sY)/N

    def isBeamOnScreen(self,screen):
        #this does nothing at the moment
        return True                                            #Add a controller to input

    def align(self,hctrl,hcor, bctrl, bpm, tol, N):
        COR = hctrl.getMagObjConstRef(hcor)                                        #create a reference to the corrector
        x1= self.getXBPM(bctrl, bpm, N)                                            #get the x position on the BPM
        I1 = COR.siWithPol                                                        #x1,x2,I1,I2 are point to determine a straight linear relationship (I=mx+c)
        x2=x1
        I2=0
        if (COR.riWithPol>0.0):                                                    #determine intial step
            initialStep = -0.0001
        else:
            initialStep = 0.0001
        self.stepCurrent(hctrl, hcor, initialStep)
        self.simulate.run()                                                        #take inital step
        x2=self.getXBPM(bctrl, bpm, N)
        I2=COR.siWithPol
        while(x2>tol):                                                            # Algorithm loops until the current position is < the tolerance 'tol'
            I_o = (I1*x2-I2*x1)/(x2-x1)                                            # find the zero-crossing of straight line mde from positions at currents I1 and I2
            print('Predicted current intercept at '+str(I_o))
            hctrl.setSI(hcor,I_o)
            self.simulate.run()                                                    # set magnet to intercept current
            x1=x2                                                                #Get rid of first set of position and current
            I1=I2
            I2=I_o
            x2=self.getXBPM(bctrl, bpm, N)
            print('Current at'+str(x2))
            time.sleep(0.1)
        print('Aligned beam using ' + hcor + ' and ' + bpm)

    def bendBeam(self,dctrl,dipole,bctrl,bpm,screen, predictedI, tol, N=1):
        DIP = dctrl.getMagObjConstRef(dipole)                                    #create a reference to the dipole
        step = predictedI/100                                                    #1% of predicted current
        setI = 0.9*predictedI
        print ('90% of predicticted current is: ',setI)
        dctrl.setSI(dipole,setI)                                                #set dipole current to 90% of predicted
        self.simulate.run()
        while(self.isBeamOnScreen(screen)==False):                                #keep iterration of a 1% current step until beam is on screen
            self.stepCurrent(magCtrl,dipole,step)
            time.sleep(0.1)
        x_old=0                                                                    #fake start x position
        x=self.getXBPM(bctrl, bpm, N)                                            #All BPM posiotn are fake and based of the previous position
        print 'x = ', str(x), 'tol = ', str(tol)                                                                        #it wont stay this way for the real procedure

        while(x>tol):                                                            #start loop that ramps up dipole current (conitines unitl x<tolerance)
            print 'x = ', str(x), 'tol = ', str(tol)
            print '!!!In bend beam!!!: ', str(caget('VM-CLA-C2V-DIA-BPM-01:X'))
            self.stepCurrent(dctrl, dipole, step)
            x_old=x                                                                # keep a note of teh last beam position to roughly predict the effect of the next step
            x=self.getXBPM(bctrl, bpm, N)
            print(x)
            time.sleep(0.1)
            if x<(x_old-x):                                                        #if the step size look like it is will over bend the beam, half it.
                step = step*0.5
        print('Centered beam in Spectrometer line using ' + dipole + ' and ' + bpm)
        return dctrl.getSI(dipole)                                        #return the current at which beam has been centered
    """NEED TO TEST MINIMIZE BETA ON REAL MACHINE"""
    def minimizeBeta(self,qctrl,quad,sctrl,screen,init_step,N=1):
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
        else:
            qctrl.setSI(quad, -0.3)
        self.simulate.run()
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
            sX_1 = sX_2
            I_1 = I_2
            self.stepCurrent(qctrl, quad, step)
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
        self.simulate.run()
        print('Minimised Beta with '+quad+' on '+screen)

    def fixDispersion(self,qctrl,quad,sctrl,screen,step_size,N=1):
        #THis needs work!!!!self.finished.emit()
        qctrl.setSI(quad, 0.0)                                                    #set a fake start current
        self.simulate.run()                                                        #assumes beam is on screen
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

    def findDispersion(self,dctrl,dipole,sctrl,screen,centering_I,points,leveloff_threshold,N=1):
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
        self.simulate.run()

        #set dipole current to 95% of centering current
        setI = 0.95*centering_I
        print setI
        dctrl.setSI(dipole,setI)
        self.simulate.run()
        #I = totalIntensity(screen)
        #I_old = I/2
        #while(I/I_old-1>leveloff_threshold):
        #self.stepCurrent(dipole,step)
        currents[0] = DIP.siWithPol
        positions[0] = self.getXScreen(sctrl,screen,N)
        I_diff = 2*(centering_I-currents[0])/(points-1)

        for i in range(1,points):
            self.stepCurrent(dctrl, dipole, I_diff)
            currents[i] = DIP.siWithPol
            positions[i] = self.getXScreen(sctrl,screen,N)
            dCurrents=currents
            dPositions= positions
            if i==(points-1)/2:
                sX = self.getSigmaXScreen(sctrl,screen,N)

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
        mom1= (400.0033/D.magneticLength)*(np.polyval(D.fieldIntegralCoefficients, abs(I-Is))*physics.c*180)/(45*physics.pi*1000000000)
        mom2= (400.0033/D.magneticLength)*(np.polyval(D.fieldIntegralCoefficients, abs(Is+I))*physics.c*180)/(45*physics.pi*1000000000)
        print(mom1-mom2)/2
        return abs(mom1-mom2)/2

    def calcMom(self, dctrl,dipole, I):
        D = dctrl.getMagObjConstRef(dipole)
        return (400.0033/D.magneticLength)*(np.polyval(D.fieldIntegralCoefficients, abs(I))*physics.c*180)/(45*physics.pi*1000000000)

    def mom2I(self,dctrl,dipole,mom):
        D = dctrl.getMagObjConstRef(dipole)
        coeffs = list(D.fieldIntegralCoefficients)
        print coeffs
        print(1000000000*(mom*physics.pi*45)/(physics.c*180))
        coeffs[-1] -= (D.magneticLength/400.0033)*(1000000000*(mom*physics.pi*45)/(physics.c*180))
        roots = np.roots(coeffs)
        current = roots[-1].real
        return -current

    def using_move_to_thread(self,qctrl,quad,sctrl,screen,init_step,N=1):
        #print '\n\n\n Test in using_move_to_thread:'
        #self.simulate.run()
        #print '\n\n\n Simulation ran?'
        #print 'qctrl1'
        #print qctrl
        #print '\n\n\n'
        app = QCoreApplication([])
        objThread = QThread()
        obj = SomeObject()
        obj.moveToThread(objThread)
        obj.finished.connect(objThread.quit)
        objThread.started.connect(obj.minimizeBeta2(qctrl,quad,sctrl,screen,init_step))
        objThread.finished.connect(app.exit)
        objThread.start()
        sys.exit(app.exec_())

class SomeObject(QObject):

    finished = pyqtSignal()
    def minimizeBeta2(self,qctrl,quad,sctrl,screen,init_step,N=1):
        print 'we are heererereerere'
        #print Functions().TEST
        self.simulate = Functions.simulate
        #print Functions.stepCurrent.TEST
        #print Functions.__init__.TEST
        #print Functions.init.TEST
        #self.simulate = simulate
        #self.getSigmaXScreen = getSigmaXScreen
        #print 'qctrl2'
        #print qctrl
        #print '\n\n\n'
        QUAD = qctrl.getMagObjConstRef(quad)
        minimisingInX = False
        if(init_step>0):
            minimisingInX=True

        '''Quick scan to find rough minimum'''
        if(minimisingInX):
            print 'Rough scan in X'
            sX_scan = []
            xrange = np.arange(-50,50,10)
            for x in xrange:
                qctrl.setSI(quad, x)
                self.simulate.run()
                time.sleep(0.1)
                print(qctrl.getSI(quad))
                sX_scan.append(self.getSigmaXScreen(sctrl,screen,N))
            print sX_scan
            sX_approxmin = xrange[np.argmin(sX_scan)]
            print sX_approxmin

            print 'Fine scan in X'
            sX_scan2 = []
            xrange2 = np.arange(sX_approxmin-10,sX_approxmin+10,2)
            for x in xrange2:
                qctrl.setSI(quad, x)
                self.simulate.run()
                time.sleep(0.1)
                print(qctrl.getSI(quad))
                sX_scan2.append(self.getSigmaXScreen(sctrl,screen,N))
            print sX_scan2
            sX_min = xrange2[np.argmin(sX_scan2)]
            print sX_min
            qctrl.setSI(quad,sX_min)
        else:
            print 'Rough scan in Y'
            sY_scan = []
            yrange = np.arange(-50,50,10)
            for y in yrange:
                qctrl.setSI(quad, y)
                self.simulate.run()
                time.sleep(0.1)
                print(qctrl.getSI(quad))
                sY_scan.append(self.getSigmaYScreen(sctrl,screen,N))
            print sY_scan
            sY_approxmin = yrange[np.argmin(sY_scan)]
            print sY_approxmin

            print 'Fine scan in Y'
            sY_scan2 = []
            yrange2 = np.arange(sY_approxmin-10,sY_approxmin+10,2)
            for y in yrange2:
                qctrl.setSI(quad, y)
                self.simulate.run()
                time.sleep(0.1)
                print(qctrl.getSI(quad))
                sY_scan2.append(self.getSigmaYScreen(sctrl,screen,N))
            print sY_scan2
            sY_min = yrange2[np.argmin(sY_scan2)]
            print sY_min
            qctrl.setSI(quad,sY_min)

        self.simulate.run()
        print('Minimised Beta with '+quad+' on '+screen)
        self.finished.emit()
