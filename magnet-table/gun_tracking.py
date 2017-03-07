#!python2
# -*- coding: utf-8 -*-
"""
Generate matrices for propagating electron beams through RF and solenoid fields
See Gulliford and Bazarov (2012): http://journals.aps.org/prab/abstract/10.1103/PhysRevSTAB.15.024002#fulltext

@author: bjs54
"""

class ReturnsBlank():
    def __getattr__(self, attr):
        return ''

import scipy.constants
import scipy.interpolate
import numpy as np
import xlrd
import matplotlib.pyplot as plt
from functools32 import lru_cache
import re
try:
    from colorama import init, Fore, Back, Style # for coloured text in the terminal!
    init(autoreset=True)
except ImportError:
    Fore = Back = Style = ReturnsBlank()

# notation
Re = lambda x: x.real

# constants
m = scipy.constants.electron_mass
c = scipy.constants.speed_of_light
e = -scipy.constants.elementary_charge
epsilon_e = m * c**2 / e


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

zero_matrix = np.matrix([[0, 0], [0, 0]])
def padToM4(m):
    "Pad out a 2x2 matrix with zeros in the top-right and bottom-left quadrants to make a 4x4 matrix."
    return np.vstack([np.hstack([m, zero_matrix]), 
                      np.hstack([zero_matrix, m])])

format_codes = re.compile('({[^}]+})')
def styleOutput(string):
    """Style the formatting of output text.
    Set the first line to be cyan, and all the {}-formatted numbers to be bright."""
    string = format_codes.sub(r'{Style.BRIGHT}\1{Style.NORMAL}', string)
    lines = string.split('\n')
    if len(lines) > 0:
        lines[0] = '{Fore.CYAN}' + lines[0] + '{Fore.WHITE}'
    return '\n'.join(lines)

