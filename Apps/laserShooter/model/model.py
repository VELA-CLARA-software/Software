# from PyQt4.QtCore import QThread, QObject, pyqtSignal, QTimer
import sys,os
import time
from functools import partial
sys.path.append("../../../")
import Software.Procedures.laserTiming as lt

class emitter(object):

    def __init__(self, signal=None):
        super(emitter, self).__init__()
        self.signal = signal

    def emit(self, *args, **kwargs):
        if self.signal is not None:
            self.signal.emit(*args, **kwargs)

class machineSetter(object):
    def __init__(self, machine):
        super(machineSetter, self).__init__()
        self.machine = machine

    def set(self, function, *args, **kwargs):
        getattr(self.machine,function)(*args, **kwargs)

    def get(self, function, *args, **kwargs):
        return getattr(self.machine,function)(*args, **kwargs)

    def __getattr__(self, attr):
        return getattr(self.machine, attr)

class Model(object):

    def __init__(self, machineType, lineType, gunType, verbose=True):
        super(Model, self).__init__()
        # self.baseMachine = machine.Machine(machineType, lineType, gunType)
        self._abort = False
        self.verbose = verbose
        # self.machine = machineSetter(self.baseMachine)
        self.machineType = machineType
        self.lineType = lineType
        self.gunType = gunType
        self.logger = emitter()
        self.laser = lt.LaserTiming(bpms=True)

        print("Model Initialized")


########### findRFCentreBLM ###############

    def findRFCentreBLM(self, scale=1):
        """
            The suggested solution (from BLM) is to scan c1 at five points in x/y at
            [[0,0], [-1,0], [1,0], [0, -1], [0,1]]
            at two energies and then solve for the zero point in x/y corrector space.
            Repeat for c2.

            Data is stored in self.experimentalData[self.main][self.sub]

            I haven't figured out how to do the fit yet...
        """
        cx = self.corrector1X
        cy = self.corrector1Y
        self.doBMLScan(cx, cy, scale, 1)

        cx = self.corrector2X
        cy = self.corrector2Y
        self.doBMLScan(cx, cy, scale, 2)

    def doBMLScan(self, corrx, corry, scale=1, no=1):
        self.machine.setLinac1Amplitude(self.linacLowerAmp)
        # self.main = 'Corr1'
        self.sub = 'Low'
        self.resetDataArray()
        for c1x, c1y in [[0,0], [-1,0], [1,0], [0, -1], [0,1]]:
            self.machine.setCorr(corrx, scale*c1x)
            self.machine.setCorr(corry, scale*c1y)
            time.sleep(self.sleepTime)
            data = self.getData()
            self.setDataArray(c1x, c1y, data)
        if self.verbose:
            self.saveLinacDataBLM(corr=no)

        self.machine.setLinac1Amplitude(self.linacUpperAmp)
        # self.main = 'Corr1'
        self.sub = 'High'
        self.resetDataArray()
        for c1x, c1y in [[0,0], [-1,0], [1,0], [0, -1], [0,1]]:
            self.machine.setCorr(corrx, scale*c1x)
            self.machine.setCorr(corry, scale*c1y)
            time.sleep(self.sleepTime)
            data = self.getData()
            self.setDataArray(c1x, c1y, data)
        if self.verbose:
            self.saveLinacDataBLM(corr=no)

    def saveLinacDataBLM(self, corr=1):
        self.timestr = time.strftime("%Y%m%d-%H%M%S")
        c1, c2, bpms = self.getDataArray(zipped=False)
        rawData = np.array(zip(c1, c2, *zip(*bpms)))
        labels = ['BPM'+str(i+1) for i in range(len(bpms[1]))]
        df = pd.DataFrame(rawData)
        df.columns = ['cx', 'cy'] + labels
        df.to_csv(self.timestr+'_LinacCentring_'+self.main+'_'+self.sub+'_'+str(self.linacLowerAmp)+'_'+str(self.linacUpperAmp)+'_Corr_'+str(corr)+'_rawDataBLM.csv', index=0)

