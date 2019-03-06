from PyQt4.QtCore import QObject#, pyqtSignal
import numpy as np
import scipy.constants as physics

class Functions(QObject):
    #qctrl_sig = pyqtSignal(float)

    #def __init__(self, OM = dummyOM()):
    def __init__(self, model):
        super(Functions, self).__init__()
        self.model = model

    def test(self, x):
        print x*2

    def I2mom(self, dctrl, dipole, I):
        D = dctrl.getMagObjConstRef(dipole)
        #return (400.0033/D.magneticLength)*(np.polyval(D.fieldIntegralCoefficients, abs(I))*physics.c*180)/(45*physics.pi*1000000000)
        return (np.polyval(D.fieldIntegralCoefficients, abs(I))*physics.c*180)/(45*physics.pi*1e9)

    def mom2I(self, dctrl, dipole, mom):
        D = dctrl.getMagObjConstRef(dipole)
        coeffs = list(D.fieldIntegralCoefficients)
        #print coeffs
        #print(1000000000*(mom*physics.pi*45)/(physics.c*180))
        #coeffs[-1] -= (D.magneticLength/400.0033)*(1000000000*(mom*physics.pi*45)/(physics.c*180))
        coeffs[-1] -= (1e9*(mom*physics.pi*45)/(physics.c*180))
        roots = np.roots(coeffs)
        current = roots[-1].real
        return current
