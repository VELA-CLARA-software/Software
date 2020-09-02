import numpy as np
from copy import deepcopy
import scipy.constants
import scipy.linalg
import scipy.optimize
from collections import OrderedDict
import time
import os
import sys
import shutil
from cycler import cycler
import matplotlib.pyplot as plt


class GeneralQuadScan(object):
    """

    Parent class that has all the methods to measure the emittance values
    by reconstructing the covariance matrix at reconstruction point
    from the beamsizes and optimised quad strengths

    :ivar charge: Charge: 10 pC
    :ivar SMatrix: Antisymmetric matrix: Smatrix
    :ivar rel_gamma: Relativistic gamma: 30.0 / m_e_MeV
    :ivar qlength: Quad length: 0.1007
    :ivar dlen1: Drift length: 0.105327
    :ivar dlen2: Drift length: 0.299300
    :ivar dlen3: Drift length: 1.033333
    :ivar cov_matrix: Calculated covariance matrix at reconstruction point: np.zeros((4, 4))
    :ivar emits: Emittances of normal modes: np.zeros((2, 1))
    :ivar emits_matrix: Emittances matrix transformation:[]
    :ivar qstrengths: Optimised quad strengths: []
    :ivar Nsteps: Number of steps of quad scan:  20
    :ivar input_dist: path of the input distribution for simulation: ''
    :ivar d_matrix_step: D matrix calculated for a single set of quad values:  np.zeros((3,10))
    :ivar d_matrix: total D matrix over all quad scans: np.array([])
    :ivar beam_sizes: data obtained from observation point used to calculate the emittance: OrderedDict()
    :ivar screen_data: Data ordered obtained from observation point in order to find the cov. matrix: np.array((3*nstep,10))
    :ivar path_output: Path to store the plot of the quad scan: ''
    """
    m_e_MeV = scipy.constants.physical_constants['natural unit of energy in MeV'][0]
    Smatrix = np.array([[0, 1, 0, 0],
                        [-1, 0, 0, 0],
                        [0, 0, 0, 1],
                        [0, 0, -1, 0]])  #: Smatrix
    rel_gamma = 45.0 / m_e_MeV  #: relative gamma: 45
    qlength = 0.1007  #: Quad length: 0.1007
    dlen1 = 0.105327  #: Drift length: 0.105327
    dlen2 = 0.299300  #: Drift length:0.299300
    dlen3 = 1.033333  #:  Drift length:1.033333


    def __init__(self):
        """

        Initialisation of the object

        """
        self.__charge = 10
        self.__cov_matrix = np.zeros((4, 4))  #: Covariance Matrix at reconstruction point
        self.__cov_m_linac = np.zeros((4,4))  #: Covariance Matrix postLinac
        self.__emits = np.zeros((2, 1))  #: Emittances of normal modes
        self.__emits_matrix = []  #: Emittance transformation matrix
        self.__qstrengths = []  #: optimised values of Quad Strengths
        self.__input_dist = ''  #: Path of input distribution: ''
        self.__nsteps = 20  #: Number of steps of Quad Scan: 20
        self.d_matrix_step = np.zeros((3, 10))  #: D matrix for one set of quad strengths
        self.d_matrix = []  #: Total D matrix for all sets of quads
        self.__beam_sizes = OrderedDict()  #: Dictionary with the measured beam sizes at observation point
        self.__screen_data = []  #: Array with measured data being ordered: []
        self.__path_output = ''  #: Path where the Quad Scan plot is to be saved
        self.__screen = '' #: Screen to plot the data

    @property
    def charge(self):
        return self.__charge

    @property
    def input_dist(self):
        if self.__input_dist != '':
            return np.loadtxt(self.__input_dist)
        else:
            return self.__input_dist

    @property
    def cov_matrix(self):
        return deepcopy(self.__cov_matrix)

    @property
    def cov_m_linac(self):
        return deepcopy(self.__cov_m_linac)

    @property
    def emits(self):
        return deepcopy(self.__emits)

    @property
    def emits_matrix(self):
        return deepcopy(self.__emits_matrix)

    @property
    def qstrengths(self):
        return deepcopy(self.__qstrengths)

    @property
    def nsteps(self):  #: Number of steps of Quad Scan: 20
        return deepcopy(int(self.__nsteps))

    @property
    def beam_sizes(self):
        return self.__beam_sizes

    @property
    def screen_data(self):
        return self.__screen_data

    @property
    def path_output(self):
        return self.__path_output

    @property
    def screen(self):
        return self.__screen

    @screen.setter
    def screen(self, scr):
        self.__screen = deepcopy(scr)

    @path_output.setter
    def path_output(self, path):
        self.__path_output = deepcopy(path)

    @charge.setter
    def charge(self, charg):
        self.__charge = deepcopy(charg)

    @screen_data.setter
    def screen_data(self, scr):
        self.__screen_data = deepcopy(scr)

    @beam_sizes.setter
    def beam_sizes(self, beam_size):
        self.__beam_sizes = deepcopy(beam_size)

    @input_dist.setter
    def input_dist(self, path_dist):
        self.__input_dist = np.loadtxt(deepcopy(path_dist))

    @cov_matrix.setter
    def cov_matrix(self, matrix):
        self.__cov_matrix = deepcopy(matrix)

    @cov_m_linac.setter
    def cov_m_linac(self, matrix):
        self.__cov_m_linac = deepcopy(matrix)

    @emits.setter
    def emits(self, emits_array):
        for i_exy, emitt in enumerate(emits_array):
            self.__emits[i_exy] = deepcopy(emitt)

    @emits_matrix.setter
    def emits_matrix(self, emits_m):
        self.__emits_matrix = deepcopy(emits_m)

    @qstrengths.setter
    def qstrengths(self, qstr):
        self.__qstrengths = deepcopy(qstr)

    @nsteps.setter
    def nsteps(self, nstep):
        self.__nsteps = deepcopy(int(nstep))
        self.d_matrix = np.zeros((3 * int(self.nsteps), 10))
        self.qstrengths = np.zeros((self.nsteps, 5))

    @staticmethod
    def FileOpen(filename):
        """
        Subroutine used to read data from a text file into an array

        :parameter filename: Path of the file to be opened

        :return Numpy array : the contents of the file

        """
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

    def I2K_CLARA_simple(self, currents, beamMomentum):
        """
        Method to calculate the quad strengths from the currents

        :parameter currents: Currents

        :parameter beamMomentum: Beam Momentum

        :return k_values: for each quadrupole

        """
        # quad calibrations are in the magnet controller
        pfitq = np.array(self.FileOpen('QuadCalibration.txt'))

        # currents are from the experiment
        currents = np.array(currents)
        kvals = np.zeros(5)
        for n in range(5):
            kvals[n] = 0
            for p in range(4):
                kvals[n] = kvals[n] + pfitq[p][n] * currents[n] ** (3 - p)
        # k value with momentum - what is this factor of 30???
        kvals = kvals * 30 / beamMomentum
        return kvals

    @staticmethod
    def transfer_matrix_drift(length):
        """

        Transfer matrix for Drifts

        :parameter length: Drift length

        :return Transfer Matrix: for a drift

        """
        return np.array([[1, length, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, 1, length],
                         [0, 0, 0, 1]])

    def transfer_matrix_quad(self, k1, length):
        """

        Transfer Matrix for a Quad (Thin Lens approximation)

        :parameter k1: Quad Strength

        :parameter length: Length of the quad

        :return  Transfer matrix: for a Quad

        """
        m = deepcopy(self.transfer_matrix_drift(length))

        if not k1:
            omega = sqrt(k1)
            m = [[np.cos(omega * length), np.sin(omega * length) / omega, 0, 0],
                 [- np.sin(omega * length) * omega, np.cos(omega * length), 0, 0],
                 [0, 0, np.cosh(omega * length), np.sinh(omega * length) / omega],
                 [0, 0, np.sinh(omega * length) * omega, np.cosh(omega * length)]]

            m = np.real(np.array(m))
        return m

    def transfer_matrix_post_linac(self, q_strengths):
        """

        Transfer Matrix to be obtained at the reconstruction point

        :parameter q_strengths: Optimised quad strengths

        :return Transfer Matrix: at reconstruction point:

        """

        mq1 = self.transfer_matrix_quad(q_strengths[0], self.qlength)
        mq2 = self.transfer_matrix_quad(q_strengths[1], self.qlength)
        md1 = self.transfer_matrix_drift(self.dlen1)
        md2 = self.transfer_matrix_drift(self.dlen2)
        md3 = self.transfer_matrix_drift(self.dlen3)

        return np.matmul(md3, np.matmul(mq2, np.matmul(md2, np.matmul(mq1, md1))))

    def match_beam_divergence(self, sig_xpx, sig_ypy, q_strength):
        """

        Method to match the beam and optimise the quads (finding an elliptical beam with waist at observation point)

        :parameter sig_xpx: coupling transversal term in x

        :parameter sig_ypy:  coupling transversal term in y

        :parameter q_strength: Quad strength

        :return difference of coupling terms: to be minimise

        """
        tm = self.transfer_matrix_post_linac(q_strength)
        cm = np.matmul(np.matmul(tm, self.cov_matrix), np.transpose(tm))
        return np.square(cm[0, 1] - sig_xpx) + np.square(cm[2, 3] - sig_ypy)

    def merit_function(self, sig_xpx, sig_ypy):
        """
        Merit function to be minimise

        :parameter sig_xpx:

        :parameter sig_ypy:

        :return lambda function:  to minimise as a function of quad strength

        """
        return lambda q_str: self.match_beam_divergence(sig_xpx, sig_ypy, q_str)

    def optimising_match_divergence(self, sig_xpx, sig_ypy, q_strength):
        """
        Method to find the optimum quads

        :parameter sig_xpx: Transversal coupling term in x

        :parameter sig_ypy: Transversal coupling term in x

        :parameter q_strength: Initial guess of quad strength

        :return optimum quad strength: Optimised quad strength

        """
        return scipy.optimize.fmin(func=self.merit_function(sig_xpx, sig_ypy), x0=q_strength)

    def multiplication_d_matrix_even(self, index, transfer_matrix):
        """

        Calculation of the even terms of the D matrix from the transfer matrix

        :parameter index: even index of the general D matrix

        :parameter transfer_matrix: transfer matrix at reconstruction point

        :return self.d_matrix_step:  (filling in the d_matrix array)

        """
        i_overall = 0
        for i_dx in np.arange(int(self.d_matrix_step.shape[1] / 2) - 1):
            for i_dy in np.arange(i_dx, int(self.d_matrix_step.shape[1] / 2) - 1):
                if i_dy == i_dx:
                    self.d_matrix_step[index, i_overall] = np.square(transfer_matrix[index, i_dy])
                else:
                    self.d_matrix_step[index, i_overall] = 2.0 * transfer_matrix[index, i_dx] * transfer_matrix[
                        index, i_dy]
                i_overall += 1

    def multiplication_d_matrix_odd(self, index, transfer_matrix):
        """
            Calculation of the odd terms of the D matrix from the transfer matrix

            :parameter index: odd index of the general D matrix

            :parameter transfer_matrix: transfer matrix at reconstruction point

            :return self.d_matrix_step:  (filling in the d_matrix array)

        """
        i_overall = 0
        for i_dx in np.arange(int(self.d_matrix_step.shape[1] / 2) - 1):
            for i_dy in np.arange(i_dx, int(self.d_matrix_step.shape[1] / 2) - 1):
                if i_dy == i_dx:
                    self.d_matrix_step[index, i_overall] = transfer_matrix[index - 1, i_dy] * transfer_matrix[
                        index + 1, i_dx]
                else:
                    self.d_matrix_step[index, i_overall] = transfer_matrix[index - 1, i_dx] * transfer_matrix[
                        index + 1, i_dy] + \
                                                           transfer_matrix[index - 1, i_dy] * transfer_matrix[
                                                               index + 1, i_dx]
                i_overall += 1

    def calculation_d_matrix_step(self, transfer_matrix):
        """

        Calculation of the D matrix for a single set of values of quad scans

        :parameter transfer_matrix: Transfer matrix at the reconstruction point

        :return self.d_matrix: (filling in the d_matrix array)

        """
        self.d_matrix_step[0, 0] = np.square(transfer_matrix[0, 0])
        self.d_matrix_step[0, 1] = 2.0 * transfer_matrix[0, 0] * transfer_matrix[0, 1]
        self.d_matrix_step[0, 2] = 2.0 * transfer_matrix[0, 0] * transfer_matrix[0, 2]
        self.d_matrix_step[0, 3] = 2.0 * transfer_matrix[0, 0] * transfer_matrix[0, 3]
        self.d_matrix_step[0, 4] = np.square(transfer_matrix[0, 1])
        self.d_matrix_step[0, 5] = 2.0 * transfer_matrix[0, 1] * transfer_matrix[0, 2]
        self.d_matrix_step[0, 6] = 2.0 * transfer_matrix[0, 1] * transfer_matrix[0, 3]
        self.d_matrix_step[0, 7] = np.square(transfer_matrix[0, 2])
        self.d_matrix_step[0, 8] = 2.0 * transfer_matrix[0, 2] * transfer_matrix[0, 3]
        self.d_matrix_step[0, 9] = np.square(transfer_matrix[0, 3])

        self.d_matrix_step[1, 0] = transfer_matrix[0, 0] * transfer_matrix[2, 0]
        self.d_matrix_step[1, 1] = (transfer_matrix[0, 1] * transfer_matrix[2, 0]) + (
                transfer_matrix[0, 0] * transfer_matrix[2, 1])
        self.d_matrix_step[1, 2] = (transfer_matrix[0, 2] * transfer_matrix[2, 0]) + (
                transfer_matrix[0, 0] * transfer_matrix[2, 2])
        self.d_matrix_step[1, 3] = (transfer_matrix[0, 3] * transfer_matrix[2, 0]) + (
                transfer_matrix[0, 0] * transfer_matrix[2, 3])
        self.d_matrix_step[1, 4] = transfer_matrix[0, 1] * transfer_matrix[2, 1]
        self.d_matrix_step[1, 5] = (transfer_matrix[0, 2] * transfer_matrix[2, 1]) + (
                transfer_matrix[0, 1] * transfer_matrix[2, 2])
        self.d_matrix_step[1, 6] = (transfer_matrix[0, 3] * transfer_matrix[2, 1]) + (
                transfer_matrix[0, 1] * transfer_matrix[2, 3])
        self.d_matrix_step[1, 7] = transfer_matrix[0, 2] * transfer_matrix[2, 2]
        self.d_matrix_step[1, 8] = (transfer_matrix[0, 3] * transfer_matrix[2, 2]) + (
                transfer_matrix[0, 2] * transfer_matrix[2, 3])
        self.d_matrix_step[1, 9] = transfer_matrix[0, 3] * transfer_matrix[2, 3]

        self.d_matrix_step[2, 0] = np.square(transfer_matrix[2, 0])
        self.d_matrix_step[2, 1] = 2.0 * transfer_matrix[2, 0] * transfer_matrix[2, 1]
        self.d_matrix_step[2, 2] = 2.0 * transfer_matrix[2, 0] * transfer_matrix[2, 2]
        self.d_matrix_step[2, 3] = 2.0 * transfer_matrix[2, 0] * transfer_matrix[2, 3]
        self.d_matrix_step[2, 4] = np.square(transfer_matrix[2, 1])
        self.d_matrix_step[2, 5] = 2.0 * transfer_matrix[2, 1] * transfer_matrix[2, 2]
        self.d_matrix_step[2, 6] = 2.0 * transfer_matrix[2, 1] * transfer_matrix[2, 3]
        self.d_matrix_step[2, 7] = np.square(transfer_matrix[2, 2])
        self.d_matrix_step[2, 8] = 2.0 * transfer_matrix[2, 2] * transfer_matrix[2, 3]
        self.d_matrix_step[2, 9] = np.square(transfer_matrix[2, 3])

        # for index in np.arange(self.d_matrix.shape[0]):
        #    if np.remainder(index, 2) == 0:
        #        self.multiplication_d_matrix_even(index, transfer_matrix)
        #    else:
        #        self.multiplication_d_matrix_odd(index, transfer_matrix)

    def reconstruction_d_matrix(self):
        """
        Calculating the D matrix from the transfer matrix post Linac for all measurements

        :return  self.d_matrix: filling in the self.d_matrix (dimensions (3*self.nstep,10))

        """
        for n_step, q_str in zip(np.arange(self.nsteps), np.arange(len(self.qstrengths))):
            transfer_matrix = self.transfer_matrix_post_linac(self.qstrengths[q_str, :])
            self.calculation_d_matrix_step(transfer_matrix)
            self.d_matrix[(2*n_step):(2*n_step)+3, :] = deepcopy(self.d_matrix_step)
            #self.d_matrix.append(self.d_matrix_step)
        print('+++ D matrix is {}'.format(self.d_matrix))

    def covariance_matrix_reconstruction(self):
        """

        Reconstruction of the covariance matrix at reconstruction point from D Matrix and set of beamsizes

        :return  self.cov_matrix: (covariance matrix at reconstruction point)

        """
        self.reconstruction_d_matrix()
        #np.savetxt(os.path.join(os.getcwd(), 'd_matrix_test.dat'), self.d_matrix)
        np.savetxt(os.path.join(os.getcwd(), 'sigma_1_test.dat'), self.screen_data)
        dxinv = np.linalg.pinv(self.d_matrix)
        #np.savetxt(os.path.join(os.getcwd(), 'd_matrix_inv_test.dat'), dxinv)
        matrix_repr = np.matmul(dxinv, self.screen_data)
        setattr(self, 'cov_matrix', np.array([[matrix_repr[i] for i in np.arange(4)],
                                              [matrix_repr[1], matrix_repr[4], matrix_repr[5], matrix_repr[6]],
                                              [matrix_repr[2], matrix_repr[5], matrix_repr[7], matrix_repr[8]],
                                              [matrix_repr[3], matrix_repr[6], matrix_repr[8], matrix_repr[9]]]))

        np.savetxt(os.path.join(os.getcwd(), 'cov_matrix_test.dat'), self.cov_matrix)
        time.sleep(2)

    def finding_eigenvalues(self):
        """

        Method to find eigenvalues (in order to calculate the emittances as the imaginary eigenvalues of cov_matrix\dot S

        :return self.emit:  Emittances for both normal modes
        :return self.emit_matrix: Transformation between normal mode space and cartesian space

        """
        self.covariance_matrix_reconstruction()
        time.sleep(10)
        d_eigen, a_f = scipy.linalg.eig(np.matmul(self.cov_matrix, self.Smatrix))
        d_eigen = np.imag(d_eigen)
        ix = np.argsort(d_eigen, axis=0)
        ix2 = deepcopy(np.array([ix[i] for i in [0, 3, 1, 2]]))

        d_eigen_new = deepcopy(np.array([d_eigen[y] for y in [ix2[1], ix2[3]]]))
        m_transf = deepcopy(a_f[:, ix2])
        # Normalise the transformation matrix
        nrm = np.matmul(np.transpose(m_transf), np.matmul(self.Smatrix, np.matmul(m_transf, self.Smatrix)))
        m_transf = np.linalg.solve(np.transpose(m_transf), np.transpose(np.sqrt(np.absolute(nrm))))
        # m_transf = np.matmul(m_transf, np.linalg.inv(np.sqrt(np.absolute(nrm))))
        mx = m_transf[0:2, 0]
        my = m_transf[2:, 0]

        if np.matmul(np.transpose(mx), np.conjugate(mx)) < np.matmul(np.transpose(my), np.conjugate(my)):
            d_eigen_new = deepcopy(np.array([d_eigen_new[y] for y in [1, 0]]))
            m_transf = deepcopy(m_transf[:, [2, 3, 0, 1]])
        time.sleep(15)
        setattr(self, 'emits', np.multiply(1e6 * self.rel_gamma, d_eigen_new))
        setattr(self, 'emits_matrix', m_transf)
        print('+++++++++++ Emittances = {}'.format(getattr(self, 'emits')))
        np.savetxt(os.path.join(os.getcwd(), 'emittances_values.txt'), d_eigen_new)
        np.savetxt(os.path.join(os.getcwd(), 'normalised_emittances_values.txt'), self.emits)
        np.savetxt(os.path.join(os.getcwd(), 'emittance_matrix_values.txt'), self.emits_matrix)

    def plot_quad_scan(self):
        """

                Method to  plot the quad scans beam sizes and coupling terms

                """
        fig, ax = plt.subplots(2, 1)
        ax_y = ax[0].twinx()
        for axs, key, colour, title_l, marker in zip([ax[0], ax_y], ['x_var', 'y_var'], ['navy', 'forestgreen'],
                                                     [r'x$_{rms}$[mm]', r'y$_{rms}$[mm]'], ['o', "^"]):
            axs.plot(np.arange(1, 1+len(self.beam_sizes[key])), np.multiply(1.0e6, np.square(self.beam_sizes[key])), ls='--', lw=2.2,
                     color=colour,
                     marker='o',
                     ms=5)
            axs.set_ylim([0.8e6 * np.amin(np.square(self.beam_sizes[key])), 1.2e6 * np.amax(np.square(self.beam_sizes[key]))])
            axs.tick_params(axis='y', color=colour, labelcolor=colour)
            axs.set_ylabel(title_l, color=colour)
            axs.yaxis.get_offset_text().set_color(colour)
            plt.setp(axs.spines.values(), color=colour)
            plt.setp([axs.get_xticklines(), axs.get_yticklines()], color=colour)
            for ticks in axs.yaxis.get_major_ticks():
                ticks.label.set_color(colour)
        ax[1].plot(np.arange(1, 1 + len(self.beam_sizes[key])), np.multiply(1.0e6, self.beam_sizes['x_y_mean']),
                   ls='--', lw=2.2, color='red',
                   marker=marker, ms=5)
        ax[1].tick_params(axis='y', color='tomato')
        ax[1].set_ylabel(r'<xy> [mm$^2$]', color='tomato')
        ax[1].yaxis.get_offset_text().set_color('tomato')
        plt.setp(ax[1].spines.values(), color='tomato')
        plt.setp([ax[1].get_xticklines(), ax[1].get_yticklines()], color='tomato')
        ax[1].set_ylim([1.5e6 * np.amin(self.beam_sizes['x_y_mean']), 1.6e6 * np.amax(self.beam_sizes['x_y_mean'])])
        for ticks in ax[1].yaxis.get_major_ticks():
            ticks.label.set_color('tomato')
        for axs in ax:
            axs.set_xticks(np.arange(self.nsteps))
            axs.grid(True, color='navy')
            axs.set_title(self.screen, color = 'navy')
        plt.subplots_adjust(hspace=0.5, wspace=0.5)
        plt.savefig(self.path_output, format='png', dpi=120, bbox_inches='tight')

    def plot_quad_scan_strengths(self):
        """

                Method to  plot the quad scans strengths

                """
        fig, ax = plt.subplots(1, 1)

        for i_x, colour, marker in zip(np.arange(2, 5), ['darkslateblue', 'maroon', 'forestgreen'],
                                       ['o', '^', 'v']):
            ax.plot(np.arange(1, 1 + self.nsteps),
                    np.array([self.qstrengths[t][int(i_x)] for t in np.arange(self.nsteps)]),
                    ls='--', lw=2.2, color=colour, marker=marker, ms=5, label=r'Quad ' + str(int(i_x + 1)))
        leg = ax.legend()
        for line, text in zip(leg.get_lines(), leg.get_texts()):
            text.set_color(line.get_color())
        ax.set_ylabel('Quad Strength [m$^{-1}$]', color='navy')
        ax.set_xlabel('Step', color='navy')
        ax.yaxis.get_offset_text().set_color('navy')
        plt.setp(ax.spines.values(), color='navy')
        plt.setp([ax.get_xticklines(), ax.get_yticklines()], color='navy')
        for key in ['xaxis', 'yaxis']:
            axs = getattr(ax, key)
            for ticks in axs.get_major_ticks():
                ticks.label.set_color('navy')

        ax.set_xticks(np.arange(1, 1 + self.nsteps))
        ax.grid(True, color='navy')
        plt.subplots_adjust(hspace=0.5, wspace=0.5)
        plt.savefig(os.path.join(os.getcwd(), 'quad_scan_strength.png'), format='png', dpi=120, bbox_inches='tight')
