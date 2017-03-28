#!python2
# -*- coding: utf-8 -*-
"""
RF and Solenoid Tracker v1.1 - Ben Shepherd - March 2017

Sets up a simulation of a combination of RF and solenoid fields,
and calculates the final momentum and Larmor angle of a beam.
Calculates the transfer matrix.

See Gulliford and Bazarov (2012): http://journals.aps.org/prab/abstract/10.1103/PhysRevSTAB.15.024002#fulltext
"""

import numpy as np
import scipy.constants
import scipy.interpolate
import scipy.optimize
import scipy.linalg
from functools import wraps  # for class method decorators
from collections import namedtuple
import matplotlib.pyplot as plt  # TODO: use pyqtgraph instead
import xlrd
from itertools import chain
import calcMomentum
import re

# http://stackoverflow.com/questions/31607458/how-to-add-clipboard-support-to-matplotlib-figures
import io
from PyQt4.QtGui import QApplication, QImage
def add_clipboard_to_figures():
    # use monkey-patching to replace the original plt.figure() function with
    # our own, which supports clipboard-copying
    oldfig = plt.figure

    def newfig(*args, **kwargs):
        fig = oldfig(*args, **kwargs)
        def clipboard_handler(event):
            if event.key == 'ctrl+c':
                # store the image in a buffer using savefig(), this has the
                # advantage of applying all the default savefig parameters
                # such as background color; those would be ignored if you simply
                # grab the canvas using Qt
                buf = io.BytesIO()
                fig.savefig(buf)
                QApplication.clipboard().setImage(QImage.fromData(buf.getvalue()))
                buf.close()

        fig.canvas.mpl_connect('key_press_event', clipboard_handler)
        return fig

    plt.figure = newfig

add_clipboard_to_figures()


class ReturnsBlank():
    def __getattr__(self, attr):
        return ''


try:
    from colorama import init, Fore, Back, Style  # for coloured text in the terminal!

    init(autoreset=True)
    import re
except ImportError:
    Fore = Back = Style = ReturnsBlank()

# notation
Re = lambda x: x.real

# constants
m = scipy.constants.electron_mass
c = scipy.constants.speed_of_light
e = -scipy.constants.elementary_charge
epsilon_e = m * c ** 2 / e


# https://wiki.python.org/moin/PythonDecoratorLibrary#Easy_Dump_of_Function_Arguments
def dump_args(func):
    "This decorator dumps out the arguments passed to a function before calling it"
    argnames = func.func_code.co_varnames[:func.func_code.co_argcount]
    fname = func.func_name

    def echo_func(*args, **kwargs):
        print fname, ":", ', '.join(
            '%s=%r' % entry
            for entry in zip(argnames, args) + kwargs.items())
        return func(*args, **kwargs)

    return echo_func


import ctypes
# http://stackoverflow.com/questions/38319606/how-to-get-millisecond-and-microsecond-resolution-timestamps-in-python
def millis():
    "return a timestamp in milliseconds (ms)"
    tics = ctypes.c_int64()
    freq = ctypes.c_int64()
    # get ticks on the internal ~2MHz QPC clock
    ctypes.windll.Kernel32.QueryPerformanceCounter(ctypes.byref(tics))
    # get the actual freq. of the internal ~2MHz QPC clock
    ctypes.windll.Kernel32.QueryPerformanceFrequency(ctypes.byref(freq))
    t_ms = tics.value * 1e3 / freq.value
    return t_ms

# https://www.andreas-jung.com/contents/a-python-decorator-for-measuring-the-execution-time-of-methods
def timeit(method):
    def timed(*args, **kw):
        ts = millis()
        result = method(*args, **kw)
        dt = millis() - ts
        if not args[0].quiet:  # args[0] is always self
            print '{method.__name__} ({args}, {kw}) {dt:.3f} ms'.format(**locals())
        return result
    return timed

# Calculation levels
# When parameters are changed, the calculation level is reset.
# A calculation will be performed again when necessary.
CALC_NONE, INIT_ARRAYS, CALC_MOM, CALC_B_MAP, CALC_LA, CALC_MATRICES = range(6)