########### findRFCentre ###############

    def findRFCentre(self):
        """
            This function will scan corrector 1 (c1) to minimise the average difference between the BPM readings
            at high and low amplitude of the linac RF. This is simply the mean value of the differences.
            Once found for c1, it does the same for corrector 2 (c2).
            Currently this function only works in one plane at a time.

            Data is stored in self.experimentalData[self.main][self.sub]
        """
        self.resetDataArray()
        for c1 in np.arange(self.corrector1Min, self.corrector1Max+self.correctorStepSize, self.correctorStepSize):
            self.machine.setCorr(self.corrector1, c1)
            self.machine.setCorr(self.corrector2, 0)
            self.machine.setLinac1Amplitude(self.linacLowerAmp)
            time.sleep(self.sleepTime)
            dataLow = self.getData()
            self.machine.setLinac1Amplitude(self.linacUpperAmp)
            time.sleep(self.sleepTime)
            dataHigh = self.getData()
            self.setDataArray(c1, 0, dataLow - dataHigh)
        c1Min = self.findC1Min()
        print 'c1Min = ', c1Min
        self.resetDataArray()
        for c2 in np.arange(self.corrector2Min, self.corrector2Max+self.correctorStepSize, self.correctorStepSize):
            self.machine.setCorr(self.corrector1, c1Min)
            self.machine.setCorr(self.corrector2, c2)
            self.machine.setLinac1Amplitude(self.linacLowerAmp)
            time.sleep(self.sleepTime)
            dataLow = self.getData()
            self.machine.setLinac1Amplitude(self.linacUpperAmp)
            time.sleep(self.sleepTime)
            dataHigh = self.getData()
            self.setDataArray(c1Min, c2, dataLow - dataHigh)
        c2Min = self.findC2Min()
        print 'c2Min = ', c2Min
        self.machine.setCorr(self.corrector1, c1Min)
        self.machine.setCorr(self.corrector2, c2Min)

    def findC1Min(self):
        self.timestr = time.strftime("%Y%m%d-%H%M%S")
        c1, c2, bpms = self.getDataArray(zipped=False)
        # This is the mean of the BPMs for each value of corrector
        BPMMean = [np.mean(b) for b in bpms]
        index = BPMMean.index(min(BPMMean))
        if self.verbose:
            self.saveLinacData(1)
        return c1[index]

    def findC2Min(self):
        c1, c2, bpms = self.getDataArray(zipped=False)
        # This is the mean of the BPMs for each value of corrector
        BPMMean = [np.mean(b) for b in bpms]
        index = BPMMean.index(min(BPMMean))
        if self.verbose:
            self.saveLinacData(2)
        return c2[index]

    def saveLinacData(self, corr=1):
        self.timestr = time.strftime("%Y%m%d-%H%M%S")
        c1, c2, bpms = self.getDataArray(zipped=False)
        rawData = np.array(zip(c1, c2, *zip(*bpms)))
        labels = ['BPM'+str(i+1) for i in range(len(bpms[1]))]
        df = pd.DataFrame(rawData)
        df.columns = ['c1', 'c2'] + labels
        df.to_csv(self.timestr+'_LinacCentring_'+self.main+'_'+self.plane+'_'+str(self.linacLowerAmp)+'_'+str(self.linacUpperAmp)+'_Corr_'+str(corr)+'_rawData.csv', index=0)

