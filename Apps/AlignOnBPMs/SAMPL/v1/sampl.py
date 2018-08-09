'''
This Class is the one User's are to initialize in there code.
You need to pass in your controllers, specifying which element of the
machine it is for
'''

from PyQt4.QtCore import QThread
import createBeam as cb
import createBeamline as cbl
import yaml
# import sys
import os

from epics import caget, caput
# sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\sourceCode\\')
# from sourceCode.SAMPLcore.SAMPLlab import PhysicalUnits


class Setup(QThread):
    # CONSTRUCTOR
    def __init__(self, V_MAG_Ctrl=None, C_S01_MAG_Ctrl=None,
                 C_S02_MAG_Ctrl=None, C2V_MAG_Ctrl=None, V_RF_Ctrl=None,
                 C_RF_Ctrl=None, L01_RF_Ctrl=None, messages=False):
        QThread.__init__(self)
        self.showMessages = messages
        self.V_MAG_Ctrl = V_MAG_Ctrl
        self.C_S01_MAG_Ctrl = C_S01_MAG_Ctrl
        self.C_S02_MAG_Ctrl = C_S02_MAG_Ctrl
        self.C2V_MAG_Ctrl = C2V_MAG_Ctrl
        self.V_RF_Ctrl = V_RF_Ctrl
        self.C_RF_Ctrl = C_RF_Ctrl
        self.L01_RF_Ctrl = L01_RF_Ctrl
        self.startElement = None
        self.stopElement = None
        self.initDistribFile = 'Null'
        self.initDistrib = None
        self.initCharge = 0.0

        stream = file(str(os.path.abspath(__file__)).split('sampl')[0] +
                      "VELA-CLARA.yaml", 'r')
        settings = yaml.load(stream)
        self.elements = settings['elements']
        self.groups = settings['groups']

    # DESTRUCTOR
    def __del__(self):
        self.wait()

    # Shell function to run AStra simulations in a thread is need.
    # Using this 'shell' function alows me to pass in agurments
    def go(self, startElement, stopElement, initDistrib, charge=0.25):
            self.startElement = startElement
            self.stopElement = stopElement
            self.initDistrib = initDistrib
            self.initCharge = charge  # in nC
            # Run in Thread
            self.start()

    # Main functions (has to be called run if I want to use in a thread)
    def run(self):
        print('------------------------------')
        print('-------------SAMPL------------')
        print('------NEW SIMULTAION RUN------')
        print('------------------------------')

        print('1. Create a beam ...')
        createBeam = cb.createBeam()
        if 'ini' in self.initDistribFile:
            self.initDistrib = createBeam.useASTRAFile(self.initDistribFile)
        else:
            print('Creating default beam.')
            xOffset = caget('VM-EBT-INJ-DIA-DUMMY-01:DDOUBLE8')
            yOffset = caget('VM-EBT-INJ-DIA-DUMMY-01:DDOUBLE9')
            self.initDistrib = createBeam.guassian(x=xOffset, y=yOffset)

        print('2. Create a beamline ...')
        selectedGroup = None

        for line in self.groups:
            hasStart = any(self.startElement in self.elements[s]['omName']
                           for s in self.groups[line])
            hasStop = any(self.stopElement in self.elements[s]['omName']
                          for s in self.groups[line])
            if (hasStart and hasStop):
                selectedGroup = self.groups[line]
                print '    Using group: ', line

        lineCreator = cbl.createBeamline(V_MAG_Ctrl=self.V_MAG_Ctrl,
                                         C_S01_MAG_Ctrl=self.C_S01_MAG_Ctrl,
                                         C_S02_MAG_Ctrl=self.C_S02_MAG_Ctrl,
                                         C2V_MAG_Ctrl=self.C2V_MAG_Ctrl,
                                         V_RF_Ctrl=self.V_RF_Ctrl,
                                         C_RF_Ctrl=self.C_RF_Ctrl,
                                         L01_RF_Ctrl=self.L01_RF_Ctrl)
        beamLine = lineCreator.create(selectedGroup, self.elements)

        # Run simulation
        for key, value in self.elements.iteritems():
            if value['omName'] == self.startElement:
                startName = key
            if value['omName'] == self.stopElement:
                stopName = key

        startIndex = [i for i, x in enumerate(beamLine.componentlist) if x.name == startName]
        stopIndex = [i for i, x in enumerate(beamLine.componentlist) if x.name == stopName]
        print('3. Running SAMPL simulation from ' +
              startName + ' to ' + stopName + '.')
        beamLine.TrackMatlab([startIndex[0], stopIndex[0]], self.initDistrib)

        # SAMPL to EPICS (look how short it is it is!!!!!!)
        # this take the most time to complete
        print('4. Writing data to EPICS ...')
        """CHANGED FOR NEW CAMER PVs"""
        for i in beamLine.componentlist:
            if beamLine.componentlist.index(i) >= startIndex[0] and beamLine.componentlist.index(i) <= stopIndex[0]:
                if 'SCR' in i.name or 'YAG' in i.name:
                    if 'CLu' in i.name:
                        caput('VM-' + self.elements[i.name]['camPV'] +
                              ':ANA:X_RBV', i.x)
                        caput('VM-' + self.elements[i.name]['camPV'] +
                              ':ANA:Y_RBV', i.y)
                        caput('VM-' + self.elements[i.name]['camPV'] +
                              ':ANA:SigmaX_RBV', i.xSigma)
                        caput('VM-' + self.elements[i.name]['camPV'] +
                              ':ANA:SigmaY_RBV', i.ySigma)
                    else:
                        caput('VM-' + self.elements[i.name]['camPV'] +
                              ':X', i.x)
                        caput('VM-' + self.elements[i.name]['camPV'] +
                              ':Y', i.y)
                        caput('VM-' + self.elements[i.name]['camPV'] +
                              ':SigmaX', i.xSigma)
                        caput('VM-' + self.elements[i.name]['camPV'] +
                              ':SigmaY', i.ySigma)
                    print '    Written data for ', self.elements[i.name]['omName']
                if 'BPM'in i.name:
                    caput('VM-' + self.elements[i.name]['pv'] + ':X', i.x)
                    caput('VM-' + self.elements[i.name]['pv'] + ':Y', i.y)
                    print '    Written data for ', self.elements[i.name]['omName']
                    print 'x Value:' , str(i.x)
