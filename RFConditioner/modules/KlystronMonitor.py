#   This class will monitor the klystron running state, and clears fault conditions if detected

#import VELA_CLARA_RF_Modulator_Control

class KlystronMonitor:

    def __init__(self):
        x = 1
        #self.__m = VELA_CLARA_RF_Modulator_Control.init()
        #self.__c = self.__m.physical_GUN_MOD_Controller()
        #self.__c.enable()
    
    def isKlystronOk(self):
        #return self.__c.isGood()
        return True