########### findRFCentre2D ###############

    def findRFCentre2D(self):
        """
            This function will scan corrector 1 (c1) to minimise the average difference between the BPM readings
            at high and low amplitude of the linac RF. This is simply the mean value of the differences.
            Once found for c1, it does the same for corrector 2 (c2).
            Currently this function only works in one plane at a time.

            Data is stored in self.experimentalData[self.main][self.sub]
        """
        self.timestr = time.strftime("%Y%m%d-%H%M%S")
        with open(self.timestr+'_LinacCentring_'+self.main+'_'+self.plane+'_'+str(self.linacLowerAmp)+'A_'+str(self.linacUpperAmp)+'A_rawData_log.csv', 'w') as logfile:
            self.resetDataArray()
            self.data1 = {}
            self.data2 = {}
            self.rawData = OrderedDict({'x':[], 'y': [], 'z1':[], 'z2': [], 'diff': []})
            self.machine.setLinac1Amplitude(self.linacLowerAmp)
            flip = -1
            c1list = np.arange(self.corrector1Min, self.corrector1Max+self.correctorStepSize, self.correctorStepSize)
            c2list = np.arange(self.corrector2Min, (self.corrector2Max+self.correctorStepSize), self.correctorStepSize)

            for c1 in c1list:
                self.machine.setCorr(self.corrector1, c1)
                self.data1[c1] = {}
                flip = -1*flip
                for i, b in enumerate(c2list):
                    if flip < 1:
                        c2 = c2list[::-1][i]
                    else:
                        c2 = c2list[i]
                    self.machine.setCorr(self.corrector2, c2)
                    while abs(self.machine.getCorr(self.corrector1) - c1) > 0.05 or abs(self.machine.getCorr(self.corrector2) - c2) > 0.05:
                        # print self.machine.get('getCorr', self.corrector1) , c1, self.machine.get('getCorr', self.corrector2) , c2
                        time.sleep(self.sleepTime)
                    if self._abort:
                        self._abort = False
                        return 0
                    print 'linac = ', self.linacLowerAmp, '  c1 = ', c1, '  c2 = ', c2
                    data1 = self.getData()[:,0]
                    print 'data1 = ', data1
                    if self.verbose:
                        logfile.write('data1,'+str(self.linacLowerAmp)+','+str(c1)+','+str(c2)+','+str(data1))
                    self.data1[c1][c2] = data1

            self.machine.setLinac1Amplitude(self.linacUpperAmp)
            flip = -1
            for c1 in c1list:
                self.machine.setCorr(self.corrector1, c1)
                self.data2[c1] = {}
                flip = -1*flip
                for i, b in enumerate(c2list):
                    if flip < 1:
                        c2 = c2list[::-1][i]
                    else:
                        c2 = c2list[i]
                    self.machine.setCorr(self.corrector2, c2)
                    while abs(self.machine.getCorr(self.corrector1) - c1) > 0.05 or abs(self.machine.getCorr(self.corrector2) - c2) > 0.05:
                        time.sleep(self.sleepTime)
                    print 'linac = ', self.linacUpperAmp, '  c1 = ', c1, '  c2 = ', c2
                    data2 = self.getData()[:,0]
                    print 'data2 = ', data2
                    if self.verbose:
                        logfile.write('data2,'+str(self.linacUpperAmp)+','+str(c1)+','+str(c2)+','+str(data2))
                    self.data2[c1][c2] = data2

            flip = -1
            for c1 in c1list:
                flip = -1*flip
                for i, b in enumerate(c2list):
                    if flip < 1:
                        c2 = c2list[::-1][i]
                    else:
                        c2 = c2list[i]
                    self.rawData['x'].append(c1)
                    self.rawData['y'].append(c2)
                    data1 = self.data1[c1][c2]
                    data2 = self.data2[c1][c2]
                    self.rawData['z1'].append(data1)
                    self.rawData['z2'].append(data2)
                    # diff = np.mean(np.array([abs(a[1] - a[0]) if a[0] < 20 and a[1] < 20 else 20 for a in zip(data1,data2)]))
                    # print data1, data2
                    diff = np.array([(a-b)**2 for a,b in zip(data2, data1)])
                    if any(np.isnan(a) for a in diff):# or np.isnan(data1) or np.isnan(data2):
                        diff = 100
                    # print 'diff = ', diff
                    self.rawData['diff'].append(diff)
                    if self.verbose:
                        logfile.write('diff,'+str(self.linacUpperAmp)+','+str(c1)+','+str(c2)+','+str(data1)+','+str(data2)+','+str(diff))
                    self.setDataArray(c1, c2, diff)
        if self.verbose:
            try:
                self.saveLinacData2D()
            except:
                pass
        self.doFitRFCentre2D()

    def doFitRFCentre2D(self):
        c1, c2, diff = self.getDataArray(zipped=False)
        diff = [np.mean(a) for a in diff]
        data = zip(c1, c2, diff)
        print data
        val, idx = max((val, idx) for (idx, val) in enumerate(diff))
        print 'max parameters ['+"{0:.2f}".format(diff[idx])+']: ' + self.corrector1 + ' = ' + str(c1[idx]) + 'A   ' + self.corrector2 + ' = ' + str(c2[idx]) + 'A'
        val, idx = min((val, idx) for (idx, val) in enumerate(diff))
        printstr = 'min parameters [' + "{0:.2f}".format(diff[idx]) +']: ' + self.corrector1 + ' = ' + str(c1[idx]) + 'A   ' + self.corrector2 + ' = ' + str(c2[idx]) + 'A'
        self.logger.emit(printstr)
        print printstr
        self.corrector1Fit[self.plane] = c1[idx]
        self.corrector2Fit[self.plane] = c2[idx]

    def setRFCentreFit(self):
        if hasattr(self, 'corrector1Fit') and hasattr(self, 'corrector2Fit'):
            if self.plane in self.corrector1Fit and self.plane in self.corrector2Fit:
                self.machine.setCorr(self.corrector1, self.corrector1Fit[self.plane])
                self.machine.setCorr(self.corrector2, self.corrector2Fit[self.plane])
                while abs(self.machine.getCorr(self.corrector1) - self.corrector1Fit[self.plane]) > 0.05 or abs(self.machine.getCorr(self.corrector2) - self.corrector2Fit[self.plane]) > 0.05:
                    time.sleep(self.sleepTime)

    def saveLinacData2D(self):
        df = pd.DataFrame(self.rawData)
        df.columns = ['x', 'y', 'z1', 'z2', 'diff']
        filename = self.timestr+'_LinacCentring_'+self.main+'_'+self.plane+'_'+str(self.linacLowerAmp)+'_'+str(self.linacUpperAmp)+'_rawData'
        df.to_csv(filename+'.csv', index=0)
        # save_dict_to_hdf5(self.rawData, filename+'.h5')