class GunTracker(object):
    """Import cavity and solenoid field maps for a given gun configuration,
    and track particles through them."""
        
    # Link the RI and SI properties
    def __getattribute__(self, name):
        if name == 'riWithPol':
            name = 'siWithPol'
        return super(GunTracker, self).__getattribute__(name)

    def __init__(self, gun, quiet=True):
        self.quiet = quiet
        # These properties are useful when accessing this class from the magnet table.
        self.magnetBranch = 'UNKNOWN_MAGNET_BRANCH'
        self.magType = 'GUN'
        self.riTolerance = 0.001 # fairly arbitrary
        self.fieldIntegralCoefficients = np.array([1, 0])
        self.magneticLength = None
        self.pvRoot = 'INJ-RF-GUN-01:' # totally made up!
        
        self.name = gun
        self.gun_list = ('gb-rf-gun', 'gb-dc-gun', 'Gun-10')
        # scale factors for electric and magnetic fields
        self.E_scaling = 1
        self.sol_scaling = 1
        self.bc_scaling = 1
        if not gun in self.gun_list:
            raise NotImplementedError(Fore.RED + 'Unknown gun "{gun}". Valid guns are {self.gun_list}.'.format(**locals()))
        elif gun == 'Gun-10':
            #B
            gun10_folder = r'\\fed.cclrc.ac.uk\Org\NLab\ASTeC\Projects\CLARA\Accelerator Physics\ASTRA\Archive from Delta + CDR\\'
            self.measurementDataLocation = gun10_folder

            gun10_bc_fieldmap_file = gun10_folder + 'bucking_coil_mod.txt'
            gun10_bc_fieldmap = np.loadtxt(gun10_bc_fieldmap_file, delimiter='\t')
            self.Bmax_bc = np.max(gun10_bc_fieldmap[:,1])
            self.nom_bc_current = 5.0 #TODO: set a more accurate value
            # Note the minus sign below - by convention the sol field is +ve and the BC field -ve
            # (gives a +ve change in Larmor angle for electrons) ↓ here
            B_gun10_bc = interpolate(gun10_bc_fieldmap[:,0],     -gun10_bc_fieldmap[:,1])
            gun10_sol_fieldmap_file = gun10_folder + 'modgunsol.txt'
            gun10_sol_fieldmap = np.loadtxt(gun10_sol_fieldmap_file, delimiter='\t')
            self.Bmax_sol = np.max(gun10_sol_fieldmap[:,1])
            self.nom_sol_current = 300.0 #TODO: set a more accurate value
            B_gun10_sol = interpolate(gun10_sol_fieldmap[:,0], gun10_sol_fieldmap[:,1])
            B_gun10 = lambda z: B_gun10_bc(z) * self.bc_scaling + B_gun10_sol(z) * self.sol_scaling
            # normalised field
            self.b = lambda z: B_gun10(z) * -e / (2 * m * c)
            
            #E
        #    gun_grad = 80 * 1e6 #V/m
            gun10_cav_fieldmap_file = gun10_folder + 'bas_gun.txt'
            gun10_cav_fieldmap = np.loadtxt(gun10_cav_fieldmap_file, delimiter='\t')
            self.Emax = np.max(gun10_cav_fieldmap[:,1])
            E_gun10 = interpolate(gun10_cav_fieldmap[:,0], gun10_cav_fieldmap[:,1])
            self.E = lambda z: E_gun10(z) * self.E_scaling
            self.freq = 2998.5 * 1e6
            
            self.dz = 0.5e-3 # OK to get within 0.5% of final momentum
            self.z_end = 0.32 # OK to get within 0.5% of final Larmor angle
            self.gamma_start = np.sqrt(1 + abs(1 / epsilon_e)) # 1 eV
            self.t_start = 0e-10
        
        elif gun[:3] == 'gb-':
            if gun == 'gb-dc-gun':
                sheet_name = 'G-B Fig 1 DC gun + sol'
                self.freq = 0
                dz = 1e-3
                self.z_end = 0.6
                self.gamma_start = np.sqrt(1 + abs(1 / epsilon_e)) # 1 eV
                self.t_start = 0
            elif gun == 'gb-rf-gun':
                sheet_name = 'G-B Fig 5 RF gun + sol'
                self.freq = 1.3 * 1e9
                dz = 0.1e-3
                self.z_end = 0.3
                self.gamma_start = np.sqrt(1 + abs(1 / epsilon_e)) # 1 eV
                self.t_start = 6.32e-10
            
            #TODO: should be on the server!
            fieldmap_folder = r'C:\Documents\CLARA'
            fieldmap_filename = fieldmap_folder + r'\Gun and solenoid field maps.xlsx'
            self.measurementDataLocation = fieldmap_folder
            book = xlrd.open_workbook(fieldmap_filename)
            sheet = book.sheet_by_name(sheet_name)
            z_list = numbersInColumn(sheet, 0)
            E_list = numbersInColumn(sheet, 1) * 1e6 #convert to V/m
            self.Emax = np.max(E_list)
            E_gb = interpolate(z_list, E_list)
            self.E = lambda z: E_gb(z) * self.E_scaling
            
            z_list = numbersInColumn(sheet, 2)
            B_list = numbersInColumn(sheet, 4)
            self.Bmax_bc = None
            self.nom_bc_current = None
            self.Bmax_sol = np.max(B_list)
            self.nom_sol_current = 300.0 # just a made-up number
            B_gb = interpolate(z_list, B_list)
            # normalised field
            self.b = lambda z: B_gb(z) * self.sol_scaling * -e / (2 * m * c)

        self.omega = 2 * np.pi * self.freq
        self.E_scaling = self.bc_scaling = self.sol_scaling = 1
        self.phase = np.degrees(self.t_start * self.omega)
        self.siWithPol = self.phase
        self.gradient = self.E_scaling * self.Emax / 1e6
        if self.Bmax_bc is not None: self.bc_field = self.bc_scaling * self.Bmax_bc
        self.sol_field = self.sol_scaling * self.Bmax_sol
        self.initialiseArrays()
        if not self.quiet:
            print(styleOutput('''Initialised gun: {gun}.
Frequency: {f:.4f} GHz
Maximum cavity field: {Emax:.1f} MV/m
Maximum solenoid field: {Bmax:.3f} T
z step: {dz:.3f} mm''').format(gun=gun, f=self.omega/(2*np.pi*1e9), Emax=self.Emax/1e6, 
                              Bmax=self.Bmax_sol, dz=self.dz*1e3, **globals()))

    def initialiseArrays(self):        
        # arrays to store results
        self.z_array = np.arange(0, self.z_end, self.dz)
        self.t_array = np.zeros_like(self.z_array)
        self.gamma_array = np.zeros_like(self.z_array)
        self.beta_array = np.zeros_like(self.z_array)
        self.p_array = np.zeros_like(self.z_array)
        self.theta_L_array = np.zeros_like(self.z_array)
        self.u_array = np.zeros((len(self.z_array), 4))
        self.M_array = np.zeros((len(self.z_array), 4, 4))

    def calculate(self, gradient=None, phase=None, 
                  sol_field=None, bc_field=None, dz=None):
        """Calculate the final momentum and Larmor angle for a given set of conditions.
           Specify any of gradient [MV/m], phase [°], sol_field [T] and bc_field [T].
           If a parameter is not specified, the previous value will be used."""
        if gradient is not None:
            self.gradient = gradient
            self.E_scaling = gradient * 1e6 / self.Emax
        if phase is not None:
            self.phase = phase
            self.t_start = np.radians(phase) / self.omega
        if sol_field is not None:
            self.sol_field = max(0, sol_field)
            self.sol_scaling = sol_field / self.Bmax_sol
        if bc_field is not None and self.Bmax_bc is not None:
            self.bc_field = max(0, bc_field)
            self.bc_scaling = bc_field / self.Bmax_bc
        if dz is not None:
            self.dz = dz
            self.initialiseArrays()
