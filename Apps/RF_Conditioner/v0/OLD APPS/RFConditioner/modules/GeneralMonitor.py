#   This class will monitor the dark current and the vacuum for breakdowns.
#
#   The last vacuum level reading is compared to a "background" vacuum level.
#
# TODO list:
# add cavity temperature protection?

#import VELA_CLARA_General_Monitor
import epics
import numpy

class GeneralMonitor:
    
    __vacAvgTimeS = 10
    __dcAvgTimeS = 10
    '''
    __m = VELA_CLARA_General_Monitor.init()
    
    # TODO: this is LRRG vac PV
    #__vacPv = __m.connectPV("CLA-S01-VAC-IMG-01:PRES")
    __vacPv = __m.connectPV("CLA-LRG1-VAC-IMG-01:P")
    # TODO: this is LRRG DC PV, search for HRRG one and it's propreties
    __dcPv = __m.connectPV("EBT-INJ-SCOPE-01:P3")
    
    __vacHist = [  __m.getValue( __vacPv )  ]
    __dcHist = [  __m.getValue( __dcPv )  ]
    '''
    
    __vacPv = epics.PV("CLA-LRG1-VAC-IMG-01:P")
    __dcPv = epics.PV("EBT-INJ-SCOPE-01:P3")
    __vacHist = [  __vacPv.get()  ]
    __dcHist = [  __dcPv.get()  ]

    def __init__(self, repRate, vacSpikeDelta, dcSpikeDelta):
        self.__vacAvgSampCount = repRate * self.__vacAvgTimeS
        self.__vacSpikeDelta = vacSpikeDelta
        self.__dcAvgSampCount = repRate * self.__dcAvgTimeS
        self.__dcSpikeDelta = dcSpikeDelta
        
    def isVacuumOk(self):
        #vacCurrVal = self.__m.getValue( self.__vacPv )
        vacCurrVal = self.__vacPv.get()
        vacAvgVal = numpy.mean(self.__vacHist)
        if vacCurrVal > self.__vacSpikeDelta + vacAvgVal:
            return False
            
        #    If the vacuum readout is a spike than don't add it to the
        # background average calculus
        else:
            self.__vacHist.append( vacCurrVal )
            if len(self.__vacHist) > self.__vacAvgSampCount:
                self.__vacHist.pop(0)
            return True
            
        return True
            
    def isDCOk(self):
        '''
        dcCurrVal = self.__m.getValue( self.__dcPv )
        dcAvgVal = numpy.mean(self.__dcHist)
        if dcCurrVal > self.__dcSpikeDelta + dcAvgVal:
            return False
        else:
            self.__dcHist.append( dcCurrVal )
            if len(self.__dcHist) > self.__dcAvgSampCount:
                self.__dcHist.pop(0)
            return True
        '''
        return True