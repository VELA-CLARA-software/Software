#import VELA_CLARA_LLRF_Control
import numpy
import epics

import time
#Debug
import array
import os

class LLRFMonitor:
    
    def __init__(self, beamline):
        #self.__m = VELA_CLARA_LLRF_Control.init()
        
        # Test area
        #self.__m.CLARA_LRRG_LLRF_CONFIG = "C:\\prj\\test_area\\VELA_CLARA_PYDs\\Config\\CLARA_LRRG_LLRF.config"
        #self.__m.setVerbose()
        '''
        if beamline == "LRRG":
            self.__c = self.__m.physical_VELA_LRRG_LLRF_Controller()
            self.__traces = ["CAVITY_FORWARD_POWER", "CAVITY_REVERSE_POWER", "KLYSTRON_FORWARD_POWER", "KLYSTRON_REVERSE_POWER"]
            self.__check = [False, True, False, False]
            
        elif beamline == "HRRG":
            self.__c = self.__m.physical_VELA_HRRG_LLRF_Controller()
            self.__traces = ["CAVITY_FORWARD_POWER", "CAVITY_REVERSE_POWER", "KLYSTRON_FORWARD_POWER", "KLYSTRON_REVERSE_POWER"]
            self.__check = [True, True, True, True]
        
        for t in self.__traces:
            self.__c.startTraceMonitoring(t)
        '''
        self.__lowMask = numpy.zeros(1017)
        self.__hiMask = numpy.zeros(1017)
        self.__maskCheckEnabled = False
        
        self.__rfSpPv = epics.PV("CLA-GUN-LRF-CTRL-01:vm:dsp:sp_amp:amplitude")
        self.__rfKlyFwdTracePv = epics.PV("CLA-GUN-LRF-CTRL-01:ad1:ch1:power_remote.POWER")
        self.__rfCavRevTracePv = epics.PV("CLA-GUN-LRF-CTRL-01:ad1:ch4:power_remote.POWER")
        self.__rfCavRevEvidPv = epics.PV("CLA-GUN-LRF-CTRL-01:ad1:ch4:power_remote.EVID")
    
        self.evid = self.__rfCavRevEvidPv.get()

    def getRfSp(self):
        #return self.__c.getAmpSP()
        return self.__rfSpPv.get()

    def setRfSp(self, sp):
        #self.__c.setAmpSP(sp)
        self.__rfSpPv.put(sp)
        
    def getKlyFwRfPower(self):
        #CTL trc = self.__c.getTraceValues("KLYSTRON_FORWARD_POWER")
        trc = self.__rfKlyFwdTracePv.get()
        # Todo choose start_index and stop_index for calculating avg power
        # 1.5us, starts at 0.65 stops at 2, one sample is 0.00914454277286135693215339233038us
        return numpy.mean(trc[71:218])
    
    # If masks are not enabled this will return True
    def isRfOk(self):
        #rtn = True
        #for i in range(0, len(self.__traces)):
        #    if self.__check[i]:
        #        rtn &= self.__c.isCheckingMask(self.__traces[i])
        #       print self.__c.isCheckingMask(self.__traces[i])
        #return rtn
        
        #trace = self.__c.getTraceValues("CAVITY_REVERSE_POWER")
        
        trace = self.__rfCavRevTracePv.get()
        
        rtn = True
        
        if ( trace < self.__lowMask ).any():
            if self.__maskCheckEnabled:
                rtn = False
                
        if ( trace > self.__hiMask ).any():
            if self.__maskCheckEnabled:
                rtn = False
                
        return rtn
        
    def setRfMasks(self, trace):
    
        #print 'setRfMasks ' + str(state)
        
        # Activate or deactivate mask checking
        #for t in self.__traces:
        #    #self.__c.setCheckMask(t, state)
        #    self.__c.setShouldCheckMask(t, state)
        #    
        #for i in range(0, len(self.__traces)):
        #    hiMask = numpy.array(traces[i,:]) * 1#1.1
        #    loMask = numpy.array(traces[i,:]) * 1#0.9
        #    self.__c.setHighMask(self.__traces[i], hiMask.tolist())
        #    self.__c.setLowMask(self.__traces[i], loMask.tolist())
        self.__lowMask = trace * 0.5 - 100e3 # -10% -20kW
        self.__hiMask = trace * 3 + 50e3 # +10% +20kW
        
    def enableRfMasks(self, state):
        self.__maskCheckEnabled = state
        
    def getCavRevTrace(self):
        '''
        trs = numpy.empty((   len(self.__traces), 1017   ))
        for i in range(0, len(self.__traces)):
            numpy.copyto(   trs[i,:],   self.__c.getTraceValues(self.__traces[i])   )
        return trs
        '''
        return self.__rfCavRevTracePv.get()
        
    def getEmptyTraces(self):
        #return numpy.empty((len(self.__traces), 1017))
        return numpy.zeros(1017)
        
    def waitForRfPulse(self):
        eq = True
        while eq:
            time.sleep(1e-3)
            curr_evid = self.__rfCavRevEvidPv.get()
            eq = self.evid == curr_evid
        self.evid = curr_evid
        