#        params = np.round([self.gradient, self.phase, self.sol_field, self.bc_field, self.dz], 4)
        return self.runCalculation(self.gradient, self.phase, self.sol_field, self.bc_field, self.dz)

    # Here we do the actual calculation. The @lru_cache decorator means that
    # all previous calculation results will be cached for quick access.
    # We don't actually need to access the function arguments, since they are
    # all attributes of the class.
    @lru_cache(maxsize=None)
    def runCalculation(self, grad, ph, sol, bc, dz):
        
        # start conditions
        if not self.quiet:
            print(styleOutput(u'''Running gun calculation.
Gradient: {self.gradient:.3f} MV/m
Phase: {self.phase:.1f}°
Solenoid field: {self.sol_field:.3f} T
Bucking coil field: {self.bc_field:.3f} T''').format(**dict(globals(), **locals())))
        self.t_array[0] = self.t_start
        self.gamma_array[0] = self.gamma_start
        self.beta_array[0] = np.sqrt(1 - 1 / self.gamma_start**2)
        self.p_array[0] = self.gamma_start * self.beta_array[0]
        theta_L = 0

        # total matrix
        M_total = np.identity(4)

        # calculation
        for i, z_i in enumerate(self.z_array[:-1]):
            t_i = self.t_array[i]
            gamma_i = self.gamma_array[i]
            beta_i = self.beta_array[i]
            p_i = self.p_array[i]
        
            # next value of z
            z_f = self.z_array[i+1]
            # shorthand for phasor representation of value
            phasor = lambda x: Re(x * np.exp(1j * self.omega * t_i))
