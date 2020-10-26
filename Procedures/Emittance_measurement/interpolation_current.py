import numpy as np
import numpy.polynomial.polynomial as poly
from copy import deepcopy
from collections import OrderedDict
import os
import matplotlib.pyplot as plt
import scipy.interpolate


def FileOpen(filename):

    if filename[-4:] != ".txt":
        filename = filename + ".txt"

    data = np.array([])

    nlines = 0

    file = open(filename, "r")  # opens on 'read' mode

    for line in file:
        nlines += 1
        data = np.append(data, np.fromstring(line, dtype=np.float, sep=','))

    file.close

    data = np.reshape(data, (nlines, int(data.size / nlines)))

    return data

def I2K_CLARA_simple(currents, beamMomentum):

    ## quad calibrations are in the magnet controller
    pfitq = np.array(FileOpen('C:\\Users\qfi29231\Documents\spawn_emittances\Emittance_GUI\QuadCalibration.txt'))

    # currents are from the experiment
    currents = np.array(currents)
    kvals = np.zeros(5)
    for n in range(5):
        kvals[n] = 0
        for p in range(4):
            kvals[n] = kvals[n] + pfitq[p][n] * currents[n] ** (3 - p)
    # k value with momentum - what is this factor of 30???
    return np.multiply(kvals, 30.0 / beamMomentum)

def plot_results(ax_pl,x,y,label, ls, marker, color):
    ax_pl.plot(x, y , label = label,ls=ls, lw=1.4, marker=marker, ms=5, color = color)
    ax_pl.tick_params('both',color='navy',labelcolor='navy')
    ax_pl.grid(True,color='navy')
    return ax_pl


if __name__=='__main__':
    beam_momentum = 40.32982511890787
    VM_strength = np.array([[-44.4098, -44.3776, -44.3322, -44.2964, -44.3157],
                  [-37.079, -37.0567, -37.0108, -36.9662, -36.9854],
                  [-29.7081, -29.6988, -29.6532, -29.597, -29.6163],
                  [-22.2791, -22.3039, -22.2592, -22.1871, -22.1873],
                  [-14.8527, -14.8572, -14.8577, -14.7914, -14.7916],
                  [-9.90182, --7.42861, -7.42883, --7.39569, -7.39578],
                  [0.0, 0.0, 0.0, 0.0, 0.0],
                  [9.90182, 7.42861, 7.42883, 7.39569, 7.39578],
                  [19.8036, 14.8572, 14.8577, 14.7914, 14.7916],
                  [29.7055, 22.3039, 22.2592, 22.1871, 22.1873],
                  [29.6108, 29.6988, 29.6532, 29.597, 29.6163],
                  [49.4387, 37.0567, 37.0108, 36.9662, 36.9854],
                  [59.2131, 44.3776, 44.3322, 44.2964, 44.3157]])

    current_array = np.linspace(-30.0, 30.0, 13)
    current_matrix = np.zeros((current_array.shape[0],5))

    k_values = np.zeros_like(current_matrix)
    coefficients_interpolation = OrderedDict()
    q_strengths = os.path.join('C:\\','Users','qfi29231','Documents','Emittance_matlab','qstrengths_matlab_05-10-20.txt')
    q_str=np.loadtxt(q_strengths,delimiter='\t')
    currents_magnet_table = np.loadtxt(os.path.join('C:\\','Users','qfi29231','Documents','Emittance_matlab','currents_VM_qstrengths.txt'),delimiter=',' )
    currents_recalculated = np.zeros_like(q_str)
    for i in np.arange(current_matrix.shape[0]):
        for j in np.arange(5):
            current_matrix[i,j] = deepcopy(current_array[i])
        k_values[i,:]=I2K_CLARA_simple(current_matrix[i,:],beam_momentum)


    np.savetxt(
        os.path.join('C:\\', 'Users', 'qfi29231', 'Documents', 'Emittance_matlab', 'test_kstrengths_05-10-20.txt'),
        k_values-VM_strength, delimiter='\t')
    for k in np.arange(5):
        coefficients_interpolation.update(
            {'QUAD-0' + str(k + 1): poly.polyfit(k_values[:, k], current_array, 5)})
        print('+++++++++++++++',poly.polyval(k_values[:, k],coefficients_interpolation['QUAD-0' + str(k + 1)]),'+++++++++')
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++')
        currents_recalculated[:, k] = deepcopy(
            poly.polyval(q_str[:, k], coefficients_interpolation['QUAD-0' + str(k + 1)]))

    np.savetxt(os.path.join('C:\\','Users','qfi29231','Documents','Emittance_matlab','currents_found_extrapolation_05-10-20.txt'),
               currents_recalculated,delimiter = ',')
    ##############################################################################
    k_interp = np.zeros_like(currents_recalculated)
    k_val_original = np.zeros_like(currents_recalculated)
    for jj in np.arange(currents_recalculated.shape[0]):
        k_interp[jj, :] = I2K_CLARA_simple(currents_recalculated[jj, :], beam_momentum)
        k_val_original[jj, :] = I2K_CLARA_simple(currents_magnet_table[jj, :], beam_momentum)

    np.savetxt(
        os.path.join('C:\\', 'Users', 'qfi29231', 'Documents', 'Emittance_matlab', 'k_found_extrapolation_05-10-20.txt'),
        k_interp, delimiter=',')

    np.savetxt(
        os.path.join('C:\\', 'Users', 'qfi29231', 'Documents', 'Emittance_matlab', 'k_original_I2K_method_05-10-20.txt'),
        k_val_original, delimiter=',')


    ######################################################

#    fig, ax = plt.subplots(3, 1)
#    colors = [plt.cm.inferno_r(i) for i in np.linspace(0.3,1,5)]
#    for i in np.arange(3,6):
#        ax[i-3] = plot_results(ax[i-3],q_str[:,i-1],currents_magnet_table[:,i-1],r'I magnet table','','o', colors[i-3])
#        ax[i-3] = plot_results(ax[i-3], q_str[:, i-1], currents_recalculated[:, i-1], r'I interpolation', '--',
#                          '', colors[i-3])
#        ax[i-3].set_title('QUAD 0'+str(i), color='navy')
#        leg = ax[i-3].legend(loc=0)
#        for line, text in zip(leg.get_lines(), leg.get_texts()):
#            text.set_color(line.get_color())####

#    plt.subplots_adjust(hspace=0.8)

#    plt.savefig(os.path.join('C:\\','Users','qfi29231','Documents','Emittance_matlab','interpolation_current_k1-22-09-20.png'),
#                format='png',dpi=120, bbox_inches='tight')

