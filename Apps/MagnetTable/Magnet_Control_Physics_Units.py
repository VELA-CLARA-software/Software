#!python2
# -*- coding: utf-8 -*-
# encoding=utf8

# Reimplementation of lower-level VELA_CLARA_Magnet_Controller
# with physical units (K, angle etc) associated with magnets

import sys
sys.path.insert(0, r'\\apclara1\ControlRoomApps\Controllers\bin\Release')
import VELA_CLARA_Magnet_Control
from enum import IntEnum
from functools import wraps, partial  # for class method decorators
import numpy as np
import scipy.constants

SPEED_OF_LIGHT = scipy.constants.c / 1e6  # in megametres/second, use with p in MeV/c

class MomentumMode(IntEnum):
    """When we change the momentum, do we recalculate all the K values, or rescale the currents to keep K constant?"""
    RECALCULATE_K = 0
    SCALE_CURRENTS = 1


def getMomSectionIndex(self, location):
    """This section has at least two momenta (i.e. there's a cavity in it somewhere) - which one to get?
    The location can be specified as an integer index, a float position in metres, or a magnet name."""
    if isinstance(location, int):  # we can use an integer index: 0 for the first bit, 1 for the second, ...
        index = location
    elif isinstance(location, float):  # or a position along the beamline in metres as a float value
        positions = [self.getPosition(name) for name in self.momentum_sections]
        index = [i for i, pos in enumerate(positions) if location >= pos][-1]
    elif location in self.momentum_sections:  # or a specified component name where the location changes
        index = self.momentum_sections.index(location)
    elif isinstance(location, str):  # or the name of an arbitrary component
        index = self.getMomSectionIndex(self.getPosition(location))
    return index

def getMomentum(self, location=0):
    """Momentum of the section in MeV/c, after initial acceleration (if any)."""
    if len(self.momentum_sections) == 0:
        # momentum_sections is an empty tuple, so this section only has one momentum
        return self._momentum
    else:
        return self._momentum[self.getMomSectionIndex(location)]

def setMomentum(self, momentum, location=0):
    """Set the section momentum in MeV/c."""
    if self.momentum_mode == MomentumMode.SCALE_CURRENTS:
        if len(self.momentum_sections) == 0:
            min_pos, max_pos = float('-inf'), float('inf')
        else:
            index = self.getMomSectionIndex(location)
            start_magnet_name = self.momentum_sections[index]
            min_pos = self.getPosition(start_magnet_name)
            try:
                end_magnet_name = self.momentum_sections[index + 1]
                max_pos = self.getPosition(end_magnet_name)
            except IndexError:  # nope, we're on the last section already
                max_pos = float('inf')
        # rescale all the currents
        # first we need to get all the K values
        names = self.getMagnetNames()
        k_array = [(name, self.getK(name)) for name in names if min_pos <= self.getPosition(name) < max_pos]  # note: < NOT <= since max_pos is the position of the next section's start magnet
        print(k_array)

    if len(self.momentum_sections) == 0:
        # momentum_sections is an empty tuple, so this section only has one momentum
        self._momentum = momentum
    else:
        print(self.getMomSectionIndex(location))
        self._momentum[self.getMomSectionIndex(location)] = momentum

    if self.momentum_mode == MomentumMode.SCALE_CURRENTS:
        [self.setK(name, k) for name, k in k_array]

VELA_CLARA_Magnet_Control.magnetController.getMomSectionIndex = getMomSectionIndex
VELA_CLARA_Magnet_Control.magnetController.getMomentum = getMomentum
VELA_CLARA_Magnet_Control.magnetController.setMomentum = setMomentum