########### findSOLCentre ###############

    def findSOLCentre(self):
        self.timestr = time.strftime("%Y%m%d-%H%M%S")
        with open(self.timestr+'_SOLCentring_'+self.main+'_'+self.plane+'_'+str(self.solLowerAmp)+'A_'+str(self.solUpperAmp)+'A_rawData_log.csv', 'w') as logfile:
            self.resetDataArray()
            self.data1 = {}
            self.data2 = {}
            self.rawData = {'x':[], 'y': [], 'z1':[], 'z2': []}
            self.machine.setSol(self.main, self.solLowerAmp)
            while abs(self.machine.getSol(self.main) - self.solLowerAmp) > 0.2:
                print 'wait'
                time.sleep(self.sleepTime)
            flip = -1
            for c1 in np.arange(self.corrector1Min, self.corrector1Max+self.correctorStepSize, self.correctorStepSize):
                self.machine.setCorr(self.corrector1, c1)
                self.data1[c1] = {}
                flip = -1*flip
                for c2 in np.arange(flip*self.corrector2Min, flip*(self.corrector2Max+self.correctorStepSize), flip*self.correctorStepSize):
                    self.machine.setCorr(self.corrector2, c2)
                    while abs(self.machine.getCorr(self.corrector1) - c1) > 0.05 or abs(self.machine.getCorr(self.corrector2) - c2) > 0.05:
                        print '0'
                        # print self.machine.get('getCorr', self.corrector1) , c1, self.machine.get('getCorr', self.corrector2) , c2
                        time.sleep(self.sleepTime)
                    if self._abort:
                        self._abort = False
                        return 0
                    print 'sol = ', self.solLowerAmp, '  c1 = ', c1, '  c2 = ', c2
                    data1 = self.getData()
                    if self.verbose:
                        logfile.write('data1,'+str(self.solLowerAmp)+','+str(c1)+','+str(c2)+','+str(data1))
                    self.data1[c1][c2] = data1

            self.machine.setSol(self.main, self.solUpperAmp)
            while abs(self.machine.getSol(self.main) - self.solUpperAmp) > 0.2:
                print 'wait2'
                time.sleep(0.1)
            flip = -1
            for c1 in np.arange(self.corrector1Min, self.corrector1Max+self.correctorStepSize, self.correctorStepSize):
                self.machine.setCorr(self.corrector1, c1)
                self.data2[c1] = {}
                flip = -1*flip
                for c2 in np.arange(flip*self.corrector2Min, flip*(self.corrector2Max+self.correctorStepSize), flip*self.correctorStepSize):
                    self.machine.setCorr(self.corrector2, c2)
                    while abs(self.machine.getCorr(self.corrector1) - c1) > 0.05 or abs(self.machine.getCorr(self.corrector2) - c2) > 0.05:
                        print '1'
                        time.sleep(self.sleepTime)
                    print 'sol = ', self.solUpperAmp, '  c1 = ', c1, '  c2 = ', c2
                    data2 = self.getData()
                    if self.verbose:
                        logfile.write('data2,'+str(self.solLowerAmp)+','+str(c1)+','+str(c2)+','+str(data2))
                    self.data2[c1][c2] = data2

            self.machine.setSol(self.main, 0)
            while abs(self.machine.getSol(self.main) - 0) > 0.2:
                time.sleep(0.1)

            flip = -1
            for c1 in np.arange(self.corrector1Min, self.corrector1Max+self.correctorStepSize, self.correctorStepSize):
                flip = -1*flip
                for c2 in np.arange(flip*self.corrector2Min, flip*(self.corrector2Max+self.correctorStepSize), flip*self.correctorStepSize):
                    self.rawData['x'].append(c1)
                    self.rawData['y'].append(c2)
                    data1 = self.data1[c1][c2]
                    data2 = self.data2[c1][c2]
                    self.rawData['z1'].append(data1)
                    self.rawData['z2'].append(data2)
                    diff = np.mean(np.array([abs(a[1] - a[0]) if a[0] < 20 and a[1] < 20 else 20 for a in zip(data1,data2)]))
                    if self.verbose:
                        logfile.write('diff,'+str(self.solLowerAmp)+','+str(c1)+','+str(c2)+','+str(data1)+','+str(data2)+','+str(diff))
                    self.setDataArray(c1, c2, diff)
        if self.verbose:
            self.saveSOLData()
        # self.doFitRFCentre()

    def saveSOLData(self):
        df = pd.DataFrame(self.rawData)
        df.columns = ['x', 'y', 'z1','z2']
        df.to_csv(self.timestr+'_SOLCentring_'+self.main+'_'+self.plane+'_'+str(self.solLowerAmp)+'A_'+str(self.solUpperAmp)+'A_rawData.csv', index=0)

    def cutDataRFCentre(self):
        """Return all data where the charge is >= 25% of the maximum and is at least 10pC"""
        allData = self.getDataArray()
        max_charge = max(self.getDataArray('yData'))

        cutData = [a for a in allData if a[1] > max_charge / 4 and a[1] > 10 and a[2] < 2]
        return cutData

    def doFitRFCentre(self):
        if max(x) - min(x) > 90:
            x = [a if a >= 0 else a+360 for a in x]
        crest_phase = (x[-1] + x[0]) / 2.0
        if crest_phase > 180:
            crest_phase -= 360
        x = [a if a <= 180 else a-360 for a in x]
        self.setFitArray(np.array(x), np.array(y))
        self.setFinalPhase(crest_phase)
        self.printFinalPhase()