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
import copy


class dummyOM():
        def __init__(self):
            print 'made a dummy OM'
        def run():
            print 'running NO simulation'


'''This Class contain function to use in a momentum procedure independant '''


class Functions(QObject):
    qctrl_sig = pyqtSignal(float)

    def __init__(self, OM = dummyOM() ):
        QThread.__init__(self)
        self.simulate = OM

    def stepCurrent(self,ctrl,magnet,step):
        MAG = ctrl.getMagObjConstRef(magnet)
        setI = MAG.siWithPol + step
        print('Stepping current to: '+str(setI))
        ctrl.setSI(magnet,setI)
        while ctrl.getSI(magnet) != setI:
            print ctrl.getSI(magnet)
            #self.qctrl.setSI(self.quad, x)
            time.sleep(0.5)
        #self.simulate.run()

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
            self.simulate.run()
            time.sleep(1)
            print '\n\n\nHere we are', str(x)                                                #set dipole current to 90% of predicted
            print dctrl.getSI(dipole)
            print '\n\n\n'
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

    # def get_qctrl_sig(self):
    #     print 'in get_qctrl_sig'
    #
    # def startBPMTimer(self, crester):
    #     self.qctrl_sig.connect(crester.update_qctrl_sig)
    #     self.timer = QTimer()
    #     self.timer.timeout.connect(lambda : self.getBPMPosition(self.parameters['bpm']))
    #     self.timer.start(100)

    def minBetaThread(self,qctrl,quad,sctrl,screen,init_step,N=1):
        self.threadObject = self.MinBetaStartThread(self, MinimiseBetaClass, qctrl,quad,sctrl,screen,init_step,self.simulate)

    def bendBeamThread(self,dctrl,dipole,bctrl,bpm,screen, predictedI, tol, N=1):
        self.threadObject = self.BendBeamStartThread(self, BendBeamClass, dctrl,dipole,bctrl,bpm,screen, predictedI, tol, self.simulate)

    def printFinished(self):
        self.test_continue=2
        print '\n\n\n\n\n\n\nThread Finished!\n\n\n\n\n\n'

    class MinBetaStartThread(QObject):
        def __init__(self, parent, MinimiseBetaClass, *args):#, **kwargs):
            #parent.disableButtons()
            self.minbeta = MinimiseBetaClass(parent, *args)#, **kwargs)
            #self.minbeta.setPhase.connect(parent.setPhase)
            #timer(self.minbeta)
            self.thread = QThread()  # no parent!
            self.minbeta.moveToThread(self.thread)
            self.thread.started.connect(self.minbeta.minimizeBeta2)
            self.minbeta.finished.connect(parent.printFinished)
            #self.minbeta.finished.connect(parent.timer.stop)
            #self.minbeta.finished.connect(parent.enableButtons)
            #self.minbeta.finishedSuccesfully.connect(lambda : phaser(offset=False))
            self.minbeta.finished.connect(self.thread.quit)
            self.thread.start()

    class BendBeamStartThread(QObject):
        def __init__(self, parent, MinimiseBetaClass, *args):#, **kwargs):
            #parent.disableButtons()
            self.bendbeam = BendBeamClass(parent, *args)#, **kwargs)
            #self.bendbeam.setPhase.connect(parent.setPhase)
            #timer(self.bendbeam)
            self.thread = QThread()  # no parent!
            self.bendbeam.moveToThread(self.thread)
            self.thread.started.connect(self.bendbeam.bendBeam)
            self.bendbeam.finished.connect(parent.printFinished)
            #self.bendbeam.finished.connect(parent.timer.stop)
            #self.bendbeam.finished.connect(parent.enableButtons)
            #self.bendbeam.finishedSuccesfully.connect(lambda : phaser(offset=False))
            self.bendbeam.finished.connect(self.thread.quit)
            self.thread.start()

class threadObject(QObject):
	finished = pyqtSignal()
	#finishedSuccesfully = pyqtSignal()
	#setPhase = pyqtSignal(str, float)
	#data = []
	_isRunning = True
	_finish = False

	def stop(self):
		print 'stopping worker!'
		self._isRunning = False

	def finish(self):
		print 'finishing worker!'
		self._finish = True

