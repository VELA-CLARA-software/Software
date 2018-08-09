# import sys
# import os
# sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\sourceCode\\')
from ..sourceCode.SAMPLcore.Components import Drift as d
from ..sourceCode.SAMPLcore.Components import Dipole as D
from ..sourceCode.SAMPLcore.Components import Quadrupole as Q
from ..sourceCode.SAMPLcore.Components import Screen as S
from ..sourceCode.SAMPLcore.Components import OrbitCorrector as C
from ..sourceCode.SAMPLcore.Components import BeamPositionMonitor as BPM
from ..sourceCode.SAMPLcore.Components import SolenoidAndRFClass as SARF
from ..sourceCode.SAMPLcore.Components import RFAcceleratingStructure as RF
from ..sourceCode.SAMPLcore.SAMPLlab import Beamline
# from sourceCode.SAMPLcore.SAMPLlab import PhysicalUnits
import numpy as np


class createBeamline():

    def __init__(self, V_MAG_Ctrl=None, C_S01_MAG_Ctrl=None,
                 C_S02_MAG_Ctrl=None, C2V_MAG_Ctrl=None, V_RF_Ctrl=None,
                 C_RF_Ctrl=None, L01_RF_Ctrl=None):
        self.V_MAG_Ctrl = V_MAG_Ctrl
        self.C_S01_MAG_Ctrl = C_S01_MAG_Ctrl
        self.C_S02_MAG_Ctrl = C_S02_MAG_Ctrl
        self.C2V_MAG_Ctrl = C2V_MAG_Ctrl
        self.V_RF_Ctrl = V_RF_Ctrl
        self.C_RF_Ctrl = C_RF_Ctrl
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
        elif 'GUN' in name:
            return self.V_RF_Ctrl.getLLRFObjConstRef()
        else:
            print ("Trying to get unrecognised object.")

    def create(self, selectedGroup, elements):

        line = Beamline.Beamline(componentlist=[])
        driftCounter = 0
        for index, name in enumerate(selectedGroup):
            element = elements[name]
            nickName = element['name']
            component = None
            # Check element type and add accordingly
            if element['type'] == 'dipole':
                component = self.addDipole(element, nickName, name)
            elif element['type'] == 'quadrupole':
                component = self.addQuadrupole(element, nickName, name)
            elif element['type'] == 'kicker':
                component = self.addCorrector(element, nickName, name)
            elif element['type'] == 'bpm':
                component = BPM.BeamPositionMonitor(name=name,
                                                    length=element['length'])
            elif element['type'] == 'screen':
                component = S.Screen(name=name)
            elif element['type'] == 'wcm':
                component = d.Drift(name=name, length=element['length'])
            elif element['type'] == 'tdc':
                component = d.Drift(name=name, length=element['length'])
            elif element['type'] == 'bam':
                component = d.Drift(name=name, length=element['length'])
            elif element['type'] == 'linac':
                linac = self.getObject(nickName, name)
                # get detials solnoids ascociated with the linac
                solenoid1 = elements[element['sol1']]
                solenoid2 = elements[element['sol2']]
                sol1 = self.getObject(solenoid1['name'], element['sol1'])
                sol2 = self.getObject(solenoid2['name'], element['sol2'])
                print 'LINAC grad: ' + str(linac.amp_MVM)
                print 'LINAC Phase: ' + str(linac.phi_DEG)
                #    component = SARF.SolenoidAndRF(length=element['length'],
                #                                   name='Linac1',
                #                                   peakField=linac.amp_MVM,
                #                                   phase=linac.phi_DEG,
                #                                   solCurrent1=sol1.siWithPol,
                #                                   solCurrent2=sol2.siWithPol)
                component = RF.RFAcceleratingStructure(length=element['length'],
                                                        name='Linac1',
                                                        voltage=-linac.amp_MVM * 1e6 * element['length'],
                                                        phase=linac.phi_DEG*(np.pi/180),
                                                        ncell=element['n_cells'],
                                                        structureType='TravellingWave')
                component.setFrequency(2998500000.0)
            else:
                component = d.Drift(name=name, length=element['length'])
                print ('ERROR: This reader doesn\'t',
                       'recognise element type of ', name)

            if index != 0:
                lastElement = elements[selectedGroup[index - 1]]
                backOfLast = lastElement['global_position'][-1]
                frontOfCurrent = element['global_position'][-1]
                angle = element['global_rotation'][-1]
                cosElementAngle = np.cos(angle * np.pi / 180)
                if element['type'] == 'dipole':
                    frontOfCurrent = element['global_front'][-1]
                else:
                    frontOfCurrent = (frontOfCurrent -
                                      element['length'] * cosElementAngle)

                if frontOfCurrent < backOfLast:
                    print ('Elements ', selectedGroup[index - 1],
                           ' and ', name, ' overlap!!')
                elif frontOfCurrent > backOfLast:
                    # Add a drift before adding component
                    b = frontOfCurrent
                    a = backOfLast
                    driftCounter = driftCounter + 1
                    driftComponent = d.Drift(name='drift' + str(driftCounter),
                                             length=(b - a) / cosElementAngle)
                    line.componentlist.append(driftComponent)
                else:
                    print 'No drift required', index

            # Append component
            line.componentlist.append(component)
        return line

# Complicated adding
    def addDipole(self, element, nickName, name):
        dip = self.getObject(nickName, name)
        angle = element['angle'] * (np.pi / 180)
        length = element['length']
        field = 0.0

        if dip.siWithPol != 0.0:
            coeffs = dip.fieldIntegralCoefficients
            absField = (np.polyval(coeffs, abs(dip.siWithPol)) /
                        dip.magneticLength)
            field = np.copysign(absField, dip.siWithPol)

        return D.Dipole(name=name, length=length, theta=angle, field=field)

    def addQuadrupole(self, element, nickName, name):
        print name
        quad = self.getObject(nickName, name)
        grad = 0.0

        if quad.siWithPol != 0.0:
            coeffs = quad.fieldIntegralCoefficients
            absGrad = (np.polyval(coeffs, abs(quad.siWithPol)) /
                       quad.magneticLength)
            grad = 1000 * np.copysign(absGrad, quad.siWithPol)

        return Q.Quadrupole(name=name, length=element['length'], gradient=grad)

    def addCorrector(self, element, nickName, name):
        print name
        vObj, hObj = self.getObject(nickName, name)
        vField = 0.0
        hField = 0.0

        if vObj.siWithPol != 0.0:
            print vObj.magneticLength
            coeffs = vObj.fieldIntegralCoefficients
            absVField = (np.polyval(coeffs, abs(vObj.siWithPol)) /
                         vObj.magneticLength)
            vField = 1000 * np.copysign(absVField, vObj.siWithPol)

        if hObj.siWithPol != 0.0:
            print hObj.magneticLength
            coeffs = hObj.fieldIntegralCoefficients
            absVField = (np.polyval(coeffs, abs(hObj.siWithPol)) /
                         hObj.magneticLength)
            vField = 1000 * np.copysign(absVField, hObj.siWithPol)

        return C.OrbitCorrector(name=name, field=[hField, vField],
                                length=element['length'])
