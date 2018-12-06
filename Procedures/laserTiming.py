import sys, time, os
sys.path.append('../../')
from Software.Widgets.generic.pv import *
sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\Release')

def loadBPMs():
    global bpm
    global bpmInit
    global bpmstatus
    import VELA_CLARA_BPM_Control as bpm
    from VELA_CLARA_BPM_Control import BPM_STATUS
    bpmstatus = BPM_STATUS
    bpmInit = bpm.init()
    bpmInit.setQuiet()
    bpm = bpmInit.physical_C2B_BPM_Controller()


class emitter(object):

    def __init__(self, signal=None):
        super(emitter, self).__init__()
        self.signal = signal

    def emit(self, *args, **kwargs):
        if self.signal == 'print':
            print args
        else:
            if self.signal is not None:
                self.signal.emit(*args, **kwargs)
        return


class LaserTiming(object):
    pvNameLaser = 'CLA-C17-TIM-EVR-01:FrontUnivOut4-Ena-SP'
    pvSetNumberPulses = 'CLA-ACC-TIM-BRST-01:Burst-Count-SP'
    pvStartBurstStart = 'CLA-ACC-TIM-BRST-01:Burst-Start-SP'
    pvSetBurstMode = 'CLA-ACC-TIM-BRST-01:Burst-Mode-SP'
    pvNameDetect = 'CLA-S01-DIA-BPM-01:RDY'
    pvWCMQName = 'CLA-S01-DIA-WCM-01:Q'
    pvFCUPQName = 'CLA-S02-DIA-FCUP-01:Q'
    pvUsefulNames = 'AllowLaser'
    nominalTiming = 1

    def __init__(self, bpms=False):
        super(LaserTiming, self).__init__()
        self.app = None
        self.pvLaser = PVObject(self.pvNameLaser)
        self.pvNumberPulses = PVObject(self.pvSetNumberPulses)
        self.pvBurstMode = PVObject(self.pvSetBurstMode)
        self.pvBurstStart = PVObject(self.pvStartBurstStart)
        self.pvDetect = PVObject(self.pvNameDetect)
        self.pvWCMQ = PVObject(self.pvWCMQName)
        self.pvFCUPQ = PVObject(self.pvFCUPQName)
        setattr(self.pvLaser, 'writeAccess', True)
        setattr(self.pvNumberPulses, 'writeAccess', True)
        setattr(self.pvBurstMode, 'writeAccess', True)
        setattr(self.pvBurstStart, 'writeAccess', True)
        if bpms:
            loadBPMs()
            self.bpms = bpm
        self.bpmDataObjects = {}
        self.logger = emitter('print')
        return

    def turnOnLaserGating(self):
        setattr(self.pvLaser, 'value', 1)
        return self.pvLaser.value

    def turnOffLaserGating(self):
        setattr(self.pvLaser, 'value', 0)
        return self.pvLaser.value

    def turnOnLaser(self):
        self.turnOnLaserGating()
        return setattr(self.pvBurstMode, 'value', 0)

    def turnOffLaser(self):
        self.turnOffLaserGating()
        return setattr(self.pvBurstMode, 'value', 1)

    def isLaserOn(self):
        return self.pvLaser.value

    def pulses(self):
        return self.pvNumberPulses.value

    def setNumberPulses(self, n=1):
        return setattr(self.pvNumberPulses, 'value', n)

    def startBurst(self):
        setattr(self.pvBurstStart, 'value', 1)
        setattr(self.pvBurstStart, 'value', 0)

    def getWCMCharge(self):
        return self.pvWCMQ.value - 5

    def getFCUPCharge(self):
        return self.pvFCUPQ.value

    def getBPMDataObject(self, bpm):
        if bpm not in self.bpmDataObjects:
            self.bpmDataObjects[bpm] = self.bpms.getBPMDataObject(bpm)
        return self.bpmDataObjects[bpm]

    def getBPM03Charge(self):
        obj = self.getBPMDataObject('S02-BPM02')
        return obj.q

    def getTimeStr(self):
        return time.strftime('%H%M%S')

    def getWorkFolder(self):
        return '\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Work\\' + time.strftime('%Y\\%m\\%d') + '\\'

    def getFileName(self, q=None, n=None, pos=None, energy=None, comment=None):
        filename = self.getWorkFolder() + self.getTimeStr() + '_VHEE_'
        filename = filename + '_' + str(q) + 'pC' if q is not None else filename
        filename = filename + '_' + str(n) + '_Shots' if n is not None else filename
        filename = filename + '_' + str(pos) + 'mm' if pos is not None else filename
        filename = filename + '_' + str(energy) + 'MeV' if energy is not None else filename
        filename = filename + '_' + str(comment) if comment is not None else filename
        filename = filename + '.txt'
        return filename

    def printer(self, *args):
        outstr = ''
        for a in args:
            outstr += str(a) + ' '

        return outstr

    def turnOnForIntegratedCharge(self, q=2500, pos=None, energy=None, comment=None):
        self.abort = False
        while not self.isLaserOn() == 1:
            self.turnOnLaserGating()

        time.sleep(0.075)
        filename = self.getFileName(q=q, n=None, pos=pos, energy=energy, comment=comment)
        file = open(filename, 'w')
        sys.stdout = file
        print 'count, intWCMQ, intFCUPQ, intBPMQ'
        sys.stdout = sys.__stdout__
        count = 0
        intWCMQ = 0
        intFCUPQ = 0
        intBPMQ = 0
        WCMlastvalue = BPMlastvalue = 0
        self.detectToggle = self.pvDetect.value
        while intWCMQ < q - 5 and not self.abort:
            if not self.pvDetect.value == self.detectToggle:
                time.sleep(0.075)
                self.detectToggle = self.pvDetect.value
                count += 1
                WCMvalue = self.getWCMCharge()
                BPMvalue = self.getBPM03Charge()
                intWCMQ += WCMvalue
                intFCUPQ += self.getFCUPCharge()
                intBPMQ += BPMvalue
                sys.stdout = file
                print count, intWCMQ, intFCUPQ, intBPMQ
                sys.stdout = sys.__stdout__
                self.logger.emit(self.printer('Shot ', count, intWCMQ, intFCUPQ, intBPMQ, WCMvalue - WCMlastvalue, BPMvalue - BPMlastvalue))
                WCMlastvalue = WCMvalue
                BPMlastvalue = BPMvalue
            elif self.app is not None:
                self.app.processEvents()

        self.turnOffLaserGating()
        return count

    def turnOnForNPulse(self, n=1, pos=None, energy=None, comment=None):
        self.abort = False
        while not self.isLaserOn() == 1:
            self.turnOnLaserGating()

        time.sleep(0.075)
        filename = self.getFileName(q=None, n=n, pos=pos, energy=energy, comment=comment)
        file = open(filename, 'w')
        sys.stdout = file
        print 'count, intWCMQ, intFCUPQ, intBPMQ'
        sys.stdout = sys.__stdout__
        count = 0
        intWCMQ = 0
        intFCUPQ = 0
        intBPMQ = 0
        WCMlastvalue = BPMlastvalue = 0
        self.detectToggle = self.pvDetect.value
        while count < n and not self.abort:
            if not self.pvDetect.value == self.detectToggle:
                time.sleep(0.075)
                self.detectToggle = self.pvDetect.value
                count += 1
                WCMvalue = self.getWCMCharge()
                BPMvalue = self.getBPM03Charge()
                intWCMQ += WCMvalue
                intFCUPQ += self.getFCUPCharge()
                intBPMQ += BPMvalue
                sys.stdout = file
                print count, intWCMQ, intFCUPQ, intBPMQ
                sys.stdout = sys.__stdout__
                self.logger.emit(self.printer('Shot ', count, intWCMQ, intFCUPQ, intBPMQ, WCMvalue - WCMlastvalue, BPMvalue - BPMlastvalue))
                WCMlastvalue = WCMvalue
                BPMlastvalue = BPMvalue
            elif self.app is not None:
                self.app.processEvents()

        self.turnOffLaserGating()
        return count

    def setBurst(self, n=10):
        count = 0
        intQ = 0
        print 'turning off laser'
        print self.turnOffLaser()
        time.sleep(2)
        print 'setting number of pulses'
        self.setNumberPulses(n)
        print 'starting burst'
        self.startBurst()
        self.detectToggle = self.pvDetect.value
        while count < n:
            if not self.pvDetect.value == self.detectToggle:
                self.detectToggle = self.pvDetect.value
                count += 1
                intQ += self.getWCMCharge()
                self.logger.emit(self.printer(count, intQ))
            else:
                time.sleep(0.02)

        return count
        