def getK(magnet):
    """K value for quadrupoles, or bend angle in degrees for dipoles, or bend angle in mrad for correctors."""
    current = magnet.siWithPol
    momentum = magnet.controller.getMomentum()

    # Get the integrated strength, based on an excitation curve
    # This is in T.mm for dipoles, T for quads, T/m for sextupoles
    # Note that excitation curves are defined with positive current,
    # so we invert the coefficients (except the offset) for negative current
    # This gives a smooth transition through zero
    sign = np.copysign(1, current)
    coeffs = np.append(magnet.fieldIntegralCoefficients[:-1] * sign, magnet.fieldIntegralCoefficients[-1])
    int_strength = np.polyval(coeffs, abs(current))
    # Calculate the normalised effect on the beam
    # This is in radians for dipoles, m⁻¹ for quads, m⁻² for sextupoles
    # effect = np.copysign(SPEED_OF_LIGHT * int_strength / momentum, current)
    effect = SPEED_OF_LIGHT * int_strength / momentum
    # Depending on the magnet type, convert to meaningful units
    mag_type = str(magnet.magType)
    if mag_type == 'DIP':
        # Get deflection in degrees
        # int_strength was in T.mm so we divide by 1000
        k = np.degrees(effect / 1000)
    elif mag_type in ('QUAD', 'SEXT'):
        k = 1000 * effect / magnet.magneticLength  # focusing term K
    elif mag_type in ('HCOR', 'VCOR'):
        k = effect  # deflection in mrad
    elif mag_type == 'BSOL':  # bucking coil
        # For the BSOL, coefficients refer to the solenoid current as well as the BSOL current
        # The 'K' value is the field at the cathode
        # x is BC current, y is solenoid current
        x = current
        y = magnet.controller.getSI('SOL')
        k_coeffs = np.array(magnet.fieldIntegralCoefficients[:-4])
        k = np.dot(k_coeffs,
                   [y, y ** 2, y ** 3, x, x * y, x * y ** 2, x ** 2, x ** 2 * y, x ** 2 * y ** 2, x ** 2 * y ** 3,
                    x ** 3, x ** 3 * y])
    elif mag_type == 'SOL':  # solenoids
        # For the solenoid, coefficients also refer to the momentum
        # The 'K' value is the Larmor angle
        I = current
        p = momentum
        k_coeffs = np.array(magnet.fieldIntegralCoefficients[:-4])
        k = np.dot(k_coeffs, [I, p * I, p ** 2 * I, p ** 3 * I, p ** 4 * I])
    return k

def setK(magnet, k):
    """Calculate the current to set in a magnet based on its K value (or bend angle)."""
    # What is the momentum in this section?
    momentum = magnet.controller.getMomentum(magnet.position)
    mag_type = str(magnet.magType)
    int_strength = None
    if mag_type == 'DIP':  # k represents deflection in degrees
        effect = np.radians(k) * 1000
    elif mag_type in ('QUAD', 'SEXT'):
        effect = k * magnet.magneticLength / 1000
    elif mag_type in ('HCOR', 'VCOR'):  # k represents deflection in mrad
        effect = k
    else:  # solenoids
        int_strength = k
    if int_strength is None:
        int_strength = effect * momentum / SPEED_OF_LIGHT
    coeffs = np.copy(magnet.fieldIntegralCoefficients[:-4] if mag_type in ('SOL', 'BSOL') else magnet.fieldIntegralCoefficients)
    # are we above or below residual field? Need to set coeffs accordingly to have a smooth transition through zero
    sign = np.copysign(1, int_strength - coeffs[-1])
    coeffs = np.append(coeffs[:-1] * sign, coeffs[-1])
    if mag_type == 'BSOL':
        # These coefficients depend on solenoid current too - need to group together like terms
        y = magnet.controller.getSI('SOL')
        ypows = y ** np.arange(4)
        coeffs = [np.dot(coeffs[10:], ypows[:2]),  # (c10 + c11*y) * x**3
                  np.dot(coeffs[6:10], ypows),  # (c6 + c7*y + c8*y**2 + c9*y**3) * x**2
                  np.dot(coeffs[3:6], ypows[:-1]),  # (c3 + c4*y + c5*y**2) * x
                  np.dot(coeffs[:3], ypows[1:])]  # (c0*y + c1*y**2 + c2*y**3)
    elif mag_type == 'SOL' and len(coeffs) > 2:
        # These coefficients depend on momentum too - need to group together like terms
        ppows = momentum ** np.arange(5)
        coeffs = [np.dot(coeffs[:5], ppows), 0]  # (c1 + c2*p + c3*p**2 + c4*p**3 + c5*p**4) * Isol

    coeffs[-1] -= int_strength  # Need to find roots of polynomial, i.e. a1*x + a0 - y = 0
    roots = np.roots(coeffs)
    current = np.copysign(roots[-1].real, sign)  # last root is always x value (#TODO: can prove this?)
    magnet.controller.setSI(magnet.name, current)


