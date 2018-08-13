from PyQt4.QtCore import QThread
import createBeam_noprint as cb
import createBeamline_noprint as cbl
import yaml
import os
from epics import caget, caput
# from sourceCode.SAMPLcore.SAMPLlab import PhysicalUnits
'''Assumes  you have the a OnlineModel in you path directory'''
from SimulationFramework import Framework


class Setup(QThread):
    # CONSTRUCTOR
    def __init__(self, V_MAG_Ctrl=None, C_S01_MAG_Ctrl=None,
                 C_S02_MAG_Ctrl=None, C2V_MAG_Ctrl=None, LRRG_RF_Ctrl=None,
                 HRRG_RF_Ctrl=None, L01_RF_Ctrl=None, messages=False):
        QThread.__init__(self)
        self.showMessages = messages
        self.V_MAG_Ctrl = V_MAG_Ctrl
        self.C_S01_MAG_Ctrl = C_S01_MAG_Ctrl
        self.C_S02_MAG_Ctrl = C_S02_MAG_Ctrl
        self.C2V_MAG_Ctrl = C2V_MAG_Ctrl
        self.HRRG_RF_Ctrl = HRRG_RF_Ctrl
        self.LRRG_RF_Ctrl = LRRG_RF_Ctrl
        self.L01_RF_Ctrl = L01_RF_Ctrl
        self.startElement = None
        self.stopElement = None
        self.initDistribFile = 'Null'
        self.initDistrib = None
        self.initCharge = 0.0
        self.pathway = Framework.Framework(subdir='.', overwrite='overwrite')

    # DESTRUCTOR
    def __del__(self):
        self.wait()

    def loadPathway(self):
        ans = False
        stream = file(str(os.path.abspath(__file__)).split('sampl')[0] +
                      "\\..\\..\\MasterLattice\\Lattices\\allPathways.yaml", 'r')
        settings = yaml.load(stream)
        for path in settings['pathways']:
            # print path
            self.pathway.loadSettings(filename='\\Lattices\\' + path)
            hasStart = False
            hasStop = False
            # print self.pathway.elements.keys()
            for element in self.pathway.elements.keys():
                #print element
                if element == self.startElement:
                    #print('found start')
                    hasStart = True
                if element == self.stopElement:
                    #print ('found stop')
                    hasStop = True
            if (hasStart and hasStop):
                ans = True
                #print '    Loaded pathway: ', path
                return ans
        #print '    Could not find a pathway...'
        #print '    Exiting ...'
        return ans

    def go(self, startElement, stopElement, initDistribFile, charge=0.25):
            self.startElement = startElement
            self.stopElement = stopElement
            self.initDistribFile = initDistribFile
            #self.initCharge = charge  # in nC
            # Run in Thread
            self.start()

    def run(self):
        print 'Start SAMPL run'
        #print('------------------------------')
        #print('-------------SAMPL------------')
        #print('------NEW SIMULATION RUN------')
        #print('------------------------------')

        #print('1. Create a beam ...')
        createBeam = cb.createBeam()
        if 'ini' in self.initDistribFile:
            self.initDistrib = createBeam.useASTRAFile(self.initDistribFile)
        else:
            #print('    Creating default beam.')
            xOffset = caget('VM-EBT-INJ-DIA-DUMMY-01:DDOUBLE8')
            yOffset = caget('VM-EBT-INJ-DIA-DUMMY-01:DDOUBLE9')
            self.initDistrib = createBeam.guassian(x=xOffset, y=yOffset)

        #print('2. Create a beamline ...')
        self.loadPathway()
        #print('    Crop pathway for SAMPL run...')
        startIndex = self.pathway.elementIndex(self.startElement)
        stopIndex = self.pathway.elementIndex(self.stopElement)
        for section in self.pathway.fileSettings.keys():
            startOfSection = self.pathway.fileSettings[section]['output']['start_element']
            stopOfSection = self.pathway.fileSettings[section]['output']['end_element']
            sectionStartIndex = self.pathway.elementIndex(startOfSection)
            sectionStopIndex = self.pathway.elementIndex(stopOfSection)
            [nameEndSection, dataEndSection] = self.pathway.getElementAt(sectionStopIndex)
            elementsToBeRemoved = []

            for i in range(sectionStartIndex, sectionStopIndex):
                # print name
                [name, data] = self.pathway.getElementAt(i)
                if dataEndSection['position_start'][-1] < data['position_start'][-1]:
                    #print '      Deleting element', name
                    elementsToBeRemoved.append(name)

            for name in elementsToBeRemoved:
                self.pathway.deleteElement(name)

            sectionStartIndex = self.pathway.elementIndex(startOfSection)
            sectionStopIndex = self.pathway.elementIndex(stopOfSection)
            startIndex = self.pathway.elementIndex(self.startElement)
            stopIndex = self.pathway.elementIndex(self.stopElement)
            if startIndex > sectionStartIndex and startIndex > sectionStopIndex:
                #print '      Deleting section', section
                del self.pathway.fileSettings[section]
            if startIndex > sectionStartIndex and startIndex < sectionStopIndex:
                #print '      Make start element the start of section', section
                self.pathway.fileSettings[section]['output']['start_element'] = self.startElement
            if stopIndex > sectionStartIndex and stopIndex < sectionStopIndex:
                #print '      Make stop element the stop of section', section
                self.pathway.fileSettings[section]['output']['end_element'] = self.stopElement
            if stopIndex < sectionStartIndex and stopIndex < sectionStopIndex:
                #print '      Deleting section', section
                del self.pathway.fileSettings[section]
        lineCreator = cbl.createBeamline(V_MAG_Ctrl=self.V_MAG_Ctrl,
                                         C_S01_MAG_Ctrl=self.C_S01_MAG_Ctrl,
                                         C_S02_MAG_Ctrl=self.C_S02_MAG_Ctrl,
                                         C2V_MAG_Ctrl=self.C2V_MAG_Ctrl,
                                         HRRG_RF_Ctrl=self.HRRG_RF_Ctrl,
                                         LRRG_RF_Ctrl=self.LRRG_RF_Ctrl,
                                         L01_RF_Ctrl=self.L01_RF_Ctrl)
        beamLine = lineCreator.create(self.pathway, self.startElement, self.stopElement)
        # Run simulation
        for element in self.pathway.elements.keys():
            if element == self.startElement:
                startName = element
            if element == self.stopElement:
                stopName = element

        #print('3. Running SAMPL simulation from ' +
        #      startName + ' to ' + stopName + '.')
        numberOfElements = len(beamLine.componentlist)
        beamLine.TrackMatlab([0, numberOfElements - 1], self.initDistrib)

        # SAMPL to EPICS (look how short it is it is!!!!!!)
        # this take the most time to complete
        #print('4. Writing data to EPICS ...')
        """CHANGED FOR NEW CAMER PVs"""
        for i in beamLine.componentlist:
            if beamLine.componentlist.index(i) >= 0 and beamLine.componentlist.index(i) <= numberOfElements - 1:
                if 'SCR' in i.name or 'YAG' in i.name:
                    #if 'CLA' in i.name:
                    caput('VM-' + self.pathway.elements[i.name]['camera_PV'] +
                          ':ANA:X_RBV', i.x)
                    caput('VM-' + self.pathway.elements[i.name]['camera_PV'] +
                          ':ANA:Y_RBV', i.y)
                    caput('VM-' + self.pathway.elements[i.name]['camera_PV'] +
                          ':ANA:SigmaX_RBV', i.xSigma)
                    caput('VM-' + self.pathway.elements[i.name]['camera_PV'] +
                          ':ANA:SigmaY_RBV', i.ySigma)
                #    else:
                #        caput('VM-' + self.pathway.elements[i.name]['camera_PV'] +
                #              ':X', i.x)
                #        caput('VM-' + self.pathway.elements[i.name]['camera_PV'] +
                #              ':Y', i.y)
                #        caput('VM-' + self.pathway.elements[i.name]['camera_PV'] +
                #              ':SigmaX', i.xSigma)
                #        caput('VM-' + self.pathway.elements[i.name]['camera_PV'] +
                #              ':SigmaY', i.ySigma)
                    #print '    Written data for ', i.name
                if 'BPM'in i.name:
                    caput('VM-' + self.pathway.elements[i.name]['PV'] + ':X', i.x)
                    caput('VM-' + self.pathway.elements[i.name]['PV'] + ':Y', i.y)
                    #print '    Written data for ', i.name
                    # print 'x Value:', str(i.x)