def requires_calc_level(level):
    """A decorator that requires a certain level of calculation to be done
    before the function is executed."""
    def wrapper(f):
        @wraps(f)
        def wrapped(self, *f_args, **f_kwargs):
            if self.calc_level < level:
                if not self.quiet:
                    print('Calculating up to level {}.'.format(level))
                self.calculate(level)
            return f(self, *f_args, **f_kwargs)
        return wrapped
    return wrapper


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

def numbersInColumn(sheet, col):
    "Return the numeric values from a zero-indexed column in a worksheet from xlrd."
    column = [sheet.cell(r, col) for r in range(sheet.nrows)]
    return np.array([cell.value for cell in column if cell.ctype == xlrd.XL_CELL_NUMBER])


# Devices (guns/linacs) that we know about.
# The ones prefixed 'gb-' are referenced in the Gulliford/Bazarov paper.
MODEL_LIST = ('gb-rf-gun', 'gb-dc-gun', 'Gun-10')

field_map_attr = namedtuple('field_map_attr', 'coeffs z_map bc_area bc_turns sol_area sol_turns')

format_codes = re.compile('({[^}]+})')
def styleOutput(string):
    return string
    """Style the formatting of output text.
    Set the first line to be cyan, and all the {}-formatted numbers to be bright."""
    string = format_codes.sub(Style.BRIGHT + r'\1' + Style.NORMAL, string)
    lines = string.split('\n')
    if len(lines) > 0:
        lines[0] = Fore.CYAN + lines[0] + Fore.WHITE
    return '\n'.join(lines)


