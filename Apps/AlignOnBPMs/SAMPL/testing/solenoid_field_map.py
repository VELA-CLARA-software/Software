#!python2
# -*- coding: utf-8 -*-
"""Solenoid Field Map
Ben Shepherd, April 2017
Given a named solenoid and current, provides a field map.
Combined solenoid and bucking coil maps are handled too."""

import numpy as np
from collections import namedtuple
import scipy.interpolate
from pkg_resources import resource_filename

# Solenoids that we know about.
# The ones prefixed 'gb-' are referenced in the Gulliford/Bazarov paper.
SOLENOID_LIST = ('gb-rf-gun', 'gb-dc-gun', 'Gun-10', 'Gun-400', 'Linac1')

field_map_attr = namedtuple('field_map_attr', 'coeffs z_map bc_area bc_turns sol_area sol_turns')
field_map_attr.__new__.__defaults__ = (1, 1, 1, 1)

def interpolate(x, y):
    "Return an interpolation object with some default parameters."
    if scipy.version.full_version >= '0.17.0':
        interp = scipy.interpolate.interp1d(x, y, fill_value='extrapolate', bounds_error=False)
    else:
        # numpy <0.17.0 doesn't allow extrapolation - so use the values at the start and end
        x = np.insert(x, 0, -1e99)
        y = np.insert(y, 0, y[0])
        x = np.append(x, 1e99)
        y = np.append(y, y[-1])
        interp = scipy.interpolate.interp1d(x, y, bounds_error=False)
    return interp


