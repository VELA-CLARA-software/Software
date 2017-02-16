# -*- coding: utf-8 -*-
"""
Generate matrices for propagating electron beams through RF and solenoid fields
See Gulliford and Bazarov (2012): http://journals.aps.org/prab/abstract/10.1103/PhysRevSTAB.15.024002#fulltext

Instructions:
    Set variable 'gun' to the correct one (line 32ish below)
        "gun-10" is the VELA 10Hz gun
        "gb-dc-gun" is the DC gun example from the G&B paper (Fig 1-2)
        "gb-rf-gun" is the RF gun example from the G&B paper (Fig 5-6)
    This sets the field maps, step size, initial time (phase), energy and RF frequency
    
@author: bjs54
"""

import scipy.constants
import scipy.interpolate
import numpy as np
import xlrd
import matplotlib.pyplot as plt

# notation
Re = lambda x: x.real

# constants
m = scipy.constants.electron_mass
c = scipy.constants.speed_of_light
e = -scipy.constants.elementary_charge
epsilon_e = m * c**2 / e

# field maps

# Decide which field map to use: gb-rf-gun, gb-dc-gun, or gun-10
gun = 'gb-rf-gun'
gun = 'gun-10'
print('Using gun: ' + gun)

def interpolate(x, y):
    "Return an interpolation object with some default parameters."
    return scipy.interpolate.interp1d(x, y, fill_value='extrapolate', bounds_error=False)
    
def numbersInColumn(sheet, col):
    "Return the numeric values from a zero-indexed column in a worksheet from xlrd."
    column = [sheet.cell(r, col) for r in range(sheet.nrows)]
    return np.array([cell.value for cell in column if cell.ctype == xlrd.XL_CELL_NUMBER])

if gun == 'gun-10':
    #B
    gun10_folder = r'\\fed.cclrc.ac.uk\Org\NLab\ASTeC\Projects\CLARA\Accelerator Physics\ASTRA\Archive from Delta + CDR\\'
    gun10_bc_fieldmap_file = gun10_folder + 'bucking_coil_mod.txt'
    gun10_bc_fieldmap = np.loadtxt(gun10_bc_fieldmap_file, delimiter='\t')
    # Note the minus sign below - by convention the sol field is +ve and the BC field -ve
    # (gives a +ve change in Larmor angle for electrons) ........   ↓ here
    B_gun10_bc = interpolate(gun10_bc_fieldmap[:,0], -gun10_bc_fieldmap[:,1])
    gun10_sol_fieldmap_file = gun10_folder + 'modgunsol.txt'
    gun10_sol_fieldmap = np.loadtxt(gun10_sol_fieldmap_file, delimiter='\t')
    #DOUBLED FIELD STRENGTH
    B_gun10_sol = interpolate(gun10_sol_fieldmap[:,0], gun10_sol_fieldmap[:,1] * 1.21)
    B_gun10 = lambda z: B_gun10_bc(z) + B_gun10_sol(z)
    # normalised field
    b = lambda z: B_gun10(z) * -e / (2 * m * c)
    
    #E
#    gun_grad = 80 * 1e6 #V/m
    gun10_cav_fieldmap_file = gun10_folder + 'bas_gun.txt'
    gun10_cav_fieldmap = np.loadtxt(gun10_cav_fieldmap_file, delimiter='\t')
    E_gun10 = interpolate(gun10_cav_fieldmap[:,0], gun10_cav_fieldmap[:,1])
    E = E_gun10
    omega = 2 * np.pi * 2998.5 * 1e6
    
    dz = 0.001
    z_end = 0.45
    gamma_start = np.sqrt(1 + abs(1 / epsilon_e)) # 1 eV
    t_start = 0e-10

elif gun[:3] == 'gb-':
    if gun == 'gb-dc-gun':
        sheet_name = 'G-B Fig 1 DC gun + sol'
        omega = 0
        dz = 1e-3
        z_end = 0.6
        gamma_start = np.sqrt(1 + abs(1 / epsilon_e)) # 1 eV
        t_start = 0
    elif gun == 'gb-rf-gun':
        sheet_name = 'G-B Fig 5 RF gun + sol'
        omega = 2 * np.pi * 1.3 * 1e9
        dz = 0.01e-3
        z_end = 0.3
        gamma_start = np.sqrt(1 + abs(1 / epsilon_e)) # 1 eV
        t_start = 5.8e-10
        
    fieldmap_filename = r'C:\Documents\CLARA\Gun and solenoid field maps.xlsx'
    book = xlrd.open_workbook(fieldmap_filename)
    sheet = book.sheet_by_name(sheet_name)
    z_list = numbersInColumn(sheet, 0)
    E_list = numbersInColumn(sheet, 1) * 1e6 #convert to V/m
    E_gb_rf = interpolate(z_list, E_list)
    E = E_gb_rf
    
    z_list = numbersInColumn(sheet, 2)
    B_list = numbersInColumn(sheet, 4)
    B_gb_rf = interpolate(z_list, B_list)
    # normalised field
    b = lambda z: B_gb_rf(z) * -e / (2 * m * c)

