from PyQt4.QtCore import QObject#, pyqtSignal
from PyQt4.QtGui import QApplication
import numpy as np
from numpy.polynomial import polynomial as P
import scipy.constants as physics
import time

class Functions(QObject):
    #qctrl_sig = pyqtSignal(float)

    #def __init__(self, OM = dummyOM()):
    def __init__(self, model):
        super(Functions, self).__init__()
        self.model = model

    def test(self, x):
        print x*2

    def I2mom(self, dctrl, dipole, I):
        D = dctrl.getMagObjConstRef(dipole)
        #return (400.0033/D.magneticLength)*(np.polyval(D.fieldIntegralCoefficients, abs(I))*physics.c*180)/(45*physics.pi*1000000000)
        return (np.polyval(D.fieldIntegralCoefficients, abs(I))*physics.c*180)/(45*physics.pi*1e9)

    def mom2I(self, dctrl, dipole, mom):
        D = dctrl.getMagObjConstRef(dipole)
        coeffs = list(D.fieldIntegralCoefficients)
        #print coeffs
        #print(1000000000*(mom*physics.pi*45)/(physics.c*180))
        #coeffs[-1] -= (D.magneticLength/400.0033)*(1000000000*(mom*physics.pi*45)/(physics.c*180))
        coeffs[-1] -= (1e9*(mom*physics.pi*45)/(physics.c*180))
        roots = np.roots(coeffs)
        current = roots[-1].real
        return current

    def getBPMPosition(self, ctrl, bpm):
        return ctrl.getXFromPV(bpm)

    def stepCurrent(self,ctrl,magnet,step):
        MAG = ctrl.getMagObjConstRef(magnet)
        setI = MAG.siWithPol + step
        print('Stepping current to: '+str(setI))
        ctrl.setSI(magnet,setI)
        #self.simulate.run()

    def setCurrent(self,ctrl,magnet,value):
        MAG = ctrl.getMagObjConstRef(magnet)
        setI = value#MAG.siWithPol + step
        print('Stepping current to: '+str(setI))
        ctrl.setSI(magnet,setI)
        #self.simulate.run()

    def stepRF(self,ctrl,step):
        setAmp = ctrl.getAmpSP() + step
        print('Stepping amplitude to: '+str(setAmp))
        ctrl.setAmpSP(setAmp)

    def getXBPM(self,ctrl,bpm,N):
        x=[]
        for i in range(N):
            #21/8/18 changed getXFromPV to getX
            a = ctrl.getX(bpm)
            print ctrl.getBPMStatus(bpm)
            #a = ctrl.getBPMStatus(bpm)
            #print type(a)
            #print 'Here'
            #b = str(a)
            #print b
            #print type(b)
            #if ctrl.getBPMStatus(bpm) == 'BPM_STATUS.GOOD':
            if str(ctrl.getBPMStatus(bpm)) == 'GOOD':
                x.append(a)
                print a, 'shot ok'
            else:
                N-=1
                print a, 'shot excluded'
            time.sleep(0.1)
        if N > 1:
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
        #print 'here1'
        if (COR[0].riWithPol>0.0):                                                    #determine intial step
            print 'polarity>0'
            initialStep = -initstep
        else:
            print 'polarity<0'
            initialStep = initstep
        #print 'here2'
        self.stepCurrent(hctrl, hcor, initialStep)
        time.sleep(1)
        #self.simulate.run()                                                        #take inital step
        x2=self.getXBPM(bctrl, bpm, N)
        I2=COR[0].siWithPol
        #print 'here3'
        print 'before while, x1:', str(x1), 'x2', str(x2), 'tol', str(tol)
        count = 1
        #print bctrl.getBPMStatus(bpm)
        #print type(x2), type(off), type(tol), type(count), type(x2), type(x1)
        while (abs(x2-off)>tol) and count<5 and abs(x2-x1)>(tol/10):                                                            # Algorithm loops until the current position is < the tolerance 'tol'
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
            print 'Alignment failed, use manual correction with up/down arrows'

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
        while(abs(x2-off)>tol) and count<5:
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
            print 'Alignment failed, use manual correction with up/down arrows'


    def bendBeam(self,dctrl,dipole,bctrl,bpm, IMin, IMax, tol, N=10):
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
        #while(self.isBeamOnScreen(screen)==False):                                #keep iterration of a 1% current step until beam is on screen
        #    self.stepCurrent(magCtrl,dipole,step)
        #    time.sleep(0)
        x_old=0                                                                    #fake start x position
        x=self.getXBPM(bctrl, bpm, N)                                            #All BPM posiotn are fake and based of the previous position
        print 'x = ', str(x), 'tol = ', str(tol)                                                                        #it wont stay this way for the real procedure
        #time.sleep(100)
        #for n in range(1,1000):
        #    time.sleep(0.1)
        #    print 'is it updating?', str(n)
        #    QApplication.processEvents()
        while(x<-tol):                                                            #start loop that ramps up dipole current (conitines unitl x<tolerance)
            #print 'x = ', str(x), 'tol = ', str(tol)
            print '!!!In bend beam!!!: '#, str(caget('CLA-C2V-DIA-BPM-01:X'))
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
            QApplication.processEvents()
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
        positions[0] = self.model.cam.getX(screen)
        print centering_I
        print currents[0]
        print points-1
        I_diff = 2*(centering_I-currents[0])/(points-1)

        for i in range(1,points):
            print 'i', str(i)
            print 'I_diff', str(I_diff)
            self.stepCurrent(dctrl, dipole, I_diff)
            QApplication.processEvents()
            time.sleep(3)
            currents[i] = DIP.siWithPol
            #positions[i] = self.getXScreen(sctrl,screen,N)
            positions[i] = self.model.cam.getX(screen)
            dCurrents=currents
            dPositions= positions
            if i==(points-1)/2:
                #sX = self.getSigmaXScreen(sctrl,screen,N)
                sX = self.model.cam.getSigX(screen)

        c, stats = P.polyfit(currents,positions,1,full=True)
        fCurrents=[0.90*centering_I,1.1*centering_I]
        fPositions=[(c[1]*0.90*centering_I)+c[0],(c[1]*1.10*centering_I)+c[0]]
        print(c)
        print('Determined Dispersion with '+dipole+' and '+screen)
        print('dispersion'+str(c[1])+' and  beamsigma is'+str(sX))

        setI = dCurrents[-1]
        for a in reversed(np.linspace(centering_I,setI, 10)): #slowly set offset to allow image collector to keep up
            print 'Moving to original position'
            QApplication.processEvents()
            dctrl.setSI(dipole,a)
            time.sleep(2)

        #print 'dCurrents', str(dCurrents)
        #print 'fCurrents', str(fCurrents)
        return c[1],sX,dCurrents,dPositions,fCurrents,fPositions

    '''The following has been altered to work with the online model (400.0033)'''
    def calcMomSpread(self,dctrl,dipole, Is, I):
        D = dctrl.getMagObjConstRef(dipole)
        #mom1= (400.0033/D.magneticLength)*(np.polyval(D.fieldIntegralCoefficients, abs(I-Is))*physics.c*180)/(45*physics.pi*1000000000)
        #mom2= (400.0033/D.magneticLength)*(np.polyval(D.fieldIntegralCoefficients, abs(Is+I))*physics.c*180)/(45*physics.pi*1000000000)
        mom1= (np.polyval(D.fieldIntegralCoefficients, abs(I-Is))*physics.c*180)/(45*physics.pi*1e9)
        mom2= (np.polyval(D.fieldIntegralCoefficients, abs(Is+I))*physics.c*180)/(45*physics.pi*1e9)
        #print(mom1-mom2)/2
        return abs(mom1-mom2)/2
