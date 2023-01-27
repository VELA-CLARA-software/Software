#!python3
# -*- coding: utf-8 -*-
"""
Parasol RF and Solenoid Tracker v1.1 - Ben Shepherd - March 2017

Sets up a simulation of a combination of RF and solenoid fields,
and calculates the final momentum and Larmor angle of a beam.
Calculates the transfer matrix.

See Gulliford and Bazarov (2012): http://journals.aps.org/prab/abstract/10.1103/PhysRevSTAB.15.024002#fulltext
"""

import os
import sys
import ctypes
from collections import namedtuple
from fractions import Fraction
from functools import wraps, reduce  # for class method decorators
import numpy as np
import scipy.constants
# import scipy.linalg
import scipy.optimize
import solenoid_field_map as sol_field_map
from calcMomentum import calcmomentum  # Fortran code to do the momentum calculation

# import clipboard  # for temporary debugging, can copy matrices into Excel

# notation
Re = lambda x: x.real

# constants
m = scipy.constants.electron_mass
c = scipy.constants.speed_of_light
e = -scipy.constants.elementary_charge
epsilon_e = m * c ** 2 / e

# figure out where the script is (or EXE file if we've been bundled)
bundle_dir = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__))
data_dir = os.path.join(bundle_dir, 'resources', 'parasol')


def millis():
    # http://stackoverflow.com/questions/38319606/how-to-get-millisecond-and-microsecond-resolution-timestamps-in-python
    """Return a timestamp in milliseconds (ms)."""
    tics = ctypes.c_int64()
    freq = ctypes.c_int64()
    # get ticks on the internal ~2MHz QPC clock
    ctypes.windll.Kernel32.QueryPerformanceCounter(ctypes.byref(tics))
    # get the actual freq. of the internal ~2MHz QPC clock
    ctypes.windll.Kernel32.QueryPerformanceFrequency(ctypes.byref(freq))
    return tics.value * 1e3 / freq.value


def timeit(method):
    # https://www.andreas-jung.com/contents/a-python-decorator-for-measuring-the-execution-time-of-methods
    def timed(*args, **kw):
        ts = millis()
        result = method(*args, **kw)
        dt = millis() - ts
        if not args[0].quiet:  # args[0] is always self
            print('{method.__name__} ({args}, {kw}) {dt:.3f} ms'.format(**locals()))
        return result

    return timed


# Calculation levels
# When parameters are changed, the calculation level is reset.
# A calculation will be performed again when necessary.
# This means that the calculation can be split up into sections.
# For instance, if the solenoid current is changed this will not affect
# the momentum, so no need to recalculate that.
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


# Devices (guns/linacs) that we know about.
# The ones prefixed 'gb-' are referenced in the Gulliford/Bazarov paper.
MODEL_LIST = ('gb-rf-gun', 'gb-dc-gun', 'Gun-10', 'Gun-400', 'Linac1')

field_map_attr = namedtuple('field_map_attr', 'coeffs z_map bc_area bc_turns sol_area sol_turns')

__all__ = ['RFSolTracker', ]