#            epsilon_z = self.E((z_i + z_f) / 2)
            gamma_tilde_dash = self.E(z_i) / -epsilon_e
            gamma_dash = phasor(gamma_tilde_dash)
            gamma_z = gamma_i + gamma_dash * self.dz
            
            p_z = np.sqrt(gamma_z**2 - 1)
            beta_z = p_z / gamma_z
            b_mid = self.b((z_i + z_f) / 2)
            
            if gamma_dash == 0:
                delta_theta_L = b_mid * self.dz / p_z
                dt = 1 / (beta_z * c)
            else:
                delta_theta_L = (b_mid / gamma_dash) * np.log((p_z + gamma_z) / 
                                                              (p_i + gamma_i))
                dt = (1 / (gamma_dash * c)) * (p_z - p_i)
        #    delta_theta_L = b_mid * dz / ((p_z + p_i) / 2)
            theta_L += delta_theta_L
            t_z = t_i + dt
            
            # final values
            t_f = t_z
            gamma_f = gamma_z
            beta_f = beta_z
            p_f = p_z
            dt = t_f - t_i
            
            # thin lens focusing due to rising edge of RF field
            if self.E(z_i) == 0:
                M1 = padToM4(np.matrix([[1, 0], 
                        [-phasor(gamma_tilde_dash) / (2 * gamma_i * beta_i**2), 1]]))
            else:
                M1 = np.identity(4)
            
            # rotation matrix due to solenoid field
            C = np.cos(delta_theta_L)
            S = np.sin(delta_theta_L)
            M2 = padToM4(np.matrix([[ C,               p_i * S / b_mid], 
                                    [-b_mid * S / p_f, p_i * C / p_f  ]]))
            M2[:2,2:] = np.matrix([[ S, 0], [0,  S]]) #top right
            M2[2:,:2] = np.matrix([[-S, 0], [0, -S]]) #bottom left
            
            # focusing term due to RF magnetic focusing
            M3 = padToM4(np.matrix([[1,                                                                0], 
                            [phasor(gamma_tilde_dash * (1 - np.exp(1j * self.omega * dt))) / (2 * gamma_f), 1]]))
            
            # thin lens focusing due to falling edge of RF field
            if self.E(z_f) == 0:
                M4 = padToM4(np.matrix([[1, 0], 
                             [Re(gamma_tilde_dash * np.exp(1j * self.omega * t_f)) / (2 * gamma_f * beta_f**2), 1]]))
            else:
                M4 = np.identity(4)
            
            M_i_4 = M4 * M3 * M2 * M1
            self.M_array[i] = M_i_4
            M_total = M_i_4 * M_total
            
            # store result
            self.t_array[i+1] = t_f
            self.gamma_array[i+1] = gamma_f
            self.beta_array[i+1] = beta_f
            self.p_array[i+1] = p_f
            self.theta_L_array[i+1] = theta_L
        
        p_MeV = p_f * -1e-6 * epsilon_e
        th_deg = np.degrees(theta_L)
        if not self.quiet:
            fs = u'Final values:\nMomentum: {p_MeV:.3f} MeV\nLarmor angle: {th_deg:.3f}°'
            print(styleOutput(fs).format(**dict(globals(), **locals())))
        return p_MeV, th_deg

    def track(self, u):
        "Track a particle (represented by a four-vector (x, x', y, y')) through the fields maps."
        if not self.quiet:
            print(styleOutput("""Particle start position:
x = {0:.3f} mm, x' = {1:.3f} mrad
y = {2:.3f} mm, y' = {3:.3f} mrad""").format(*u.A1*1e3, **globals()))
        for i, M in enumerate(self.M_array):
            self.u_array[i] = u.T
            u = M * u
        if not self.quiet:
            print(styleOutput(u'''Particle final position:
x = {0:.3f} mm, x' = {1:.3f} mrad
y = {2:.3f} mm, y' = {3:.3f} mrad''').format(*u.A1*1e3, **globals()))
        return u

    def setMomentum(self, p):
        "Find the value of gradient that produces a particle with the given momentum (in MeV)."
        delta_p = lambda grad: self.calculate(gradient=grad)[0] - p
        return scipy.optimize.brentq(delta_p, 0.0, self.Emax * 2 / 1e6, xtol=1e-3)

    def setLarmorAngle(self, theta):
        "Find the value of solenoid field that rotates a particle through the given Larmor angle (in degrees)."
        if not self.quiet:
            print(u'{Fore.GREEN}Setting Larmor angle to {}°'.format(theta, **globals()))
        delta_theta = lambda sol_B: self.calculate(sol_field=sol_B)[1] - theta
        sol_field = scipy.optimize.brentq(delta_theta, 0, self.Bmax_sol * 2, xtol=1e-3)
        if not self.quiet:
            print('{Fore.GREEN}Found solenoid field: {} T{Fore.WHITE}'.format(sol_field, **globals()))
        self.calculate(sol_field=sol_field)
        return sol_field

    def cathodeField(self, sf=None):
        "Set the bucking coil scaling factor, and return the field at the cathode."
        if sf is not None: self.bc_scaling = sf
        return self.b(0) * 2*m*c / -e

    def setCathodeField(self, field):
        "Find the value of BC field that sets the cathode field to the given value (in T)."
        if not self.quiet:
            print(u'{Fore.GREEN}Setting field at cathode to {} T{Fore.WHITE}'.format(field, **globals()))
        delta_B = lambda sf: self.cathodeField(sf) - field
        bc_field = self.Bmax_bc * scipy.optimize.brentq(delta_B, 0, 2, xtol=1e-3)
        if not self.quiet:
            print('{Fore.GREEN}Found BC field: {} T{Fore.WHITE}'.format(bc_field, **globals()))
        return bc_field

    def plotLAM(self):
        "Plot Larmor angle and momentum versus z."
        self.plotVsZ((np.degrees(self.theta_L_array),), r'$\theta_L [\degree]$', 'Larmor angle')
        self.plotVsZ((self.p_array * -1e-6 * epsilon_e,), 'p [MeV/c]', 'Momentum')
    
    def plotXY(self):
        "Plot x, x', y, y' versus z."
        self.plotVsZ(np.transpose([[ui.item(0) * 1e3, ui.item(2) * 1e3] for ui in self.u_array]), 
                'x, y [mm]', 'Particle position', labels=('x', 'y'))
        self.plotVsZ(np.transpose([[ui.item(1) * 1e3, ui.item(3) * 1e3] for ui in self.u_array]), 
                "x', y' [mrad]", 'Particle angle', labels=("x'", "y'"))
    
    def plotRTheta(self):
        u"Plot r and θ versus z."
        self.plotVsZ(([1e3 * np.sqrt(ui.item(0)**2 + ui.item(2)**2) for ui in self.u_array],), 'r [mm]', 'Particle radius')
        self.plotVsZ(([np.degrees(np.arctan2(ui.item(2), ui.item(0))) for ui in self.u_array],), r"$\theta [\degree]$", 'Particle angle')

    def plotVsZ(self, arrays, ylabel, title, labels=('',)):
        for ar, l in zip(arrays, labels):
            plt.plot(self.z_array, ar, label=l)
        plt.xlabel('z [m]')
        plt.ylabel(ylabel)
        plt.grid()
        plt.title(title)
        plt.legend(loc='best')
        plt.show()

if __name__ == '__main__':
    gun10 = GunTracker('Gun-10', quiet=False)
    gun10.calculate(phase=330)
    gun10.track(np.matrix([0.001, 0, 0, 0]).T)
#    gun10.plotLAM()
#    gun10.plotXY()
    