# THIS PROGRAM MAY NOT WORK AT NON-NOMINAL MOMENTUM - WE TRIED CRESTING AT 3MeV/c AND THE PROGRAM KEPT CRASHING
# WE NEED TO LOOK AT HOW IT SETS VALUES.



from math import *
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
from scipy import constants
import velaBPMGlobals as vbpmg
import time
import epics
import monitorInterface
from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import pub 
import os
import time
import wx
import sys
import velaRFControl as vRF
import velaMagnetControl as vMC
import phaseCalibrateGUI as GUI
import urllib



class MasterController():
    def __init__(self, app):
        try:
            print 'Master Controller initialised'
            #initialise gui
            self.gui = GUI.MyFrameSub(None)
            self.gui.Show(True)
            pub.subscribe(self.doMeasurement, "startCalibrate")
            
            #create bpm and screen monitors
            self.velaBPMControl1 = monitorInterface.BPMMonitor()
            self.velaScopeControl1 = monitorInterface.scopeMonitor()
        
            #choose which BPM and Scope we are using, in this case I have just set it to 'EBT-INJ-DIA-BPMC-04' (BPM2) and 'EBT-INJ-SCOPE-01'
            self.BPM = vbpmg.globalBPMNames[ 2 ]
            self.scope = vbpmg.globalScopeNames[ 0 ]
            print 'Monitoring ', self.BPM
            
            #initialise RF and Magnet controllers
            self.RFControl = vRF.velaRFController()
            self.MagControl = vMC.velaMagnetController()
            self.MagControl.startAllMonitors()
            
            self.phaselist1 = []
            self.phaselist2 = []
            self.amplist = []
            self.meanX1 = []
            self.meanX2 = []
            self.meanQ = []
            self.stdX1 = []
            self.stdX2 = []
            self.stdQ = []
            self.yfit1 = []
            self.yfit2 = []
            
        except:
            print 'Error in initialising Master Controller'
            sys.exit()
        
    def doMeasurement(self, message):
        #calls all of the other processes, in order
        self.currentConfig = message.data
        print 'Current Config'
        for i in self.currentConfig.keys():
            print i, ' = ', self.currentConfig[ i ]
        
        print 'Initialising magnets'
        self.magnetControl()
        print 'Finding approximate crest using wall current monitor'
        self.approxCrest()
        print 'Checking screen'
        self.checkScreen()
        print 'Finding Crest'
        self.findCrest()
        print 'Saving data'
        self.saveData()
        print 'Setting BPM reading to zero using RF amplitude'
        self.setRFAmp()
        print 'The RF phase has been set to ', self.phaseformax2
        print 'The RF amplitude has been set to ', self.ampforzero
        print 'Close this window to exit the Phase Calibrate program'
        
    def magnetControl( self ):
        
        try:
            #finding the correct DIP01 current for a specified momentum using formula from magnets table
            mom = float(self.currentConfig['Momentum'])
            len = 403.3e-3
            field = pi*mom/(4e-6*constants.c*len)
            current = (1/0.0193)*(field - 0.0007)
            
            if current > 2.0:
                print 'ERROR: INPUT MOMENTUM IS TOO HIGH'
                sys.exit()
                
            
            print 'Degaussing BSOL?', self.currentConfig['DegaussBSOL']
            print 'Degaussing SOL?', self.currentConfig['DegaussSOL']
            print 'Degaussing DIP01?', self.currentConfig['DegaussDIP01']
            print 'Degaussing QUAD01?', self.currentConfig['DegaussQUAD01']
            print 'Degaussing QUAD02?', self.currentConfig['DegaussQUAD02']
            print 'Degaussing QUAD03?', self.currentConfig['DegaussQUAD03']
            print 'Degaussing QUAD04?', self.currentConfig['DegaussQUAD04']
            print 'Turning Quads off?', self.currentConfig['QuadsOFF']
            print 'Turning Correctors off?', self.currentConfig['CorrectorsOFF']
            
            if self.currentConfig['DegaussBSOL'] == True:
                self.MagControl.deGauss('BSOL')
                pass        
            if self.currentConfig['DegaussSOL'] == True:
                self.MagControl.deGauss('SOL')
                pass
            if self.currentConfig['DegaussDIP01'] == True:
                self.MagControl.deGauss('DIP01') 
                pass            
            if self.currentConfig['DegaussQUAD01'] == True:
               self.MagControl.deGauss('QUAD01')
               pass
            if self.currentConfig['DegaussQUAD02'] == True:
                self.MagControl.deGauss('QUAD02')
                pass
            if self.currentConfig['DegaussQUAD03'] == True:
                self.MagControl.deGauss('QUAD03')
                pass
            if self.currentConfig['DegaussQUAD04'] == True:
                self.MagControl.deGauss('QUAD04')
                pass

            
            quads = [ 'QUAD01', 'QUAD02', 'QUAD03', 'QUAD04', 'QUAD05', 'QUAD06' ]
            correctors = [ 'HCOR03', 'HCOR04', 'HCOR05', 'VCOR03', 'VCOR04', 'VCOR05']
            
            if self.currentConfig['QuadsOFF'] == True:
                for i in quads:
                    self.MagControl.switchOFFpsu( i )
                    pass
            if self.currentConfig['CorrectorsOFF'] == True:
                for i in correctors:
                    self.MagControl.switchOFFpsu( i )
                    pass
            
            print 'Setting the dipole current to ', current
            self.MagControl.setSI('DIP01', current, 0.0001, 2)
            
        except:
            print 'Error in magnet control'

    
    def approxCrest(self):
        try:
            #can choose a wide range here as won't go off bpm
            for phase in np.linspace(-115.0, -75.0, 20):
                self.RFControl.setGunPhi(phase)
                currphase = self.RFControl.getGunPhi()
                
                #wait until phase is set
                timeout = time.time() + 5
                while abs(phase - currphase) > 0.1:
                    currphase = self.RFControl.getGunPhi()
                    if time.time() > timeout:
                        break
            
                self.phaselist1.append(currphase)
                print 'Current phase ', self.phaselist1[-1]
               
                self.velaScopeControl1.monitorScopeForNCounts( self.scope,  self.currentConfig['Shots'] )
            
                while True:
                    if self.velaScopeControl1.isBusy( self.scope ) == False:
                        break
                    #exits the while loop
            
                self.scopeData = self.velaScopeControl1.getChargeData( self.scope )

                #find mean charge from the N shots
                self.meanQ.append(np.mean( self.scopeData ))
            
                #find standard deviation
                stddev = np.std(self.scopeData)
                self.stdQ.append(stddev)
            
            plt.errorbar(self.phaselist1, self.meanQ, self.stdQ, color = 'b')

            #finding the peak of the curve
            def func(list, a, b, c):
                x = np.array(list)
                return a*x**2 + b*x + c
                
            popt, pcov = curve_fit(func, self.phaselist1, self.meanQ, p0=None, sigma=np.array(self.stdQ), absolute_sigma=False)
            self.yfit1 = func(self.phaselist1, *popt)
            self.maxy1 = max(self.yfit1)
            p = popt[0]
            q = popt[1]
            r = popt[2] - self.maxy1
            self.phaseformax1 = (-q + np.sqrt(q**2-4*p*r))/(2*p)
            plt.plot(self.phaselist1, self.yfit1, color = 'r')
            plt.xlabel('Phase')
            plt.ylabel('Charge Reading')
            plt.title('Close this plot if happy with fit and program will continue')
            self.approxcrest = self.phaseformax1 - 30
            print 'Approximate crest = ', self.approxcrest
            plt.show()
        except:
            print 'Error in approximate cresting using wall current monitor'

                
    def checkScreen(self):
        pass 
        

    def findCrest( self ):
        try:
            self.range = self.currentConfig['Range']
            for phase in np.linspace(self.approxcrest-self.range/2, self.approxcrest+self.range/2, 20):
                self.RFControl.setGunPhi(phase)
                currphase = self.RFControl.getGunPhi()
                
                #wait until phase is set
                timeout = time.time() + 5
                while abs(phase - currphase) > 0.1:
                    currphase = self.RFControl.getGunPhi()
                    if time.time() > timeout:
                        break
                
                self.phaselist2.append(currphase)
                print 'Current phase ', self.phaselist2[-1]
               
                self.velaBPMControl1.monitorBPMForNCounts( self.BPM,  self.currentConfig['Shots'] )
            
                while True:
                    if self.velaBPMControl1.isBusy( self.BPM ) == False:
                        break
                    #exits the while loop
            
                self.positionData1 = self.velaBPMControl1.getAllPositionData( self.BPM )

                #find mean X from the N shots
                self.meanX1.append(np.mean( self.positionData1[0] ))
            
                #find standard deviation
                stddev = np.std(self.positionData1[0])
                self.stdX1.append(stddev)
                
                #if the beam is not on the bpm then the same value will be read n times, need to remove these data points
                if stddev == 0.0:
                    print  'ERROR:BEAM NOT SHOWN ON BPM'
                    self.stdX1.pop()
                    self.meanX1.pop()
                
            
            plt.errorbar(self.phaselist2, self.meanX1, self.stdX1, color = 'b')
            
            #finding the peak of the curve
            def func(list, a, b, c):
                x = np.array(list)
                return a*x**2 + b*x + c
                
            popt, pcov = curve_fit(func, self.phaselist2, self.meanX1, p0=None, sigma=np.array(self.stdX1), absolute_sigma=False)
            self.yfit2 = func(self.phaselist2, *popt)
            self.maxy2 = max(self.yfit2)
            p = popt[0]
            q = popt[1]
            r = popt[2] - self.maxy2
            self.phaseformax2 = (-q + np.sqrt(q**2-4*p*r))/(2*p)
            plt.plot(self.phaselist2, self.yfit2, color = 'r')
            plt.xlabel('Phase')
            plt.ylabel('BPM Reading')
            plt.title('Close this plot if happy with fit and program will continue')
           
            print 'Crest phase', self.phaseformax2
            
            #set the phase to the crest phase found plus the offset
            self.offset = self.currentConfig['Degrees']
            print 'Offset from crest by', self.offset
            self.RFControl.setGunPhi(self.phaseformax2 + self.offset)
            
            plt.show()
        except:
            print 'Error finding crest'
            sys.exit()
            
    def setRFAmp(self):
            #make sure that the Klystron forward power absolutely never goes above 10
            power = self.RFControl.getKlyFWD()
            if power < 10:
                #changing amp to set BPM reading to zero
                startamp = self.RFControl.getGunAmp()
                for amp in np.linspace(startamp-10, startamp+10, 20):
                    self.RFControl.setGunAmp(int(round(amp)))
                    power = self.RFControl.getKlyFWD()
                    curramp = self.RFControl.getGunAmp()
            
                    self.amplist.append(curramp)
                    print 'Current RF amplitude ', self.amplist[-1]
               
                    self.velaBPMControl1.monitorBPMForNCounts( self.BPM,  self.currentConfig['Shots'] )
            
                    while True:
                        if self.velaBPMControl1.isBusy( self.BPM ) == False:
                            break
                        #exits the while loop
            
                    self.positionData2 = self.velaBPMControl1.getAllPositionData( self.BPM )

                    #find mean X from the N shots
                    self.meanX2.append(np.mean( self.positionData2[0] ))
                
                    #find standard deviation
                    stddev = np.std(self.positionData2[0])
                    self.stdX2.append(stddev)
                
                    #if the beam is not on the bpm then the same value will be read n times, need to remove these data points
                    if stddev == 0.0:
                        print  'ERROR:BEAM NOT SHOWN ON BPM'
                        self.stdX2.pop()
                        self.meanX2.pop()
                
            
                plt.errorbar(self.amplist, self.meanX2, self.stdX2, color = 'b')
            
                #finding the peak of the curve
                def func2(list, a, b, c):
                    x = np.array(list)
                    return a*x + b
                
                popt, pcov = curve_fit(func2, self.amplist, self.meanX2, p0=None, sigma=np.array(self.stdX2), absolute_sigma=False)
                self.yfit3 = func2(self.amplist, *popt)
                p = popt[0]
                q = popt[1]
                self.ampforzero = -q/p
                plt.plot(self.amplist,self.yfit3, color = 'r')
                plt.xlabel('Amp')
                plt.ylabel('BPM Reading')
                plt.title('Close this plot if happy with fit and program will continue')
                plt.show()
                
                print 'Amplitude to centre in BPM', self.ampforzero
                #set the amplitude to that which gives zero on the bpm
                self.RFControl.setGunAmp(int(round(self.ampforzero)))  
            else:
                print 'Klystron FWD Power too high'
                sys.exit()
            
    def saveData( self ):
        try:
            text_file = open( 'data.txt', "w" )
            text_file.write('Mean X')
            text_file.write('\t')
            text_file.write('Std X')
            text_file.write('\n')
            for i in range(len(self.meanX1)):
                text_file.write( str( self.meanX1[ i ] ) )
                text_file.write( "\t" )
                text_file.write( str( self.stdX1[ i ] ) )
                text_file.write( "\n" )
            text_file.close()
        except:
            print 'Error saving data'
            
if __name__ == "__main__":

    os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
    os.environ["EPICS_CA_ADDR_LIST"] = "192.168.83.255"
    print 'EPICS_CA_AUTO_ADDR_LIST = ', os.environ["EPICS_CA_AUTO_ADDR_LIST"]
    print 'EPICS_CA_ADDR_LIST = ', os.environ["EPICS_CA_ADDR_LIST"]
    print 'EPICS_CA_MAX_ARRAY_BYTES = ', os.environ["EPICS_CA_MAX_ARRAY_BYTES"]
    
    app = wx.App(False)
    mc = MasterController(app)    
    app.MainLoop() 