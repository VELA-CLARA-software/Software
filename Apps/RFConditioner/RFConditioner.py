'''
TODO LLRFMonitor: Decide which traces are used for BD detection:
                        RF cavity reverse at the moment
TODO LLRFMonitor: CAVITY_PROBE for HRRG ?
TODO LLRFMonitor: HRRG implementation of the controller
                        HRRG will result in AttributeError: 'NoneType' object has no attribute 'startTraceMonitoring'
TODO LLRFMonitor: decide for which portion of the signals are the masks applied
                        At the moment for the whole of the trace
TODO LLRFMonitor: Testing

TODO GeneralMonitor: Add PVs for HRRG vacuum and DC, and their deltas etc...

TODO DataWriter

TODO KlystronMonitor

TODO RFProtectionMonitor
'''

'''
CTRLS: c.getKlyFwdPowerData()   c.getKlyFwdPower()
'''

# Set environmental variables needed for the C++ monitors
import os
os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_ADDR_LIST"] = "192.168.83.255"
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
import sys
sys.path.append("modules")
sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\Release\\')
#sys.path.append('c:\\prj\\test_area\\VELA_CLARA_PYDs\\bin\\Release\\')

import numpy
from GeneralMonitor import GeneralMonitor
from RFProtectionMonitor import RFProtectionMonitor
from DataWriter import DataWriter
from KlystronMonitor import KlystronMonitor
from LLRFMonitor import LLRFMonitor
from BDRollingAverage import BDRollingAverage

repRate = 10
bdRollingAvgT = 4 * 3600
bdNormalRate = 1e-4#1e-5
# Manually tuned value for LRRG with solenoid on with wobbler program.
# Wobbling the solenoid creates vacuum spikes when at +/-62A. Old value
# with no solenoid was 0.5e9
vacSpikeDelta = 1e-9
stepPow = 10e3
stopPow = 10.0e6
powIncreasePulses = 600

rfPower = 8.00e6

averagingPulses = bdRollingAvgT * repRate

bdRollAvg = BDRollingAverage(
    averagingPulses = averagingPulses,
    bdNormalRate = bdNormalRate)

genMon = GeneralMonitor(
    repRate,
    vacSpikeDelta = vacSpikeDelta,
    dcSpikeDelta = 0.2
)

# LRRG or HRRG
llrfMon = LLRFMonitor(beamline = "LRRG")

protMon = RFProtectionMonitor()
klyMon = KlystronMonitor()

inBreakdown = False
powIncreasePulseCounter = 0
pulsesSinceInBreakdown = 0

increasingRfPower = False
rfSetPoint = llrfMon.getRfSp()
rfSpHist = []

tracesHist = []

pulsesAfterBreakdown = 0

while True:

    llrfMon.waitForRfPulse()
    
    print 'New Pulse SP: {0:.0f}  pow rd: {1:.3f} MW  pow SP: {2:.2f} MW  BDR {3:.3e}  (target {4:.1e})  {5:.0f} until next step'.format(
        rfSetPoint, llrfMon.getKlyFwRfPower()/1e6, rfPower/1e6, bdRollAvg.getBdRate(), bdNormalRate,
        powIncreasePulses-powIncreasePulseCounter)
    # print "New Pulse SP: " + str(rfSetPoint) + "   pow rd: " + str(llrfMon.getKlyFwRfPower()/1e6) + "   pow SP: " + str(rfPower/1e6) + "   BDR " + str(bdRollAvg.getBdRate()) + " " + str(bdRollAvg.isBdRateExceeded()) + \
    #    " " + str(len(bdRollAvg.bdHist)) + " " + str(bdRollAvg.pulseCount)  +  " " + str(bdRollAvg.bdCount)
    #sys.stdout.write('.')
    
    # Check if parameters have normal values
    vacOk = genMon.isVacuumOk()
    dcOk = genMon.isDCOk()
    rfOk = llrfMon.isRfOk()
    klyOk = klyMon.isKlystronOk()
    protectionOk = protMon.isProtectionOk()
    
    writeDetailedData = False
    
    #TODO if kly not ok than reset the error
    #TODO if protection not ok than reset the error
    
    if not vacOk:
        print "vac"
    #if not dcOk:
    #    print "DC"
    if not rfOk:
        print "RF"
    if not klyOk:
        print "kly"
        
    # Breakdowns are detected on the vacuum, DC and RF
    #if vacOk and dcOk and rfOk and not inBreakdown:
    if vacOk and rfOk and not inBreakdown: # Test only
        bdRollAvg.addPulse(isBd = False)
        llrfMon.setRfMasks(llrfMon.getCavRevTrace())
        
        if increasingRfPower:
            if llrfMon.getKlyFwRfPower() < rfPower:
                rfSetPoint += 1
                llrfMon.setRfSp(rfSetPoint)
            else:
                rfSpHist.append(rfSetPoint)
                increasingRfPower = False
        
    else:
        if not inBreakdown:
            inBreakdown = True
            pulsesSinceInBreakdown = 1
            # RF OFF
            llrfMon.setRfSp(0)
            bdRollAvg.addPulse(isBd = True)
            if bdRollAvg.isBdRateExceeded():
                rfPower -= stepPow
                if len(rfSpHist) > 1:
                    del rfSpHist[-1]
                    rfSetPoint = rfSpHist[-1]
            writeDetailedData = True
            powIncreasePulseCounter = 1
        else:
            # Two seconds cooldown time
            if pulsesSinceInBreakdown < repRate * 2:
                pulsesSinceInBreakdown += 1
                
            # If after the cooldown time the vacuum didn't recover
            # or if Klystron isn't started
            elif not vacOk or not klyOk or not protectionOk:
                pulsesSinceInBreakdown += 1
                
            # RF ON
            else:
                inBreakdown = False
                pulsesAfterBreakdown = 2
                llrfMon.setRfSp(rfSetPoint)
                
    # Handle the RF Power increase
    if inBreakdown:
        increasingRfPower = False
    else:
        powIncreasePulseCounter += 1
        if powIncreasePulseCounter > powIncreasePulses:
            powIncreasePulseCounter = 1
            if not bdRollAvg.isBdRateExceeded():
                rfPower += stepPow
                increasingRfPower = True
                if rfPower >= stopPow:
                    rfPower = stopPow
                    increasingRfPower = False
                    
    # Keep the RF traces of the last three pulses in this variable
    # for using them in the detailed breakdown reporting
    tracesHist.append(llrfMon.getCavRevTrace())
    if (len(tracesHist)) > 3:
        tracesHist.pop(0)
    
    # 
    if (len(tracesHist)) < 3:
        llrfMon.enableRfMasks(False)
    else:
        llrfMon.enableRfMasks(not inBreakdown and (pulsesAfterBreakdown < 1))
        
    pulsesAfterBreakdown -= 1
    
    # For some reason first RF pulse after the breakdown is with 0 setpoint
    firstPulseAfterBreakdown = False
    
    # TODO: Write normal data
    
    # TODO: Write BD data if it is the case
    if writeDetailedData:
        x = 1