VELA_CLARA_Magnet_Control.magnetObject.k = property(getK, setK)

k_unit_dict = {'DIP': u'°', 'QUAD': u'm⁻²', 'HCOR': 'mrad', 'VCOR': 'mrad', 'BSOL': 'T', 'SOL': u'°'}
def addKFuncs(f):
    """Add functions for getting and setting K values to a magnet object, as well as a reference to the controller."""
    @wraps(f)
    def wrapped(self, *f_args, **f_kwargs):
        mag_obj = f(self, *f_args, **f_kwargs)
        mag_obj.controller = self
        mag_type = str(mag_obj.magType)
        mag_obj.k_units = k_unit_dict[mag_type]
        return mag_obj
    return wrapped

# Replace the magnetController class' function with our own wrapper code, which adds functions to get and set K
VELA_CLARA_Magnet_Control.magnetController.getMagObjConstRef = addKFuncs(VELA_CLARA_Magnet_Control.magnetController.getMagObjConstRef)

def getKOfMagnet(self, name):
    """Function for the magnet controller to get the K value of a given magnet (analogous to getSI)."""
    return self.getMagObjConstRef(name).k

def setKOfMagnet(self, name, k):
    """Function for the magnet controller to set the K value of a given magnet (analogous to setSI)."""
    self.getMagObjConstRef(name).k = k

VELA_CLARA_Magnet_Control.magnetController.getK = getKOfMagnet
VELA_CLARA_Magnet_Control.magnetController.setK = setKOfMagnet

areas = VELA_CLARA_Magnet_Control.MACHINE_AREA
modes = VELA_CLARA_Magnet_Control.MACHINE_MODE

class init(VELA_CLARA_Magnet_Control.init):
    """Subclassed magnet controller initialisation routine."""
    def __init__(self):
        super(init, self).__init__()
        # Add some named functions for creating magnet controllers
        for mode_name, mode in modes.names.items():
            for area_name, area in areas.names.items():
                setattr(self, '{}_{}_Magnet_Controller'.format(mode_name.lower(), area_name),
                        partial(self.getMagnetController, mode, area))

    def getMagnetController(self, mode, area):
        """Return the magnet controller, and add momentum and getK properties."""
        mc = super(init, self).getMagnetController(mode, area)
        mc.momentum_mode = MomentumMode.RECALCULATE_K

        if area in (areas.CLARA_PH1, areas.CLARA_2_BA1, areas.CLARA_2_BA1_BA2, areas.CLARA_2_BA2):
            mc.momentum_sections = ('BSOL', 'L01-SOL1')
            mc._momentum = [4, 45]
        # elif area == areas.VELA_INJ:  # for testing
        #     mc.momentum_sections = ('BSOL', 'QUAD03')
        #     mc._momentum = [4, 4]
        #     print('test')
        else:
            mc.momentum_sections = ()
            mc._momentum = 4
        return mc

# Reimplement everything else as-is

class CONTROLLER_TYPE(VELA_CLARA_Magnet_Control.CONTROLLER_TYPE):
    pass


class ILOCK_STATE(VELA_CLARA_Magnet_Control.ILOCK_STATE):
    pass


class MACHINE_AREA(VELA_CLARA_Magnet_Control.MACHINE_AREA):
    pass


class MACHINE_MODE(VELA_CLARA_Magnet_Control.MACHINE_MODE):
    pass


class MAG_PSU_STATE(VELA_CLARA_Magnet_Control.MAG_PSU_STATE):
    pass


class MAG_REV_TYPE(VELA_CLARA_Magnet_Control.MAG_REV_TYPE):
    pass


class MAG_TYPE(VELA_CLARA_Magnet_Control.MAG_TYPE):
    pass


class STATE(VELA_CLARA_Magnet_Control.STATE):
    pass


class VCbase(VELA_CLARA_Magnet_Control.VCbase):
    pass


class magnetStateStruct(VELA_CLARA_Magnet_Control.magnetStateStruct):
    pass


