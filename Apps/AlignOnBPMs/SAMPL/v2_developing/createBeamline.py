'''Assumes  you have the a OnlineModel in you path directory'''
from SAMPL.sourceCode.SAMPLcore.Components import Drift as d
from SAMPL.sourceCode.SAMPLcore.Components import Dipole as D
from SAMPL.sourceCode.SAMPLcore.Components import Quadrupole as Q
from SAMPL.sourceCode.SAMPLcore.Components import Screen as S
from SAMPL.sourceCode.SAMPLcore.Components import OrbitCorrector as C
from SAMPL.sourceCode.SAMPLcore.Components import BeamPositionMonitor as BPM
# from ..sourceCode.SAMPLcore.Components import SolenoidAndRFClass as SARF
from SAMPL.sourceCode.SAMPLcore.Components import RFAcceleratingStructure as RF
from SAMPL.sourceCode.SAMPLcore.SAMPLlab import Beamline
# from OnlineMode.SAMPL.sourceCode.SAMPLcore.SAMPLlab import PhysicalUnits
import numpy as np
import math as m

class createBeamline():

    def __init__(self, V_MAG_Ctrl=None, C_S01_MAG_Ctrl=None,
                 C_S02_MAG_Ctrl=None, C2V_MAG_Ctrl=None, LRRG_RF_Ctrl=None,
                 HRRG_RF_Ctrl=None, L01_RF_Ctrl=None):
        self.V_MAG_Ctrl = V_MAG_Ctrl
        self.C_S01_MAG_Ctrl = C_S01_MAG_Ctrl
        self.C_S02_MAG_Ctrl = C_S02_MAG_Ctrl
        self.C2V_MAG_Ctrl = C2V_MAG_Ctrl
        self.LRRG_RF_Ctrl = LRRG_RF_Ctrl
        self.HRRG_RF_Ctrl = HRRG_RF_Ctrl
        self.L01_RF_Ctrl = L01_RF_Ctrl

    def getObject(self, nickName, name):
        if 'EBT' in name and 'MAG' in name:
            if 'COR' in name:
                vObj = self.V_MAG_Ctrl.getMagObjConstRef('V' + nickName)
                hObj = self.V_MAG_Ctrl.getMagObjConstRef('H' + nickName)
                return vObj, hObj
            else:
                return self.V_MAG_Ctrl.getMagObjConstRef(nickName)
        elif 'S01' in name and 'MAG' in name:
            if 'COR' in name:
                vObj = self.C_S01_MAG_Ctrl.getMagObjConstRef('S01-V' + nickName)
                hObj = self.C_S01_MAG_Ctrl.getMagObjConstRef('S01-H' + nickName)
                return vObj, hObj
            else:
                return self.C_S01_MAG_Ctrl.getMagObjConstRef(nickName)
        elif 'L01' in name and 'MAG' in name:
            return self.C_S01_MAG_Ctrl.getMagObjConstRef(nickName)
        elif 'S02' in name and 'MAG' in name:
            if 'COR' in name:
                vObj = self.C_S02_MAG_Ctrl.getMagObjConstRef('S02-V' + nickName)
                hObj = self.C_S02_MAG_Ctrl.getMagObjConstRef('S02-H' + nickName)
                return vObj, hObj
            else:
                return self.C_S02_MAG_Ctrl.getMagObjConstRef(nickName)
        elif 'C2V' in name and 'MAG' in name:
            if 'COR' in name:
                vObj = self.C2V_MAG_Ctrl.getMagObjConstRef('C2V-V' + nickName)
                hObj = self.C2V_MAG_Ctrl.getMagObjConstRef('C2V-H' + nickName)
                return vObj, hObj
            else:
                return self.C2V_MAG_Ctrl.getMagObjConstRef(nickName)
        elif 'L01' in name:
            return self.L01_RF_Ctrl.getLLRFObjConstRef()
        elif 'GUN' in name and 'LR' in name:
            return self.LRRG_RF_Ctrl.getLLRFObjConstRef()
        elif 'GUN' in name and 'HR' in name:
            return self.HRRG_RF_Ctrl.getLLRFObjConstRef()
        else:
            print ("Trying to get unrecognised object.")

    def create(self, pathway, startElement, stopElement):

        line = Beamline.Beamline(componentlist=[])
        driftCounter = 0
        mod = False
        #print pathway.elementOrder
        #for name, element in pathway.elements.iteritems():
    #        print name
        for name, element in pathway.elements.iteritems():
            if name == startElement:
                mod = True

            if mod is True:
                #print name
                # print element['type']
                # Check element type and add accordingly
                if element['type'] == 'dipole':
                    component = self.addDipole(element, element['Controller_Name'], name)
                elif element['type'] == 'quadrupole':
                    component = self.addQuadrupole(element, element['Controller_Name'], name)
                elif element['type'] == 'kicker':
                    component = self.addCorrector(element, element['Controller_Name'], name)
                elif element['type'] == 'beam_position_monitor':
                    length = pathway.getElement(element=name,
                                           setting='length',
                                           default=0)
                    component = BPM.BeamPositionMonitor(name=name,
                                                        length=length)
                elif element['type'] == 'screen':
                    component = S.Screen(name=name)
                elif element['type'] == 'wcm':
                    component = d.Drift(name=name, length=element['length'])
                elif element['type'] == 'tdc':
                    component = d.Drift(name=name, length=element['length'])
                elif element['type'] == 'bam':
                    component = d.Drift(name=name, length=element['length'])
                elif element['type'] == 'cavity':
                    component = self.addAccerlatingRF(element, element['Controller_Name'], name)
                else:
                    length = pathway.getElement(element=name,
                                           setting='length',
                                           default=0)
                    component = d.Drift(name=name, length=length)
                    # print (' ARNING: This reader doesn\'t' +
                    #       'recognise element type of ' + name)

                if name != startElement:
                    #print name
                    previousElement = pathway.previousElement(name)
                    # is a list
                    if type(previousElement[0])==type([]):
                        lastElementName = previousElement[0][0]
                        lastElement = previousElement[1][0]
                    else:
                        lastElementName = previousElement[0]
                        lastElement = previousElement[1]
                    #print lastElement
                    backOfLast = lastElement['position_end'][-1]
                    frontOfCurrent = element['position_start'][-1]
                    global_rotation = pathway.getElement(element=name,
                                                         setting='global_rotation',
                                                         default=[0, 0, 0])
                    angle = global_rotation[-1]
                    cosElementAngle = np.cos(angle)
                    if element['type'] == 'dipole':
                        frontOfCurrent = element['buffer_start'][-1]
                    if frontOfCurrent < backOfLast:
                        print ('Elements ' + lastElementName +
                               ' and ' + name + ' overlap!!')
                    elif frontOfCurrent > backOfLast:
                        # Add a drift before adding component
                        b = frontOfCurrent
                        a = backOfLast
                        driftCounter = driftCounter + 1
                        driftComponent = d.Drift(name='drift' + str(driftCounter),
                                                 length=(b - a) / cosElementAngle)
                        line.componentlist.append(driftComponent)
                    #else:
                    #    print ('No drift required between ' + lastElementName +
                    #           ' and ' + name)
                # Append component
                line.componentlist.append(component)
                if name == stopElement:
                    mod = False
        return line