print('''Frequency: {f:.3f} GHz
Start time: {ts:.3f} ps ({ph:.1f}° phase)
z step: {dz:.2f} mm'''.format(f=omega/(2*np.pi*1e9), ts=t_start*1e12, 
                              ph=np.degrees(t_start*omega), dz=dz*1e3))

# arrays to store results
z_array = np.arange(0, z_end, dz)
t_array = np.zeros_like(z_array)
gamma_array = np.zeros_like(z_array)
beta_array = np.zeros_like(z_array)
p_array = np.zeros_like(z_array)
theta_L_array = np.zeros_like(z_array)
u_array = []
u = np.matrix([[0.001], [0]])
#u = np.matrix([[0], [0.001]])
print("Particle starts at x = {0:.3f} mm, x' = {1:.3f} mrad".format(*u.A1))
u_array.append(u)

# start conditions

t_array[0] = t_start
gamma_array[0] = gamma_start
beta_array[0] = np.sqrt(1 - 1 / gamma_start**2)
p_array[0] = gamma_start * beta_array[0]
theta_L = 0

# total matrix
M_total = np.matrix([[1,0],[0,1]])

# calculation

for i, z_i in enumerate(z_array[:-1]):
    t_i = t_array[i]
    gamma_i = gamma_array[i]
    beta_i = beta_array[i]
    p_i = p_array[i]

    # next value of z
    z_f = z_array[i+1]
    # shorthand for phasor representation of value
    phasor = lambda x: Re(x * np.exp(1j * omega * t_i))
    epsilon_z = E((z_i + z_f) / 2)
    gamma_tilde_dash = E(z_i) / -epsilon_e
    gamma_dash = phasor(gamma_tilde_dash)
    gamma_z = gamma_i + gamma_dash * dz # is this dz correct?
    p_z = np.sqrt(gamma_z**2 - 1)
#    if gamma_dash == 0:
#        delta_theta_L = 0
#    else:
#        delta_theta_L = (b((z_i + z_f) / 2) / gamma_dash) * np.log((p_z + gamma_z) / (p_i + gamma_i))
    delta_theta_L = b((z_i + z_f) / 2) * dz / ((p_z + p_i) / 2)
    theta_L += delta_theta_L
    
#    t_z = (p_z - p_i) / (c * gamma_dash)
    beta_z = p_z / gamma_z
    t_dash = 1 / (beta_z * c)
    t_z = t_i + t_dash * dz
    
    # final values
    t_f = t_z
    gamma_f = gamma_z
    beta_f = beta_z
    p_f = p_z
    dt = t_f - t_i
    
    # store result
    t_array[i+1] = t_f
    gamma_array[i+1] = gamma_f
    beta_array[i+1] = beta_f
    p_array[i+1] = p_f
    theta_L_array[i+1] = theta_L
    
    # matrices
    
    # thin lens focusing due to rising edge of RF field
    if E(z_i) == 0:
        M1 = np.matrix([[1, 0], 
                        [-phasor(gamma_tilde_dash) / (2 * gamma_i * beta_i**2), 1]])
    else:
        M1 = np.matrix([[1,0],[0,1]])
    
    # rotation matrix due to solenoid field
    C = np.cos(delta_theta_L)
    S = np.sin(delta_theta_L)
#    print(p_i, S, z_i, b(z_i))
    if S == 0:
        M2 = np.matrix([[1,0],[0,1]])
    else:
        M2 = np.matrix([[C, p_i * S / b(z_i)], 
                        [-b(z_i) * S / p_f, p_i * C / p_f]])
    
    # focusing term due to RF magnetic focusing
    M3 = np.matrix([[1, 0], 
                    [phasor(gamma_tilde_dash * (1 - np.exp(1j * omega * dt))) / (2 * gamma_f), 1]])
    
    # thin lens focusing due to falling edge of RF field
    if E(z_f) == 0:
        M4 = np.matrix([[1, 0], [Re(gamma_tilde_dash * np.exp(1j * omega * t_f)) / (2 * gamma_f * beta_f**2), 1]])
    else:
        M4 = np.matrix([[1,0],[0,1]])
    
    M_total = M4 * M3 * M2 * M1 * M_total
    if np.isnan(M_total).any():
        break
    u = M4 * M3 * M2 * M1 * u
    u_array.append(u)
    
print('Final gamma: {:.3f}'.format(gamma_f))
def plotVsZ(ar, ylabel, title):
    plt.plot(z_array, ar)
    plt.xlabel('z [m]')
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()

plotVsZ(theta_L_array, r'$\theta_L$ [rad]', 'Larmor angle')
plotVsZ(gamma_array, r'$\gamma$', 'Gamma')
plotVsZ([ui.item(0)*1000 for ui in u_array], 'x [mm]', 'Particle position')
plotVsZ([ui.item(1)*1000 for ui in u_array], "x' [mm]", 'Particle angle')
