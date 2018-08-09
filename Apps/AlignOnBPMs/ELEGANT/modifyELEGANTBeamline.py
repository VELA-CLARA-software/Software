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

    def modfiy(self, pathway):

        for index, name in pathway.elements.iteritems():
            element = pathway.elements[name]
            nickName = element['name']
            component = None
            # Check element type and add accordingly
            if element['type'] == 'dipole':
                self.changeDipole(pathway, element, nickName, name)
            elif element['type'] == 'quadrupole':
                self.changeQuadrupole(pathway, element, nickName, name)
            elif element['type'] == 'kicker':
                self.changeCorrector(pathway, element, nickName, name)
'''
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
'''
            elif element['type'] == 'cavity':
                cavity = self.getObject(nickName, name)
                # get detials solnoids ascociated with the linac
                solenoid1 = elements[element['sol1']]
                solenoid2 = elements[element['sol2']]
                sol1 = self.getObject(solenoid1['name'], element['sol1'])
                sol2 = self.getObject(solenoid2['name'], element['sol2'])
                print 'LINAC grad: ' + str(cavity.amp_MVM)
                print 'LINAC Phase: ' + str(cavity.phi_DEG)
                pathway.modifyElement(element=element,
                                      setting='field_amplitude',
                                      value=cavity.amp_MVM*1e6)
                pathway.modifyElement(element=element,
                                      setting='phase',
                                      value=cavity.phi_DEG*1e6)
            else:
                print ('ERROR: This reader doesn\'t',
                       'recognise element type of ', name)
            # Append component
            line.componentlist.append(component)

# Complicated adding
    def changeDipole(self, pathway, element, nickName, name):
        dip = self.getObject(nickName, name)
        field = 0.0
        coeffs = dip.fieldIntegralCoefficients
        absField = (np.polyval(coeffs, abs(dip.siWithPol)) /
                    dip.magneticLength)
        field = np.copysign(absField, dip.siWithPol)
        pathway.modifyElement(element=element,
                              setting='field',
                              value=field)

    def changeQuadrupole(self, element, nickName, name):
        quad = self.getObject(nickName, name)
        grad = 0.0
        coeffs = quad.fieldIntegralCoefficients
        absGrad = (np.polyval(coeffs, abs(quad.siWithPol)) /
                   quad.magneticLength)
        grad = 1000 * np.copysign(absGrad, quad.siWithPol)
        pathway.modifyElement(element=element,
                              setting='k1',
                              value=field)

    def changeCorrector(self, element, nickName, name):
        print name
        vObj, hObj = self.getObject(nickName, name)
        vField = 0.0
        hField = 0.0
        coeffs = vObj.fieldIntegralCoefficients
        absVField = (np.polyval(coeffs, abs(vObj.siWithPol)) /
                     vObj.magneticLength)
        vField = 1000 * np.copysign(absVField, vObj.siWithPol)

        coeffs = hObj.fieldIntegralCoefficients
        absHField = (np.polyval(coeffs, abs(hObj.siWithPol)) /
                     hObj.magneticLength)
        hField = 1000 * np.copysign(absVField, hObj.siWithPol)

        pathway.modifyElement(element=element,
                              setting='H_Field',
                              value=hField)
        pathway.modifyElement(element=element,
                              setting='V_Field',
                              value=vField)