class MinimiseBetaClass(threadObject):
    def __init__(self, parent,qctrl,quad,sctrl,screen,init_step,simulate,N=1):
        super(MinimiseBetaClass, self).__init__()
        self.parent = parent
        self.Fns = Functions()
        self.qctrl = qctrl
        self.quad = quad
        self.sctrl = sctrl
        self.screen = screen
        self.init_step = init_step
        self.simulate = simulate
        self.N = N

    def minimizeBeta2(self):
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
                while self.qctrl.getSI(self.quad) != x:
                    print self.qctrl.getSI(self.quad)
                    #self.qctrl.setSI(self.quad, x)
                    time.sleep(0.5)
                #time.sleep(5)
                self.simulate.run()
                time.sleep(2)
                print '\n\n\nDID IT WORK HERE?', str(x)
                print(self.qctrl.getSI(self.quad))
                print '\n\n\n'
                sX_scan.append(self.Fns.getSigmaXScreen(self.sctrl,self.screen,self.N))
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
                sX_scan2.append(self.Fns.getSigmaXScreen(self.sctrl,self.screen,self.N))
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
                sY_scan.append(self.Fns.getSigmaYScreen(self.sctrl,self.screen,self.N))
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
                sY_scan2.append(self.Fns.getSigmaYScreen(self.sctrl,self.screen,self.N))
            print sY_scan2
            sY_min = yrange2[np.argmin(sY_scan2)]
            print sY_min
            self.qctrl.setSI(self.quad,sY_min)

        self.simulate.run()
        print('Minimised Beta with '+self.quad+' on '+self.screen)
        self.finished.emit()

class BendBeamClass(threadObject):
    def __init__(self, parent,dctrl,dipole,bctrl,bpm,screen, predictedI, tol,simulate,N=1):
        super(BendBeamClass, self).__init__()
        self.parent = parent
        self.Fns = Functions()
        self.dctrl = dctrl
        self.dipole = dipole
        self.bctrl = bctrl
        self.bpm = bpm
        self.screen = screen
        self.predictedI = predictedI
        self.tol = tol
        self.simulate = simulate
        self.N = N

    def bendBeam(self):
        DIP = self.dctrl.getMagObjConstRef(self.dipole)                                    #create a reference to the dipole
        step = self.predictedI/100                                                    #1% of predicted current
        setI = 0.9*self.predictedI
        print ('90% of predicticted current is: ',setI)
        print self.dipole
        print setI
        print self.dctrl
        self.dctrl.setSI(self.dipole,setI)
        while self.dctrl.getSI(self.dipole) != setI:
            print self.dctrl
            print setI
            print self.Fns
            print self.dipole
            print self.predictedI
            print self.simulate
            print self.dctrl.getSI(self.dipole)
            #self.qctrl.setSI(self.quad, x)
            time.sleep(0.5)
        time.sleep(1)
        print '\n\n\nHere we are\n\n\n'                                                #set dipole current to 90% of predicted
        print self.dctrl.getSI(self.dipole)
        time.sleep(10)
        self.simulate.run()
        #while(self.isBeamOnScreen(screen)==False):                                #keep iterration of a 1% current step until beam is on screen
        #    self.stepCurrent(magCtrl,dipole,step)
        #    time.sleep(0.1)
        x_old=0                                                                    #fake start x position
        x=self.Fns.getXBPM(self.bctrl, self.bpm, self.N)                                            #All BPM posiotn are fake and based of the previous position
        print 'x = ', str(x), 'tol = ', str(self.tol)                                                                        #it wont stay this way for the real procedure

        while(x<-self.tol):                                                            #start loop that ramps up dipole current (conitines unitl x<tolerance)
            print 'x = ', str(x), 'tol = ', str(self.tol)
            print '!!!In bend beam!!!: ', str(caget('VM-CLA-C2V-DIA-BPM-01:X'))
            self.Fns.stepCurrent(self.dctrl, self.dipole, step)
            self.simulate.run()
            time.sleep(1)
            print '\n\n\nHere we are', str(x)                                                #set dipole current to 90% of predicted
            print self.dctrl.getSI(self.dipole)
            print '\n\n\n'
            x_old=x                                                                # keep a note of teh last beam position to roughly predict the effect of the next step
            x=self.Fns.getXBPM(self.bctrl, self.bpm, self.N)
            print(x)
            time.sleep(0.1)
            #if x<(x_old-x):                                                        #if the step size look like it is will over bend the beam, half it.
            #    step = step*0.5
        print('Centered beam in Spectrometer line using ' + self.dipole + ' and ' + self.bpm)
        return self.dctrl.getSI(self.dipole)                                        #return the current at which beam has been centered
        self.finished.emit()
