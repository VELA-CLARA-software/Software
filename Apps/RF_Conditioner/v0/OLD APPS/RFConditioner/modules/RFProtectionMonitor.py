#   This class will monitor the RF protection was triggered, and signal to the controller if needed

#import VELA_CLARA_RF_Protection_Control

import epics

class RFProtectionMonitor:

    def __init__(self):
        #self.__c = VELA_CLARA_RF_Protection_Control.init()
        
        self.__interlockStatusPv = epics.PV("CLA-GUN-LRF-CTRL-01:app:interlock:state")
        self.__rfOutputEnablePv = epics.PV("CLA-GUN-LRF-CTRL-01:app:rf_ctrl")
        self.__setpointLockedPv = epics.PV("CLA-GUN-LRF-CTRL-01:vm:dsp:ff_amp:lock")
        
    def isProtectionOk(self):
    
        rtn = True
    
        # 0 is OK
        if self.__interlockStatusPv.get() != 0:
            rtn = False
    
        # 1 is enabled
        if self.__rfOutputEnablePv.get() != 1:
            rtn = False
        
        # 1 is locked
        if self.__setpointLockedPv.get() != 1:
            rtn = False
    
        return rtn