class RFSolTracker(object):
    """Simulation of superimposed RF and solenoid fields."""

    # Link the RI and SI properties
    def __getattribute__(self, name):
        if name == 'riWithPol':
            name = 'siWithPol'
        return super(RFSolTracker, self).__getattribute__(name)

    def __init__(self, name, quiet=True):
        """Initialise the class, setting parameters relevant to the named setup."""
        self.quiet = quiet
        if not name in MODEL_LIST:
            raise NotImplementedError(
                Fore.RED + 'Unknown model "{name}". Valid models are {MODEL_LIST}.'.format(**locals()))
        self.name = name

        # These properties are useful when accessing this class from the magnet table.
        self.magnetBranch = 'UNKNOWN_MAGNET_BRANCH'
        self.magType = 'GUN'
        self.riTolerance = 0.001  # fairly arbitrary
        self.fieldIntegralCoefficients = np.array([1, 0])
        self.magneticLength = None
        self.pvRoot = 'INJ-RF-GUN-01:'  # totally made up!

        # Set up the simulation
        if name == 'Gun-10':
            gun10_folder = r'\\fed.cclrc.ac.uk\Org\NLab\ASTeC-TDL\Projects\tdl-1168 CLARA\CLARA-ASTeC Folder\Accelerator Physics\ASTRA\Archive from Delta + CDR\\'
            self.measurementDataLocation = gun10_folder

            # Read in RF field map and normalise so peak = 1
            gun10_cav_fieldmap_file = gun10_folder + 'bas_gun.txt'
            gun10_cav_fieldmap = np.loadtxt(gun10_cav_fieldmap_file, delimiter='\t')

            self.rf_peak_field = float(np.max(gun10_cav_fieldmap[:, 1]) / 1e6)
            # Normalise
            gun10_cav_fieldmap[:, 1] /= (self.rf_peak_field * 1e6)
            self.norm_E = interpolate(*gun10_cav_fieldmap.T)
            #            self.E = lambda z: E_gun10(z) * self.rf_peak_field * 1e6
            self.freq = 2998.5 * 1e6  # in Hz
            self.phase = 330.0  # to get optimal acceleration

            # Set parameters
            self.dz = 0.5e-3  # in metres - OK to get within 0.5% of final momentum
            self.gamma_start = np.sqrt(1 + abs(1 / epsilon_e))  # 1 eV

            # magnetic field map built up from coefficients for x**n and y**n
            # where x = BC current density
            # and y = solenoid current density
            # and n <= 3
            # See BJAS' spreadsheet: coeffs-vs-z.xlsx
            # This takes care of interaction between the BC and solenoid
            self.b_field = field_map_attr(np.loadtxt('gun10-coeffs-vs-z.csv', delimiter=','),
                                          np.arange(-12, 467, dtype='float64') * 1e-3,
                                          856.0, 720.0, 8281.0, 144.0)
            self.z_end = max(gun10_cav_fieldmap[-1, 1], self.b_field.z_map[-1])

            self.bc_current = 5.0  # reasonable default value
            self.sol_current = 300.0  # reasonable default value

        elif name[:3] == 'gb-':
            if name == 'gb-dc-gun':
                sheet_name = 'G-B Fig 1 DC gun + sol'
                self.freq = 0
                self.dz = 1e-3
                self.z_end = 0.6
                self.gamma_start = np.sqrt(1 + abs(1 / epsilon_e))  # 1 eV
            elif name == 'gb-rf-gun':
                sheet_name = 'G-B Fig 5 RF gun + sol'
                self.freq = 1.3e9
                self.dz = 0.1e-3
                self.z_end = 0.3
                self.gamma_start = np.sqrt(1 + abs(1 / epsilon_e))  # 1 eV

            # TODO: should be on the server!
            fieldmap_folder = r'C:\Documents\CLARA'
            fieldmap_filename = fieldmap_folder + r'\Gun and solenoid field maps.xlsx'
            self.measurementDataLocation = fieldmap_folder
            book = xlrd.open_workbook(fieldmap_filename)
            sheet = book.sheet_by_name(sheet_name)
            z_list = numbersInColumn(sheet, 0)
            E_list = numbersInColumn(sheet, 1)  # in MV/m
            self.rf_peak_field = float(np.max(E_list))
            # Normalise
            E_list /= self.rf_peak_field
            self.norm_E = interpolate(z_list, E_list)
            self.phase = 295  # to get optimal acceleration

            z_list = numbersInColumn(sheet, 2)
            B_list = numbersInColumn(sheet, 4)
            self.bc_current = 0.0
            self.sol_current = 300.0  # just a made-up number

            # Define this in a simpler way - then we can just multiply by sol_current to get B-field value
            self.b_field = np.array([z_list, B_list / self.sol_current])

        self.siWithPol = self.phase
        self.calc_level = CALC_NONE
        # cached results (longitudinal and transverse)
        self.long_cache = self.trans_cache = {}

    def __repr__(self):
        return '<RFSolTracker {}>'.format(self.name)

    def calculate(self, level):
        """Calculate the output parameters for the given inputs."""
        if self.calc_level == CALC_NONE and level > CALC_NONE:
            self.initialiseArrays()
        if self.calc_level == INIT_ARRAYS and level > INIT_ARRAYS:
            self.calcMomentum()
        if self.calc_level == CALC_MOM and level > CALC_MOM:
            self.calcMagneticFieldMap()
        if self.calc_level == CALC_B_MAP and level > CALC_B_MAP:
            self.calcLarmorAngle()
        if self.calc_level == CALC_LA and level > CALC_LA:
            self.calcMatrices()
        if not self.quiet:
            print('New calculation level: {self.calc_level}'.format(**locals()))

    @timeit
    def initialiseArrays(self):
        """Initialise arrays to store results."""
        self.z_array = np.arange(0, self.z_end, self.dz)
        #        self.gamma_tilde_dash = [self.E(z) / -epsilon_e for z in self.z_array]
        self.gamma_tilde_dash = self.norm_E(self.z_array) * self.rf_peak_field * 1e6 / -epsilon_e
        self.theta_L_array = np.zeros_like(self.z_array)
        self.gamma_dash_array = np.zeros_like(self.z_array)
        self.u_array = np.zeros((len(self.z_array), 4))
        self.M_array = np.zeros((len(self.z_array), 4, 4))
        self.calc_level = INIT_ARRAYS

    def momentumGenerator(self):
        omega = 2 * np.pi * self.freq
        gamma = self.gamma_start
        beta = np.sqrt(1 - 1 / gamma ** 2)
        p = gamma * beta
        t = self.phase / (360 * self.freq)
        for gamma_tilde_dash in self.gamma_tilde_dash:
            gamma_dash = gamma_tilde_dash * np.cos(omega * t)
            yield t, gamma_dash, gamma, beta, p
            gamma += gamma_dash * self.dz
            p_new = np.sqrt(gamma ** 2 - 1)
            beta = p / gamma
            if gamma_dash == 0:
                dt = 1 / (beta * c)
            else:
                dt = (p_new - p) / (gamma_dash * c)
            p = p_new
            t += dt

    @timeit
    @requires_calc_level(INIT_ARRAYS)
    def calcMomentum(self):
        """Calculate the momentum gain for a given E-field distribution."""
        # start conditions
        if not self.quiet:
            fs = u'''Calculating momentum gain.
Peak field: {self.rf_peak_field:.3f} MV/m
Phase: {self.phase:.1f}°'''
            print(fs.format(**locals()))

        # Python generator method (11 ms to run)
        # result = np.fromiter(chain.from_iterable(self.momentumGenerator()), 'float64', count=len(self.gamma_tilde_dash) * 5).reshape(-1, 5)
        # self.t_array, self.gamma_dash_array, self.gamma_array, self.beta_array, self.p_array = np.array(result).T
        # Fortran method (0.8 ms to run)
        self.t_array, self.gamma_dash_array, self.gamma_array, self.beta_array, self.p_array = calcMomentum.calcmomentum(self.freq, self.phase, self.gamma_start, self.dz, self.gamma_tilde_dash)

        self.final_p_MeV = self.p_array[-1] * -1e-6 * epsilon_e

        if not self.quiet:
            print(styleOutput(u'Final momentum: {self.final_p_MeV:.3f} MeV/c').format(**locals()))
        self.calc_level = CALC_MOM

    @timeit
    @requires_calc_level(INIT_ARRAYS)
    def calcMagneticFieldMap(self):
        """Calculate the magnetic field map for given solenoid and BC currents."""
        # Is b_field a tuple? Then it has coefficients describing how the B-field depends on the sol/BC currents.
        if isinstance(self.b_field, tuple):
            X = self.bc_current * self.b_field.bc_turns / self.b_field.bc_area
            Y = self.sol_current * self.b_field.sol_turns / self.b_field.sol_area
            # Use a subset of coefficients
            A = np.array(
                [Y, Y ** 2, Y ** 3, X, X * Y, X * Y ** 2, X ** 2, X ** 2 * Y,
                 X ** 2 * Y ** 2, X ** 2 * Y ** 3, X ** 3, X ** 3 * Y]).T
            field_map = np.dot(self.b_field.coeffs, A)
            self.B = interpolate(self.b_field.z_map, field_map)

        else:  # we've defined it as just an array, multiply by sol current to get field
            z_map, B_map = self.b_field
            self.B = interpolate(z_map, B_map * self.sol_current)

        # Normalised b-field (note lower case)
        self.b = lambda z: self.B(z) * -e / (2 * m * c)
        self.calc_level = CALC_B_MAP

    @timeit
    @requires_calc_level(CALC_B_MAP)
    def calcLarmorAngle(self):
        # start conditions
        if not self.quiet:
            fs = u'''Calculating Larmor angle.
Peak field: {self.rf_peak_field:.3f} MV/m
Phase: {self.phase:.1f}°
Solenoid current: {self.sol_current:.3f} A
Solenoid maximum field: {Bmax_sol:.3f} T
Bucking coil current: {self.bc_current:.3f} A'''
            print(fs.format(Bmax_sol=self.getPeakMagneticField(), **locals()))
        theta_L = 0

        # calculation
        b_mid = self.b(self.z_array[:-1] + self.dz / 2)
        p_i = self.p_array[:-1]
        p_f = self.p_array[1:]
        gamma_i = self.gamma_array[:-1]
        gamma_f = self.gamma_array[1:]
        delta_theta_L = np.zeros_like(self.z_array[:-1])
        gamma_dash = self.gamma_dash_array[:-1]
        mask = gamma_dash == 0
        delta_theta_L[mask] = b_mid[mask] * self.dz / p_f[mask]
        delta_theta_L[~mask] = (b_mid[~mask] / gamma_dash[~mask]) * np.log(
            (p_f[~mask] + gamma_f[~mask]) / (p_i[~mask] + gamma_i[~mask]))
        self.theta_L_array = np.cumsum(np.insert(delta_theta_L, 0, 0))

        self.calc_level = CALC_LA
        if not self.quiet:
            fs = u'Final Larmor angle: {:.3f}°'
            print(styleOutput(fs).format(self.getFinalLarmorAngle()))

    @timeit
    @requires_calc_level(CALC_LA)
    def calcMatrices(self):
        if not self.quiet:
            fs = styleOutput(u'''Calculating matrices.
Peak field: {self.rf_peak_field:.3f} MV/m
Phase: {self.phase:.1f}°
Solenoid current: {self.sol_current:.3f} A
Solenoid maximum field: {Bmax_sol:.3f} T
Bucking coil current: {self.bc_current:.3f} A''')
            print(fs.format(Bmax_sol=self.getPeakMagneticField(), **locals()))

        # total matrix
        M_total = np.identity(4)

        # calculation
        omega = 2 * np.pi * self.freq
        b_mid = self.b(self.z_array[:-1] + self.dz / 2)
        delta_theta_L = np.ediff1d(self.theta_L_array)
        C = np.cos(delta_theta_L)
        S = np.sin(delta_theta_L)
        gamma_i = self.gamma_array[:-1]
        gamma_f = self.gamma_array[1:]
        beta_i = self.beta_array[:-1]
        beta_f = self.beta_array[1:]
        t_i = self.t_array[:-1]
        t_f = self.t_array[1:]
        p_i = self.p_array[:-1]
        p_f = self.p_array[1:]
        # gamma_dash = self.gamma_tilde_dash * np.cos(omega * t_i)

        # thin lens focusing due to rising edge of RF field
        mask = self.gamma_tilde_dash[:-1] == 0  # i.e. where E-field starts from zero
        M1 = np.zeros((len(self.z_array) - 1, 4, 4))
        M1[:] = np.identity(4)
        gamma_dash = self.gamma_dash_array[:-1]
        off_diag = -gamma_dash[mask] / (2 * gamma_i[mask] * beta_i[mask] ** 2)
        M1[mask, 1, 0] = off_diag
        M1[mask, 3, 2] = off_diag

        # rotation matrix due to solenoid field (identity matrix where field == 0)
        mask = b_mid == 0
        M2 = np.zeros((len(self.z_array) - 1, 4, 4))
        M2[mask] = np.identity(4)
        M2_nonzero = np.array([[C[~mask], p_i[~mask] * S[~mask] / b_mid[~mask]],
                              [-b_mid[~mask] * S[~mask] / p_f[~mask], p_i[~mask] * C[~mask] / p_f[~mask]]])
        off_diag = np.array([[S[~mask], np.zeros_like(S[~mask])], [np.zeros_like(S[~mask]), S[~mask]]])
        # A bit of funky transposing is required here so the axes are correct
        M2_nonzero = np.vstack((np.hstack((M2_nonzero, off_diag)), np.hstack((-off_diag, M2_nonzero)))).transpose((2, 0, 1))
        M2[~mask] = M2_nonzero

        # focusing term due to RF magnetic focusing
        M3 = np.zeros((len(self.z_array) - 1, 4, 4))
        M3[:] = np.identity(4)
        # off_diag = np.cos(omega * t_i) * self.gamma_tilde_dash[:-1] * (1 - np.cos(omega * (t_f - t_i))) / (2 * gamma_f)
        off_diag = Re(self.gamma_tilde_dash[:-1] * (1 - np.exp(1j * omega * (t_f - t_i))) * np.exp(1j * omega * t_i)) / (2 * gamma_f)
        M3[:, 1, 0] = off_diag
        M3[:, 3, 2] = off_diag

        # thin lens focusing due to falling edge of RF field
        M4 = np.zeros((len(self.z_array) - 1, 4, 4))
        M4[:] = np.identity(4)
        mask = self.gamma_tilde_dash[1:] == 0  # i.e. where E-field goes to zero
        gtd = self.gamma_tilde_dash[:-1]
        off_diag = gtd[mask] * np.cos(omega * t_f[mask]) / (2 * gamma_f[mask] * beta_f[mask] ** 2)
        M4[mask, 1, 0] = off_diag
        M4[mask, 3, 2] = off_diag

        # output CSV files
        # np.savetxt('m1-rst.csv', M1.reshape(-1, 16), delimiter=',')
        # np.savetxt('m2-rst.csv', M2.reshape(-1, 16), delimiter=',')
        # np.savetxt('m3-rst.csv', M3.reshape(-1, 16), delimiter=',')
        # np.savetxt('m4-rst.csv', M4.reshape(-1, 16), delimiter=',')

        self.M_array = np.matmul(np.matmul(np.matmul(M1, M2), M3), M4)
        self.M_total = reduce(np.dot, self.M_array)
        self.calc_level = CALC_MATRICES

    def resetValue(self, attr_name, value, calc_level):
        """General function for setting attribute value and resetting calculation level."""
        if not getattr(self, attr_name) == value:
            setattr(self, attr_name, float(value))
            # Reset calculation level
            self.calc_level = min(self.calc_level, calc_level)

    def setRFPeakField(self, field):
        """Set the peak electric field in MV/m."""
        self.resetValue('rf_peak_field', field, CALC_NONE)

    def setRFPhase(self, phase):
        """Set the RF phase in degrees."""
        self.resetValue('phase', phase, CALC_NONE)

    def setSolenoidCurrent(self, current):
        """Set the solenoid current in A."""
        self.resetValue('sol_current', current, CALC_B_MAP - 1)

    def setBuckingCoilCurrent(self, current):
        """Set the bucking coil current in A."""
        self.resetValue('bc_current', current, CALC_B_MAP - 1)

    def setDZ(self, dz):
        """Set the z step size in metres."""
        self.resetValue('dz', dz, INIT_ARRAYS - 1)

    @requires_calc_level(INIT_ARRAYS)
    def getZRange(self):
        """Return an array containing the z coordinates of the field maps."""
        return self.z_array

    @requires_calc_level(INIT_ARRAYS)
    def getRFFieldMap(self):
        """Return the electric field map produced by the RF cavity."""
        return self.norm_E(self.z_array) * self.rf_peak_field * 1e6

    @requires_calc_level(CALC_B_MAP)
    def getMagneticFieldMap(self):
        """Return the magnetic field map produced by the solenoid and bucking coil."""
        return self.B(self.z_array)

    @requires_calc_level(CALC_B_MAP)
    def getMagneticField(self, z):
        """Return the magnetic field at a given z coordinate."""
        return float(self.B(z))

    @requires_calc_level(CALC_B_MAP)
    def getPeakMagneticField(self):
        """Return the peak solenoid field in T."""
        return np.max(self.B(self.z_array))

    @requires_calc_level(CALC_MOM)
    def getMomentumMap(self):
        """Return an array showing how the momentum (in MeV/c) varies 
        along the length of the cavity."""
        return self.p_array * -1e-6 * epsilon_e

    @requires_calc_level(CALC_MOM)
    def getFinalMomentum(self):
        """Return the final momentum in MeV/c at the end of the cavity."""
        return self.final_p_MeV

    @requires_calc_level(CALC_LA)
    def getLarmorAngleMap(self):
        """Return an array showing how the Larmor angle (in degrees) varies 
        along the length of the cavity."""
        return np.degrees(self.theta_L_array)

    @requires_calc_level(CALC_LA)
    def getFinalLarmorAngle(self):
        """Return the final Larmor angle in degrees at the end of the cavity."""
        return np.degrees(self.theta_L_array[-1])

    @requires_calc_level(CALC_MATRICES)
    def getMatrixMap(self):
        """Return an array showing how the transfer matrix evolves along the 
        length of the cavity."""
        return self.M_array

    @requires_calc_level(CALC_MATRICES)
    def getOverallMatrix(self):
        """Return the overall 4x4 transfer matrix for the cavity."""
        return self.M_total

    @requires_calc_level(CALC_MATRICES)
    def trackBeam(self, u):
        """Track a particle (represented by a four-vector (x, x', y, y')) 
        through the field maps and return the final phase space coordinates."""
        if not self.quiet:
            print(styleOutput("""Particle start position:
x = {0:.3f} mm, x' = {1:.3f} mrad
y = {2:.3f} mm, y' = {3:.3f} mrad""").format(*u.A1 * 1e3, **globals()))
        for i, M in enumerate(self.M_array):
            self.u_array[i] = u.T
            u = M * u
        self.u_array[-1] = u.T
        if not self.quiet:
            print(styleOutput(u'''Particle final position:
x = {0:.3f} mm, x' = {1:.3f} mrad
y = {2:.3f} mm, y' = {3:.3f} mrad''').format(*u.A1 * 1e3, **globals()))
        return u

    def optimiseParam(self, opt_func, operation, x_name, x_units, target=None, target_units=None, tol=1e-6):
        """General function for optimising a parameter by varying another."""
        # operation should be of form "Set peak field" etc.
        x_init = getattr(self, x_name)
        if not self.quiet:
            target_text = '' if target == None else ', target {target:.3f} {target_units}'.format(**locals())
            print('{operation}{target_text}, by varying {x_name} starting at {x_init:.3f} {x_units}.'.format(**locals()))
        xopt = scipy.optimize.fmin(opt_func, x_init, xtol=1e-3, disp=False)
        # if res.success:
        if not self.quiet:
            print('Optimised with {x_name} setting of {0:.3f} {x_units}'.format(float(xopt), **locals()))
        return float(xopt)
        # else:
        #     target_text = '' if target == None else ' to find target value of {target:.3f} {target_units}'.format(**locals())
        #     fs = '{operation}: failed{target_text} around {x_name} of {x_init:.3f} {x_units}.'
        #     raise RuntimeError(fs.format(**locals()))

    def peakFieldToMomentum(self, peak_field):
        """Set an RF peak field value and return the momentum."""
        self.setRFPeakField(peak_field)
        return self.getFinalMomentum()

    def setFinalMomentum(self, momentum):
        """Set the final momentum by changing the peak electric field, and
        return the value of this field."""
        delta_p_sq = lambda pf: (self.peakFieldToMomentum(pf) - momentum) ** 2
        return self.optimiseParam(delta_p_sq, 'Set final momentum', 'rf_peak_field', 'MV/m', momentum, 'MeV/c')

    def rfParamsToMomAndGrad(self, peak_field, phase):
        """Set RF peak field and phase and return the momentum and momentum gradient."""
        self.setRFPeakField(peak_field)
        self.setRFPhase(phase)
        return np.array([self.getFinalMomentum(), self.getMomentumGradient()])

    def setFinalMomentumOnCrest(self, momentum):
        """Set the final momentum by changing the peak electric field, and
        return the value of this field."""
        delta_p_sq = lambda x: x[0] * np.sum((self.rfParamsToMomAndGrad(*x) - [momentum, 0]) ** 2)
        x_init = np.array([self.rf_peak_field, self.phase])
        if not self.quiet:
            fs = u'Set final momentum on-crest, target {momentum:.3f} MeV/c, by varying peak field starting at {0:.3f} MV/m and phase starting at {1:.3f}°.'
            print(fs.format(*x_init, **locals()))
        res = scipy.optimize.minimize(delta_p_sq, x_init)
        if res.success:
            if not self.quiet:
                print(u'Optimised with peak field setting of {0:.3f} MV/m and phase of {1:.3f}°'.format(*res.x))
            return res.x
        else:
            fs = u'Failed to find target value of {momentum:.3f} MeV/c around peak field of {0:.3f} MV/m and phase of {1:.3f}°.'
            raise RuntimeError(fs.format(*x_init, **locals()))

    def phaseToMomentum(self, phase):
        """Set a phase and return the momentum."""
        self.setRFPhase(phase)
        return self.getFinalMomentum()

    def crestCavity(self):
        """Maximise the output momentum by changing the RF phase, and return 
        the value of this phase."""
        return self.optimiseParam(lambda ph: -self.phaseToMomentum(ph), 'Crest cavity', 'phase', 'degrees', tol=1e-4)

    def getMomentumGradient(self):
        """Make a slight change to the phase and measure the gradient dp/dphi."""
        dphi = 0.5
        orig_phase = self.phase
        p0 = self.phaseToMomentum(orig_phase - dphi / 2)
        p1 = self.phaseToMomentum(orig_phase + dphi / 2)
        self.setRFPhase(orig_phase)
        return (p1 - p0) / dphi

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

    def solCurrentToLarmorAngle(self, sol_current):
        self.setSolenoidCurrent(sol_current)
        return self.getFinalLarmorAngle()

    def setLarmorAngle(self, angle):
        """Set the Larmor angle to a given value (in degrees) by changing the 
        solenoid current, and return the value of this current."""
        delta_thl_sq = lambda soli: (self.solCurrentToLarmorAngle(soli) - angle) ** 2
        return self.optimiseParam(delta_thl_sq, 'Set Larmor angle', 'sol_current', 'A', angle, 'degrees')

    def plotVsZ(self, arrays, ylabel, title, labels=('',), show=True):
        arrays = np.array(arrays)
        if len(arrays.shape) == 1:
            arrays = np.array([arrays])
        for array, label in zip(arrays, labels):
            plt.plot(self.z_array, array, label=label)
        plt.xlabel('z [m]')
        plt.ylabel(ylabel)
        plt.grid()
        plt.title(title)
        if not labels == ('',):
            plt.legend(loc='best')
        if show:
            plt.show()

    def plotTwo(self, arrays1, xlabel1, title1, arrays2, xlabel2, title2, labels1=('',), labels2=('',)):
        """Show two plots, one above the other."""
        plt.subplot(2, 1, 1)
        self.plotVsZ(arrays1, xlabel1, title1, labels=labels1, show=False)
        plt.subplot(2, 1, 2)
        self.plotVsZ(arrays2, xlabel2, title2, labels=labels2, show=False)
        plt.show()

    def plotLAM(self):
        """"Plot Larmor angle and momentum versus z."""
        self.plotTwo(self.getLarmorAngleMap(), r'$\theta_L [\degree]$', 'Larmor angle',
                     self.getMomentumMap(), 'p [MeV/c]', 'Momentum')

    def plotXY(self):
        """"Plot x, x', y, y' versus z."""
        self.plotTwo(1e3 * self.u_array[:, :3:2].T, 'x, y [mm]', 'Particle position',
                     1e3 * self.u_array[:, 1::2].T, "x', y' [mrad]", 'Particle angle', labels1=('x', 'y'), labels2=("x'", "y'"))

    def plotRTheta(self):
        u"""Plot r and θ versus z."""
        self.plotTwo(1e3 * np.sqrt(np.sum(self.u_array[:, :3:2] ** 2, 1)), 'r [mm]', 'Particle radius',
                     np.degrees(np.arctan2(*self.u_array[:, :3:2].T)), r"$\theta [\degree]$", 'Particle angle')


if __name__ == '__main__':
    gun10_new = RFSolTracker('Gun-10', quiet=True)
    gun10_new.setRFPhase(330)
    # gun10_new = RFSolTracker('gb-rf-gun', quiet=False)
    # gun10_new.setRFPhase(300)
    gun10_new.getFinalMomentum()
    gun10_new.getMagneticFieldMap()
    gun10_new.getFinalLarmorAngle()
    # print(gun10_new.getOverallMatrix())
    gun10_new.trackBeam(np.matrix([0.001, 0, 0, 0]).T)
    gun10_new.plotLAM()
    gun10_new.plotXY()