class RFSolTracker(object):
    """Simulation of superimposed RF and solenoid fields."""

    def __init__(self, name, quiet=True):
        """Initialise the class, setting parameters relevant to the named setup."""
        self.M_total = None
        self.final_p_MeV = None
        self.p_array = None
        self.beta_array = None
        self.gamma_array = None
        self.t_array = None
        self.b = None
        self.M_array = None
        self.u_array = None
        self.gamma_dash_array = None
        self.delta_theta_L = None
        self.theta_L_array = None
        self.gamma_tilde_dash = None
        self.z_array = None
        self.quiet = quiet
        if name not in MODEL_LIST:
            raise NotImplementedError(f'Unknown model "{name}". Valid models are {MODEL_LIST}.')
        self.name = name

        # Set up the simulation
        self.solenoid = sol_field_map.Solenoid(name, quiet=self.quiet)
        # from \\fed.cclrc.ac.uk\Org\NLab\ASTeC-TDL\Projects\tdl-1168 CLARA\CLARA-ASTeC Folder\Accelerator Physics\ASTRA
        if name[:3] == 'Gun':
            cav_fieldmap_file = os.path.join(data_dir, 'bas_gun.txt' if name == 'Gun-10' else 'HRRG_1D_RF.dat')

            # Read in RF field map and normalise so peak = 1
            cav_fieldmap = np.loadtxt(cav_fieldmap_file, delimiter='\t')

            self.rf_peak_field = 50  # float(np.max(cav_fieldmap[:, 1]) / 1e6)  # set a 'reasonable' value
            # Normalise
            cav_fieldmap[:, 1] /= np.max(cav_fieldmap[:, 1])
            self.norm_E = [sol_field_map.interpolate(*cav_fieldmap.T), ]
            self.phase_offset = np.zeros(1, dtype='float')
            self.freq = 2998.5 * 1e6  # in Hz
            self.phase = 330.0  # to get optimal acceleration

            # Set parameters
            self.dz = 0.5e-3  # in metres - OK to get within 0.5% of final momentum
            self.gamma_start = np.sqrt(1 + abs(1 / epsilon_e))  # 1 eV

            self.z_start = 0
            self.z_end = 0.981  # location of screen # max(cav_fieldmap[-1, 1], self.solenoid.getZMap()[-1])

        elif name == 'Linac1':

            def fetch_dat(part):
                # Some of this (Mathematica-exported) data is in fraction form (e.g. 2/25), so we need to convert it
                return np.loadtxt(os.path.join(data_dir, f'L1{part}cell.dat'), encoding='utf-8', converters={0: Fraction})

            entrance_data = fetch_dat('entrance')
            single_cell_data = fetch_dat('single')
            exit_data = fetch_dat('exit')
            grad_phase_data = np.loadtxt(os.path.join(data_dir, 'RI_linac_grad_phase_error.txt'))
            # convert from percentage of first to fraction of max
            rel_grads = grad_phase_data[:, 0] / np.max(grad_phase_data[:, 0])
            self.phase_offset = np.cumsum(np.radians(-grad_phase_data[:, 1]))
            n_cells = len(grad_phase_data)

            self.freq = 2998.5 * 1e6  # in Hz
            self.phase = 330.0  # to get optimal acceleration - TODO: not tested
            self.rf_peak_field = 50  # MV/m, just a made-up figure at the moment (TODO)

            data_z_length = entrance_data[-1, 0] - entrance_data[0, 0]

            def interpolate(xy):
                return scipy.interpolate.interp1d(*xy.T, fill_value=0, bounds_error=False)

            ent_interp = interpolate(entrance_data)
            sgl_interp = interpolate(single_cell_data)
            exit_interp = interpolate(exit_data)

            cell_length = 0.033327  # from document: \\fed.cclrc.ac.uk\Org\NLab\ASTeC-TDL\Projects\tdl-1168 CLARA\CLARA-ASTeC Folder\Accelerator Physics\ASTRA\Injector\CLARA v10 Injector Simulations v0.3.docx
            self.dz = 0.001
            z_length = n_cells * cell_length + data_z_length  # include a bit extra at the ends
            # self.z_start = -z_length / 2
            # self.z_end = z_length / 2
            z_map = self.solenoid.get_z_map()
            self.z_start = z_map[0]
            self.z_end = z_map[-1]
            # TODO: self.dz =
            self.norm_E = []
            self.gamma_start = np.sqrt(1 + abs(4e6 / epsilon_e) ** 2)  # 4 MeV

            n_offset = (n_cells - 1) / 2
            for i in range(n_cells):
                interp = ent_interp if i == 0 else exit_interp if i == n_cells - 1 else sgl_interp
                self.norm_E.append(
                    scipy.interpolate.interp1d(z_map, rel_grads[i] * interp(z_map + (n_offset - i) * cell_length),
                                               fill_value=0, bounds_error=False))

        elif name.startswith('gb-'):
            self.gamma_start = np.sqrt(1 + abs(1 / epsilon_e))  # 1 eV
            self.z_start = 0
            if name == 'gb-dc-gun':
                self.freq = 0
                self.dz = 1e-3
                self.z_end = 0.6
                self.phase = 0
            elif name == 'gb-rf-gun':
                self.freq = 1.3e9
                self.dz = 1e-4
                self.z_end = 0.3
                self.phase = 295  # to get optimal acceleration

            z_list, E_list = np.loadtxt(os.path.join(data_dir, 'gb-field-maps', f'{name}_e-field.csv'), delimiter=',').T
            self.rf_peak_field = float(np.max(E_list))
            # Normalise
            E_list /= self.rf_peak_field
            self.norm_E = [sol_field_map.interpolate(z_list, E_list), ]
            self.phase_offset = [0, ]

        self.calc_level = CALC_NONE

    def __repr__(self):
        return f'<RFSolTracker {self.name}>'

    def calculate(self, level):
        """Calculate the output parameters for the given inputs."""
        if self.calc_level == CALC_NONE and level > CALC_NONE:
            self.initialise_arrays()
        if self.calc_level == INIT_ARRAYS and level > INIT_ARRAYS:
            self.calc_momentum()
        if self.calc_level == CALC_MOM and level > CALC_MOM:
            self.calc_magnetic_field_map()
        if self.calc_level == CALC_B_MAP and level > CALC_B_MAP:
            self.calc_larmor_angle()
        if self.calc_level == CALC_LA and level > CALC_LA:
            self.calc_matrices()
        if not self.quiet:
            print(f'New calculation level: {self.calc_level}')

    @timeit
    def initialise_arrays(self):
        """Initialise arrays to store results."""
        self.z_array = np.arange(self.z_start, self.z_end, self.dz)
        #        self.gamma_tilde_dash = [self.E(z) / -epsilon_e for z in self.z_array]
        self.gamma_tilde_dash = np.array(
            [norm_E(self.z_array) * self.rf_peak_field * 1e6 / -epsilon_e for norm_E in self.norm_E])
        self.theta_L_array = np.zeros_like(self.z_array)
        self.delta_theta_L = np.zeros(len(self.z_array) - 1)
        self.gamma_dash_array = np.zeros_like(self.z_array)
        self.u_array = np.zeros((len(self.z_array), 4))
        self.M_array = np.zeros((len(self.z_array), 4, 4))
        self.calc_level = INIT_ARRAYS

    @timeit
    @requires_calc_level(INIT_ARRAYS)
    def calc_momentum(self):
        """Calculate the momentum gain for a given E-field distribution."""
        # start conditions
        if not self.quiet:
            print(f'Calculating momentum gain.\nPeak field: {self.rf_peak_field:.3f} MV/m\nPhase: {self.phase:.1f}°')

        # Fortran method (0.8 ms to run cf 11 ms for Python code)
        self.t_array, self.gamma_dash_array, self.gamma_array, self.beta_array, self.p_array = \
            calcmomentum(self.freq, self.phase, self.gamma_start, self.dz, self.gamma_tilde_dash, self.phase_offset)
        # print(self.gamma_dash_array)
        self.final_p_MeV = self.p_array[-1] * -1e-6 * epsilon_e

        if not self.quiet:
            print(u'Final momentum: {:.3f} MeV/c'.format(self.final_p_MeV))
        self.calc_level = CALC_MOM

    @timeit
    @requires_calc_level(INIT_ARRAYS)
    def calc_magnetic_field_map(self):
        """Calculate the magnetic field map for given solenoid and BC currents."""
        # Normalised b-field (note lower case)
        self.solenoid.calc_magnetic_field_map()
        self.b = lambda z: self.solenoid.B_interp(z) * -e / (2 * m * c)
        self.calc_level = CALC_B_MAP

    @timeit
    @requires_calc_level(CALC_B_MAP)
    def calc_larmor_angle(self):
        # start conditions
        if not self.quiet:
            print(f'Calculating Larmor angle.\nPeak field: {self.rf_peak_field:.3f} MV/m\nPhase: {self.phase:.1f}°\n'
                  f'Solenoid current: {self.solenoid.sol_current:.3f} A\n'
                  f'Solenoid maximum field: {self.get_peak_magnetic_field():.3f} T\n'
                  f'Bucking coil current: {self.solenoid.bc_current:.3f} A')
        # calculation
        b_mid = self.b(self.z_array[:-1] + self.dz / 2)
        p_i = self.p_array[:-1]
        p_f = self.p_array[1:]
        gamma_i = self.gamma_array[:-1]
        gamma_f = self.gamma_array[1:]
        # delta_theta_L = np.zeros_like(self.z_array[:-1])
        gamma_dash = self.gamma_dash_array[:-1]
        mask = gamma_dash == 0
        self.delta_theta_L[mask] = b_mid[mask] * self.dz / p_f[mask]
        self.delta_theta_L[~mask] = (b_mid[~mask] / gamma_dash[~mask]) * np.log(
            (p_f[~mask] + gamma_f[~mask]) / (p_i[~mask] + gamma_i[~mask]))
        # np.savetxt('delta_theta_L.csv', self.delta_theta_L)
        self.theta_L_array = np.cumsum(np.insert(self.delta_theta_L, 0, 0))

        self.calc_level = CALC_LA
        if not self.quiet:
            print(f'Final Larmor angle: {self.get_final_larmor_angle():.3f}°')

    @timeit
    @requires_calc_level(CALC_LA)
    def calc_matrices(self):
        if not self.quiet:
            print(f'Calculating matrices.\nPeak field: {self.rf_peak_field:.3f} MV/m\nPhase: {self.phase:.1f}°\n'
                  f'Solenoid current: {self.solenoid.sol_current:.3f} A\n'
                  f'Solenoid maximum field: {self.get_peak_magnetic_field():.3f} T\n'
                  f'Bucking coil current: {self.solenoid.bc_current:.3f} A')

        # calculation
        omega = 2 * np.pi * self.freq
        b_mid = self.b(self.z_array[:-1] + self.dz / 2)
        # delta_theta_L = np.ediff1d(self.theta_L_array)
        C = np.cos(self.delta_theta_L)
        S = np.sin(self.delta_theta_L)
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
        mask = self.gamma_dash_array[:-1] == 0  # i.e. where E-field starts from zero
        M1 = np.zeros((len(self.z_array) - 1, 4, 4))
        M1[:] = np.identity(4)
        gamma_dash = self.gamma_dash_array[:-1]
        off_diag = -gamma_dash[mask] / (2 * gamma_i[mask] * beta_i[mask] ** 2)
        M1[mask, 1, 0] = off_diag
        M1[mask, 3, 2] = off_diag

        # rotation matrix due to solenoid field
        mask = b_mid == 0
        M2 = np.zeros((len(self.z_array) - 1, 4, 4))
        M2[mask] = np.identity(4)
        # Where b=0, we use a simplified matrix otherwise we get divide-by-zero errors
        M2[mask, 0, 1] = self.dz
        M2[mask, 2, 3] = self.dz
        M2[mask, 1, 1] = p_i[mask] / p_f[mask]
        M2[mask, 3, 3] = p_i[mask] / p_f[mask]
        M2_nonzero = np.array([[C[~mask], p_i[~mask] * S[~mask] / b_mid[~mask]],
                               [-b_mid[~mask] * S[~mask] / p_f[~mask], p_i[~mask] * C[~mask] / p_f[~mask]]])
        off_diag = np.array([[S[~mask], np.zeros_like(S[~mask])], [np.zeros_like(S[~mask]), S[~mask]]])
        # A bit of funky transposing is required here so the axes are correct
        M2_nonzero = np.vstack((np.hstack((M2_nonzero, off_diag)),
                                np.hstack((-off_diag, M2_nonzero)))).transpose((2, 0, 1))
        M2[~mask] = M2_nonzero

        # focusing term due to RF magnetic focusing
        M3 = np.zeros((len(self.z_array) - 1, 4, 4))
        M3[:] = np.identity(4)
        # off_diag = self.gamma_tilde_dash[0, :-1] * (1 - np.cos(omega * (t_f - t_i))) * np.cos(omega * t_i) / (2 * gamma_f)
        off_diag = np.sum([gtd[:-1] * (1 - np.cos(omega * (t_f - t_i))) * np.cos(omega * t_i + pho)
                           for gtd, pho in zip(self.gamma_tilde_dash, self.phase_offset)], axis=0) / (2 * gamma_f)
        M3[:, 1, 0] = off_diag
        M3[:, 3, 2] = off_diag

        # thin lens focusing due to falling edge of RF field
        M4 = np.zeros((len(self.z_array) - 1, 4, 4))
        M4[:] = np.identity(4)
        mask = self.gamma_dash_array[1:] == 0  # i.e. where E-field goes to zero
        gtd = self.gamma_tilde_dash[:, :-1]
        # off_diag = gtd[mask] * np.cos(omega * t_f[mask]) / (2 * gamma_f[mask] * beta_f[mask] ** 2)
        off_diag = np.sum([gtdj[mask] * np.cos(omega * t_f[mask] + pho)
                           for gtdj, pho in zip(gtd, self.phase_offset)]) / (2 * gamma_f[mask] * beta_f[mask] ** 2)
        M4[mask, 1, 0] = off_diag
        M4[mask, 3, 2] = off_diag

        self.M_array = np.matmul(np.matmul(np.matmul(M1, M2), M3), M4)
        self.M_total = reduce(np.dot, self.M_array[::-1])  # multiply from the right!
        self.calc_level = CALC_MATRICES

    def reset_value(self, attr_name, value, calc_level):
        """General function for setting attribute value and resetting calculation level."""
        if getattr(self, attr_name) != value:
            setattr(self, attr_name, float(value))
            # Reset calculation level
            self.calc_level = min(self.calc_level, calc_level)

    def set_initial_momentum(self, new_momentum):
        """Set the initial momentum in MeV/c."""
        self.reset_value('gamma_start', np.sqrt(1 + abs(1e6 * new_momentum / epsilon_e)), CALC_NONE)

    def set_rf_peak_field(self, field):
        """Set the peak electric field in MV/m."""
        self.reset_value('rf_peak_field', field, CALC_NONE)

    def set_rf_phase(self, phase):
        """Set the RF phase in degrees."""
        self.reset_value('phase', phase, CALC_NONE)

    def set_solenoid_current(self, current):
        """Set the solenoid current in A."""
        self.calc_level = min(self.calc_level, CALC_B_MAP - 1)
        self.solenoid.set_solenoid_current(current)  # to reset solenoid calc

    def set_bucking_coil_current(self, current):
        """Set the bucking coil current in A."""
        self.calc_level = min(self.calc_level, CALC_B_MAP - 1)
        self.solenoid.set_bucking_coil_current(current)  # to reset solenoid calc

    def set_cathode_field(self, field):
        """Set the cathode field to a given level by changing the bucking coil
        current, and return the value of this current."""
        self.calc_level = min(self.calc_level, CALC_B_MAP - 1)
        return self.solenoid.set_cathode_field(field)  # to reset solenoid calc

    def set_dz(self, dz):
        """Set the z step size in metres."""
        self.reset_value('dz', dz, INIT_ARRAYS - 1)

    @requires_calc_level(INIT_ARRAYS)
    def get_z_range(self):
        """Return an array containing the z coordinates of the field maps."""
        return self.z_array

    @requires_calc_level(INIT_ARRAYS)
    def get_rf_field_map(self, phase=0):
        """Return the electric field map produced by the RF cavity."""
        # TODO: we might want to see something else for a multi-cell cavity
        return np.sum([norm_E(self.z_array) * self.rf_peak_field * 1e6 * np.cos(pho + phase)
                       for norm_E, pho in zip(self.norm_E, self.phase_offset)], 0)

    @requires_calc_level(CALC_B_MAP)
    def get_magnetic_field_map(self):
        """Return the magnetic field map produced by the solenoid and bucking coil."""
        return self.solenoid.B_interp(self.z_array)

    @requires_calc_level(CALC_B_MAP)
    def get_magnetic_field(self, z):
        """Return the magnetic field at a given z coordinate."""
        return float(self.solenoid.B_interp(z))

    @requires_calc_level(CALC_B_MAP)
    def get_peak_magnetic_field(self):
        """Return the peak solenoid field in T."""
        return self.solenoid.get_peak_magnetic_field()

    @requires_calc_level(CALC_MOM)
    def get_momentum_map(self):
        """Return an array showing how the momentum (in MeV/c) varies
        along the length of the cavity."""
        return self.p_array * -1e-6 * epsilon_e

    @requires_calc_level(CALC_MOM)
    def get_final_momentum(self):
        """Return the final momentum in MeV/c at the end of the cavity."""
        return self.final_p_MeV

    @requires_calc_level(CALC_LA)
    def get_larmor_angle_map(self):
        """Return an array showing how the Larmor angle (in degrees) varies
        along the length of the cavity."""
        return np.degrees(self.theta_L_array)

    @requires_calc_level(CALC_LA)
    def get_final_larmor_angle(self):
        """Return the final Larmor angle in degrees at the end of the cavity."""
        return np.degrees(self.theta_L_array[-1])

    @requires_calc_level(CALC_MATRICES)
    def get_matrix_map(self):
        """Return an array showing how the transfer matrix evolves along the
        length of the cavity."""
        return self.M_array

    @requires_calc_level(CALC_MATRICES)
    def get_overall_matrix(self):
        """Return the overall 4x4 transfer matrix for the cavity."""
        return self.M_total

    @requires_calc_level(CALC_MATRICES)
    def track_beam(self, u):
        """Track a particle (represented by a four-vector (x, x', y, y'))
        through the field maps and return the final phase space coordinates."""
        if not self.quiet:
            template = "Particle start position:\nx = {0:.3f} mm, x' = {1:.3f} mrad\ny = {2:.3f} mm, y' = {3:.3f} mrad"
            print(template.format(*np.asarray(u).A1 * 1e3))
        for i, M in enumerate(self.M_array):
            self.u_array[i] = u.T
            u = M * u
        self.u_array[-1] = u.T
        if not self.quiet:
            print("Particle final position:\nx = {0:.3f} mm, x' = {1:.3f} mrad\n"
                  "y = {2:.3f} mm, y' = {3:.3f} mrad".format(*u.A1 * 1e3))
        return u

    def optimise_param(self, opt_func, operation, x_name, x_units, target=None, target_units=None, tol=1e-6):
        """General function for optimising a parameter by varying another."""
        # operation should be of form "Set peak field" etc.
        x_init = reduce(getattr, [self] + x_name.split('.'))
        if not self.quiet:
            target_text = '' if target is None else f', target {target:.3f} {target_units}'
            print(x_name, x_init)
            print(f'{operation}{target_text}, by varying {x_name} starting at {x_init:.3f} {x_units}.')
        xopt = scipy.optimize.fmin(opt_func, x_init, xtol=1e-3, disp=False)
        if not self.quiet:
            print(f'Optimised with {x_name} setting of {float(xopt):.3f} {x_units}')
        return float(xopt)

    def peak_field_to_momentum(self, peak_field):
        """Set an RF peak field value and return the momentum."""
        self.set_rf_peak_field(peak_field)
        return self.get_final_momentum()

    def set_final_momentum(self, new_momentum):
        """Set the final momentum by changing the peak electric field, and
        return the value of this field."""
        delta_p_sq = lambda pf: (self.peak_field_to_momentum(pf) - new_momentum) ** 2
        return self.optimise_param(delta_p_sq, 'Set final momentum', 'rf_peak_field', 'MV/m', new_momentum, 'MeV/c')

    def rf_params_to_mom_and_grad(self, peak_field, phase):
        """Set RF peak field and phase and return the momentum and momentum gradient."""
        self.set_rf_peak_field(peak_field)
        self.set_rf_phase(phase)
        return np.array([self.get_final_momentum(), self.get_momentum_gradient()])

    def set_final_momentum_on_crest(self, momentum):
        """Set the final momentum by changing the peak electric field, and
        return the value of this field."""
        delta_p_sq = lambda x: x[0] * np.sum((self.rf_params_to_mom_and_grad(*x) - [momentum, 0]) ** 2)
        x_init = np.array([self.rf_peak_field, self.phase])
        if not self.quiet:
            print(f'Set final momentum on-crest, target {momentum:.3f} MeV/c, by varying peak field ' \
                  'starting at {x_init[0]:.3f} MV/m and phase starting at {x_init[1]:.3f}°.')
        res = scipy.optimize.minimize(delta_p_sq, x_init)
        if not res.success:
            raise RuntimeError(f'Failed to find target value of {momentum:.3f} MeV/c '
                               'around peak field of {x_init[0]:.3f} MV/m and phase of {x_init[1]:.3f}°.')
        if not self.quiet:
            print('Optimised with peak field setting of {0:.3f} MV/m and phase of {1:.3f}°'.format(*res.x))
        return res.x

    def phase_to_momentum(self, phase):
        """Set a phase and return the momentum."""
        self.set_rf_phase(phase)
        return self.get_final_momentum()

    def crest_cavity(self):
        """Maximise the output momentum by changing the RF phase, and return the value of this phase."""
        return self.optimise_param(lambda ph: -self.phase_to_momentum(ph), 'Crest cavity', 'phase', 'degrees', tol=1e-4)

    def get_momentum_gradient(self):
        """Make a slight change to the phase and measure the gradient dp/dphi."""
        dphi = 0.5
        orig_phase = self.phase
        p0 = self.phase_to_momentum(orig_phase - dphi / 2)
        p1 = self.phase_to_momentum(orig_phase + dphi / 2)
        self.set_rf_phase(orig_phase)
        return (p1 - p0) / dphi

    def sol_current_to_larmor_angle(self, sol_current):
        self.set_solenoid_current(sol_current)
        return self.get_final_larmor_angle()

    def set_larmor_angle(self, angle):
        """Set the Larmor angle to a given value (in degrees) by changing the
        solenoid current, and return the value of this current."""

        def delta_thl_sq(sol_current):
            return (self.sol_current_to_larmor_angle(sol_current) - angle) ** 2

        return self.optimise_param(delta_thl_sq, 'Set Larmor angle', 'solenoid.sol_current', 'A', angle, 'degrees')


