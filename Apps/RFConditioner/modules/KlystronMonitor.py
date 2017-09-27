#   This class will monitor the klystron running state, and clears fault conditions if detected

#import VELA_CLARA_RF_Modulator_Control

import epics

class KlystronMonitor:

    def __init__(self):
        #self.__m = VELA_CLARA_RF_Modulator_Control.init()
        #self.__c = self.__m.physical_GUN_MOD_Controller()
        #self.__c.enable()
        
        self.__klyStatusPv = epics.PV("CLA-GUNS-HRF-MOD-01:Sys:StateSet")
    
    def isKlystronOk(self):
        #return self.__c.isGood()
        
        # 3 is equivalent to "Trig"
        return self.__klyStatusPv.get() == 3