# Complicated adding
    def addAccerlatingRF(self, element, nickName, name):
        rf = self.getObject(nickName, name)
        # get detials solnoids ascociated with the linac
        #solenoid1 = elements[element['sol1']]
        #solenoid2 = elements[element['sol2']]
        #sol1 = self.getObject(solenoid1['name'], element['sol1'])
        #sol2 = self.getObject(solenoid2['name'], element['sol2'])
        #print 'rf grad: ' + str(rf.amp_MVM)
        #print 'rf Phase: ' + str(rf.phi_DEG)
        structureType = 'Null'
        if element['Structure_Type'] == 'TravellingWave':
            structureType = 'TravellingWave'
        elif element['Structure_Type'] == 'StandingWave':
            structureType = 'StandingWave'
        # component = SARF.SolenoidAndRF(length=element['length'],
        #                                   name='Linac1',
        #                                   peakField=linac.amp_MVM,
        #                                   phase=linac.phi_DEG,
        #                                   solCurrent1=sol1.siWithPol,
        #                                   solCurrent2=sol2.siWithPol)
        #print rf.amp_MVM * 1e6 * element['length']
        component = RF.RFAcceleratingStructure(length=element['length'],
                                               name=nickName,
                                               voltage=-(rf.amp_MVM * 1e6 *
                                                         element['length']),
                                               phase=rf.phi_DEG * (np.pi / 180),
                                               ncell=int(element['n_cells']),
                                               structureType=structureType)
        component.setFrequency(element['frequency'])
        return component

    def addDipole(self, element, nickName, name):
        dip = self.getObject(nickName, name)
        angle = element['angle']
        length = element['length']
        field = 0.0

        if dip.siWithPol != 0.0:
            coeffs = dip.fieldIntegralCoefficients
            absField = (np.polyval(coeffs, abs(dip.siWithPol)) /
                        dip.magneticLength)
            field = np.copysign(absField, dip.siWithPol)

        return D.Dipole(name=name, length=length, theta=angle, field=field)

    def addQuadrupole(self, element, nickName, name):
        # print name
        quad = self.getObject(nickName, name)
        grad = 0.0

        if quad.siWithPol != 0.0:
            coeffs = quad.fieldIntegralCoefficients
            absGrad = (np.polyval(coeffs, abs(quad.siWithPol)) /
                       quad.magneticLength)
            grad = 1000 * np.copysign(absGrad, quad.siWithPol)

        return Q.Quadrupole(name=name, length=element['length'], gradient=grad)

    def addCorrector(self, element, nickName, name):
        # print name
        vObj, hObj = self.getObject(nickName, name)
        vField = 0.0
        hField = 0.0

        if vObj.siWithPol != 0.0 and vObj.siWithPol != -999.999:
            # print vObj.magneticLength
            coeffs = vObj.fieldIntegralCoefficients
            absHField = (np.polyval(coeffs, abs(vObj.siWithPol)) /
                         vObj.magneticLength)
            hField = 1000 * np.copysign(absHField, vObj.siWithPol)

        if hObj.siWithPol != 0.0 and hObj.siWithPol != -999.999:
            #print hObj.magneticLength
            coeffs = hObj.fieldIntegralCoefficients
            absVField = (np.polyval(coeffs, abs(hObj.siWithPol)) /
                         hObj.magneticLength)
            vField = 1000 * np.copysign(absVField, hObj.siWithPol)

        return C.OrbitCorrector(name=name, field=[hField, vField],
                                length=element['length'])