if __name__ == '__main__':
    gun = 'Gun-10'
    print(f'Running simulation of {gun}')
    gun10 = RFSolTracker(gun, quiet=False)
    peak_field = 50
    phase = 330
    print(f'Peak field: {peak_field:.3f}, phase {phase:.3f}°')
    gun10.set_rf_peak_field(peak_field)
    gun10.set_rf_phase(phase)
    momentum = gun10.get_final_momentum()
    print(f'Final momentum: {momentum:.3f} MeV/c')
    B_field = 0.14
    for _ in range(4):  # converge on an answer
        gun10.solenoid.set_peak_magnetic_field(B_field)
        gun10.set_cathode_field(0)
    print(f'Cathode field: {gun10.get_magnetic_field(0):.3f} with BC current of {gun10.solenoid.bc_current:.3f} A')
    print(f'Peak solenoid field: {gun10.solenoid.get_peak_magnetic_field():.3f} T')
    print(f'Solenoid current: {gun10.solenoid.sol_current:.3f} A')
    larmor_angle = gun10.get_final_larmor_angle()
    print(f'Final Larmor angle: {larmor_angle:.3f}°')
    x_init = [1, 1, 4, 1]
    n = 30000
    print(f'\nBeam tracking, {n} particles')
    matrix = gun10.get_overall_matrix()
    x0 = np.matrix([np.random.normal(0, sigma * 1e-3, n) for sigma in x_init])
    x1 = np.array([matrix.dot(x.T) for x in x0.T])
    template = "sigmas: x = {:.3f} mm, x' = {:.3f} mrad, y = {:.3f} mm, y' = {:.3f} mrad"
    print(f"Initial {template.format(*x_init)}")
    print(f'Final {template.format(*np.std(x1[:, :, 0], 0) * 1000.0)}')