class Solenoid():
    """Create a reference to a known solenoid."""

    def __init__(self, name, quiet=True):
        """Initialise the class, setting parameters relevant to the named setup."""
        self.quiet = quiet
        if not name in SOLENOID_LIST:
            raise NotImplementedError('Unknown solenoid "{name}". Valid names are {SOLENOID_LIST}.'.format(**locals()))
        self.name = name
        self.calc_done = False
        if name[:3] == 'Gun':
            # 2D models of Gun-10 and Gun-400 solenoids have slightly different sizes for their coils.
            # This should be resolved at some point... TODO
            if name == 'Gun-10':
                bc_area, bc_turns, sol_area = (856.0, 720.0, 8281.0)
                self.bc_range = (0.0, 5.0)
                self.bc_current = 5.0  # reasonable default value
            else:
                bc_area, bc_turns, sol_area = (2744.82, 54.0, 7225.0)
                self.bc_range = (0.0, 400.0)
                self.bc_current = 400.0  # reasonable default value
            # magnetic field map built up from coefficients for x**n and y**n
            # where x = BC current density
            # and y = solenoid current density
            # and n <= 3
            # See BJAS' spreadsheet: coeffs-vs-z.xlsx
            # This takes care of interaction between the BC and solenoid
            field_map_coeffs = np.loadtxt(str(name + '-coeffs-vs-z.csv'), delimiter=',')
            self.b_field = field_map_attr(coeffs=field_map_coeffs, z_map=np.arange(0, 401, dtype='float64') * 1e-3,
                                          bc_area=bc_area, bc_turns=bc_turns, sol_area=sol_area, sol_turns=144.0)
            self.z_map = self.b_field.z_map
            self.sol_current = 300.0  # reasonable default value
            self.sol_range = (0.0, 500.0)

        elif name == 'Linac1':
            # Modelled solenoid field
            # path = r'\\fed.cclrc.ac.uk\Org\NLab\ASTeC-TDL\Projects\tdl-1168 CLARA\CLARA-ASTeC Folder\Accelerator Physics\ASTRA\Injector\fieldmaps' + '\\'
            # z_list, B_list = np.loadtxt(path + 'SwissFEL_linac_sols.dat').T

            # Measured solenoid field
            path = r'\\fed.cclrc.ac.uk\Org\NLab\ASTeC-TDL\Projects\tdl-1168 CLARA\mag - magnets (WP2)\SwissFEL Linac Solenoids' + '\\'
            x, y, z, Bz = np.loadtxt(path + 'wfs08_YZ.lis', skiprows=17, unpack=True)
            self.bc_current = 199.93  # defined in file
            on_axis = y == 0
            z_list_08 = z[on_axis] / 100  # convert cm -> m
            B_list_08 = Bz[on_axis] * 1e-4 / self.bc_current  # convert G -> T and normalise to current

            x, y, z, Bz = np.loadtxt(path + 'wfs09_YZ.lis', skiprows=17, unpack=True)
            self.sol_current = 199.93  # defined in file
            on_axis = y == 0
            z_list_09 = z[on_axis] / 100  # convert cm -> m
            B_list_09 = Bz[on_axis] * 1e-4 / self.sol_current  # convert G -> T and normalise to current

            # From document: file:///\\fed.cclrc.ac.uk\Org\NLab\ASTeC-TDL\Projects\tdl-1168%20CLARA\CLARA-ASTeC%20Folder\Accelerator%20Physics\ASTRA\Injector\CLARA%20v10%20Injector%20Simulations%20v0.3.docx
            cell_length = 0.033327
            n_cells = 61
            n_sols = 2
            dz = (z_list_08[-1] - z_list_08[0]) / (len(z_list_08) - 1)
            # TODO: fix actual position of solenoids
            z_offset = np.array([-1, 1]) * cell_length * (n_cells - 1) / 4
            print(z_offset)
            z_minmax = z_offset + z_list_08[[0, -1]]
            print(z_minmax)
            z_map = np.arange(*z_minmax, step=dz)
            B_map = np.zeros((n_sols, len(z_map)))
            # Here, we reverse the order of B_list since the solenoids are installed with the -Z end (in the measured coordinate system)
            # at the +Z end (in the machine coordinate system). Source: private email from Vjeran Vrankovic to BJAS 12/7/17:
            # "you can see on the picture the orientation of the magnets while being measured. The front face with the reference holes is at -Z"
            # The picture is on the first page of the measurement report "WFS Magnetic Measurements.pdf" in the data files folder
            # We can see that the connections are on the right-hand side - installed on CLARA they are on the left.
            sol_interp = [scipy.interpolate.interp1d(z_list, B_list[::-1], fill_value=0, bounds_error=False) for z_list, B_list in [[z_list_08, B_list_08], [z_list_09, B_list_09]]]
            for i in range(n_sols):
                B_map[i] = sol_interp[i](z_map + z_offset[i])# / self.sol_current
            coeffs = np.zeros((len(z_map), 12))
            coeffs[:, 0] = B_map[0]
            coeffs[:, 3] = B_map[1]
            self.b_field = field_map_attr(coeffs=coeffs, z_map=z_map)
            # self.b_field = np.array([z_map, nom_sol_field * np.sum(B_map, 0) / self.sol_current])
            self.sol_range = self.bc_range = (-200.0, 200.0)
            self.z_map = z_map

        elif name[:3] == 'gb-':
            self.bc_current = None
            self.sol_current = 300.0  # just a made-up number

            # Define this in a simpler way - then we can just multiply by sol_current to get B-field value
            z_list, B_list = np.loadtxt('gb-field-maps/{}_b-field.csv'.format(name), delimiter=',').T
            self.b_field = np.array([z_list, B_list / self.sol_current])
            self.bc_range = None
            self.sol_range = (0.0, 500.0)

        self.bmax_index = np.argmax(self.getMagneticFieldMap())  # assume this won't change with sol/BC currents

    def setBuckingCoilCurrent(self, current):
        """Reset the bucking coil current to a new value."""
        if current != self.bc_current:
            self.bc_current = float(current)
            self.calc_done = False

    def setSolenoidCurrent(self, current):
        """Reset the solenoid current to a new value."""
        if current != self.sol_current:
            self.sol_current = float(current)
            self.calc_done = False

    def calcMagneticFieldMap(self):
        """Calculate the magnetic field map for given solenoid and BC currents."""
        if isinstance(self.b_field, tuple):
            # Coefficients describing how the B-field depends on the sol/BC currents
            X = self.bc_current * self.b_field.bc_turns / self.b_field.bc_area
            Y = self.sol_current * self.b_field.sol_turns / self.b_field.sol_area
            # Use a subset of coefficients
            A = np.array(
                [Y, Y ** 2, Y ** 3, X, X * Y, X * Y ** 2, X ** 2, X ** 2 * Y,
                 X ** 2 * Y ** 2, X ** 2 * Y ** 3, X ** 3, X ** 3 * Y]).T
            self.B_map = np.dot(self.b_field.coeffs, A)
            self.z_map = self.b_field.z_map
        else:
            # we've defined it as just an array, multiply by sol current to get field
            self.z_map, B_map = self.b_field
            self.B_map = B_map * self.sol_current
        self.B_interp = interpolate(self.z_map, self.B_map)
        self.calc_done = True

    def getZMap(self):
        """Return the longitudinal (z) coordinates used in the field map."""
        return self.z_map

    def getMagneticFieldMap(self):
        """Return the magnetic field map produced by the solenoid and bucking coil."""
        if not self.calc_done:
            self.calcMagneticFieldMap()
        return self.B_map

    def getMagneticField(self, z):
        """Return the magnetic field at a given z coordinate."""
        if not self.calc_done:
            self.calcMagneticFieldMap()
        return float(self.B_interp(z))

    def getPeakMagneticField(self):
        """Return the peak solenoid field in T."""
        if not self.calc_done:
            self.calcMagneticFieldMap()
        return float(self.B_map[self.bmax_index])

    def optimiseParam(self, opt_func, operation, x_name, x_units, target=None, target_units=None, tol=1e-6):
        """General function for optimising a parameter by varying another."""
        # operation should be of form "Set peak field" etc.
        x_init = getattr(self, x_name)
        if not self.quiet:
            target_text = '' if target == None else ', target {target:.3f} {target_units}'.format(**locals())
            print('{operation}{target_text}, by varying {x_name} starting at {x_init:.3f} {x_units}.'.format(**locals()))
        xopt = scipy.optimize.fmin(opt_func, x_init, xtol=1e-3, disp=not self.quiet)
        if not self.quiet:
            print('Optimised with {x_name} setting of {0:.3f} {x_units}'.format(float(xopt), **locals()))
        return float(xopt)

    def bcCurrentToCathodeField(self, bci):
        self.setBuckingCoilCurrent(bci)
        return self.getMagneticField(0.0)

    def setCathodeField(self, field=0.0):
        """Set the cathode field to a given level by changing the bucking coil 
        current, and return the value of this current."""
        delta_B_sq = lambda bci: (self.bcCurrentToCathodeField(bci) - field) ** 2
        return self.optimiseParam(delta_B_sq, 'Set field at cathode', 'bc_current', 'A', field, 'T')

    def solCurrentToPeakField(self, sol_current):
        self.setSolenoidCurrent(sol_current)
        return self.getPeakMagneticField()

    def setPeakMagneticField(self, field):
        """Set the peak magnetic field to a given level (in T) by changing the 
        solenoid current, and return the value of this current."""
        delta_B_sq = lambda soli: (self.solCurrentToPeakField(soli) - field) ** 2
        return self.optimiseParam(delta_B_sq, 'Set solenoid peak field', 'sol_current', 'A', field, 'T')

