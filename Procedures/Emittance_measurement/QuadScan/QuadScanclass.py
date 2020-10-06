import numpy as np
from copy import deepcopy
import scipy.constants
import scipy.linalg
import scipy.optimize
from collections import OrderedDict
import time
import os
import sys
import cmath
from scipy import linalg
from cycler import cycler
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..', '..', '..', 'SimFrame_fork', 'simframe')))
#sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..', '..', 'SimFrame_fork', 'simframe')))
import SimulationFramework.Modules.read_twiss_file as read_twiss_file


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
    Smatrix = np.zeros((4, 4))
    for indx in np.arange(Smatrix.shape[0]):
        for indy in np.arange(Smatrix.shape[1]):
            if indx == 0:
                if indy == 1:
                    value = 1.0
                else:
                    value = 0.0
            elif indx == 1:
                if indy == 0:
                    value = -1.0
                else:
                    value = 0.0
            elif indx == 2:
                if indy == 3:
                    value = 1.0
                else:
                    value = 0.0
            else:
                if indy == 2:
                    value = -1.0
                else:
                    value = 0.0
            Smatrix[indx, indy] = value
    # Smatrix = np.array([[0, 1, 0, 0],
    #                    [-1, 0, 0, 0],
    #                    [0, 0, 0, 1],
    #                    [0, 0, -1, 0]])  #: Smatrix
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
        self.__cov_m_linac = np.zeros((4, 4))  #: Covariance Matrix postLinac
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
        self.__screen = ''  #: Screen to plot the data
        self.BeamMomentum = 40.0  #: Beam momentum 30.0 MeV nominal
        self.rel_gamma = 40.0 / self.m_e_MeV  #: relative gamma: 45

    @property
    def charge(self):
        """

            Charge attribute in pC

            :type: float(Charge):

        """
        return self.__charge

    @property
    def input_dist(self):
        """


            Input distribution

            :type: dictionary(Input distribution):

        """
        if self.__input_dist != '':
            return np.loadtxt(self.__input_dist)
        else:
            return self.__input_dist

    @property
    def cov_matrix(self):
        """

            Covariance matrix at the reconstruction point

            :type: Array(4,4): covariance matrix at reconstruction point:

        """
        return deepcopy(self.__cov_matrix)

    @property
    def cov_m_linac(self):
        """

            Covariance matrix at the end of the LINAC

            :type: Array (4,4) (array with the covariance matrix at the end of the LINAC, read from the hdf5 file distribution):

        """
        return deepcopy(self.__cov_m_linac)

    @property
    def emits(self):
        """

            Normal emittances

            :type: Array(2,1)(Normal mode emittances):

        """
        return deepcopy(self.__emits)

    @property
    def emits_matrix(self):
        """

            Transformation matrix between cartesian and the normal mode space

            :type: Array (4,4)(Transformation matrix):

        """
        return deepcopy(self.__emits_matrix)

    @property
    def qstrengths(self):
        """

            Optimised Quad Strengths for Quad Scan

            :type: Array (nsteps, 5): Matrix of quad strength values:

        """
        return deepcopy(self.__qstrengths)

    @property
    def nsteps(self):  #: Number of steps of Quad Scan: 20
        """

            Number of steps for the quad scan (defines the shape of the covariance matrix, d matrix and beam size matrix)

            :type: integer(Number of steps):

        """
        return deepcopy(int(self.__nsteps))

    @property
    def beam_sizes(self):
        """
            Matrix with the beam sizes at the observation point and the coupling parameter

            :type: Matrix (3*nsteps,1)(Beam sizes Matrix):

        """
        return self.__beam_sizes

    @property
    def screen_data(self):
        """
            Reorganised data obtained from the screen to be used in order to determine the cov. matrix at reconstruction point

            :type: matrix (3*nsteps,1)(Screen data matrix):

        """
        return self.__screen_data

    @property
    def path_output(self):
        """
            Path and name to save the beam size plot obtained at the end of the quad scan

            :type: string(Path to save the plot):


        """
        return self.__path_output

    @property
    def screen(self):
        """
            Screen where the results are displayed

            :type: string(Name of the screen):

        """
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

            :param filename: Path of the file to be opened:

            :return Array: the contents of the file:

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

            :param currents: Currents:

            :param beamMomentum: Beam Momentum:

            :return k_values: k values for each quadrupole:

        """
        ## quad calibrations are in the magnet controller
        pfitq = np.array(self.FileOpen('QuadCalibration.txt'))

        # currents are from the experiment
        currents = np.array(currents)
        kvals = np.zeros(5)
        for n in np.arange(5):
            kvals[n] = 0.0
            for p in np.arange(4):
                kvals[n] = kvals[n] + pfitq[p][n] * currents[n] ** (3.0 - p)
        # k value with momentum - what is this factor of 30???
        return np.multiply(kvals, 30.0 / beamMomentum)

    @staticmethod
    def transfer_matrix_drift(length):
        """

            Transfer matrix for Drifts

            :param length: Drift length:

            :return Transfer Matrix for a drift:

        """
        return np.array([[1.0, length, 0.0, 0.0],
                         [0.0, 1.0, 0.0, 0.0],
                         [0.0, 0.0, 1.0, length],
                         [0.0, 0.0, 0.0, 1.0]])

    def transfer_matrix_quad(self, k1, length):
        """

            Transfer Matrix for a Quad (Thin Lens approximation)

            :param k1: Quad Strength:

            :param length: Length of the quad:

            :return  Matrix: Transfer matrix for a Quad:

        """
        m = deepcopy(self.transfer_matrix_drift(length))

        if k1 != 0.0:
            if k1 < 0.0:
                omega = complex(0, np.sqrt(np.abs(k1)))
                m = np.array(m)
                m[0, :] = deepcopy(np.array([cmath.cos(omega * length), cmath.sin(omega * length) / omega, 0, 0]))
                m[1, :] = deepcopy(np.array([- cmath.sin(omega * length) * omega, cmath.cos(omega * length), 0, 0]))
                m[2, :] = deepcopy(np.array([0.0, 0.0, cmath.cosh(omega * length), cmath.sinh(omega * length) / omega]))
                m[3, :] = deepcopy(np.array([0.0, 0.0, cmath.sinh(omega * length) * omega, cmath.cosh(omega * length)]))
            else:
                omega = np.sqrt(k1)
                m[0, :] = deepcopy(np.array([np.cos(omega * length), np.sin(omega * length) / omega, 0.0, 0.0]))
                m[1, :] = deepcopy(np.array([- np.sin(omega * length) * omega, np.cos(omega * length), 0.0, 0.0]))
                m[2, :] = deepcopy(np.array([0.0, 0.0, np.cosh(omega * length), np.sinh(omega * length) / omega]))
                m[3, :] = deepcopy(np.array([0.0, 0.0, np.sinh(omega * length) * omega, np.cosh(omega * length)]))
            m = np.real(np.array(m))
        return m

    def transfer_matrix_post_linac(self, q_strengths):
        """

            Transfer Matrix to be obtained after the LINAC (Simulation)

            :param  q_strengths: Optimised quad strengths:

            :return Matrix: Transfer Matrix at the end of the LINAC:

        """

        mq1 = self.transfer_matrix_quad(q_strengths[0], self.qlength)
        mq2 = self.transfer_matrix_quad(q_strengths[1], self.qlength)
        md1 = self.transfer_matrix_drift(self.dlen1)
        md2 = self.transfer_matrix_drift(self.dlen2)
        md3 = self.transfer_matrix_drift(self.dlen3)

        return np.dot(md3, np.dot(mq2, np.dot(md2, np.dot(mq1, md1))))

    def transfer_matrix_quad_scan(self, q_strengths):
        """

            Transfer Matrix to be obtained at the reconstruction point.

            :param  q_strengths: Optimised quad strengths:

            :return Matrix: Transfer Matrix at the reconstruction point:

        """
        dlen1 = 0.165967
        dlen2 = 0.299300
        dlen3 = 0.712450
        dlen4 = 0.181183
        mq3 = self.transfer_matrix_quad(q_strengths[2], self.qlength)
        mq4 = self.transfer_matrix_quad(q_strengths[3], self.qlength)
        mq5 = self.transfer_matrix_quad(q_strengths[4], self.qlength)
        md1 = self.transfer_matrix_drift(dlen1)
        md2 = self.transfer_matrix_drift(dlen2)
        md3 = self.transfer_matrix_drift(dlen3)
        md4 = self.transfer_matrix_drift(dlen4)
        return np.dot(md4, np.dot(mq5, np.dot(md3, np.dot(mq4, np.dot(md2, np.dot(mq3, md1))))))

    def match_beam_divergence(self, sig_xpx, sig_ypy, q_strength):
        """

            Method to match the beam and optimise the quads (finding an elliptical beam with waist at observation point)

            :param sig_xpx: coupling transversal term in x:

            :param sig_ypy:  coupling transversal term in y:

            :param q_strength: Quad strength:

            :return difference of coupling terms: to be minimise:

        """
        tm = self.transfer_matrix_post_linac(q_strength)
        cm = np.dot(np.dot(tm, self.cov_matrix), np.transpose(tm))
        return np.square(cm[0, 1] - sig_xpx) + np.square(cm[2, 3] - sig_ypy)

    def merit_function(self, sig_xpx, sig_ypy):
        """

            Merit function to be minimise

            :param sig_xpx:

            :param sig_ypy:

            :return lambda function:  to minimise as a function of quad strength:

        """
        return lambda q_str: self.match_beam_divergence(sig_xpx, sig_ypy, q_str)

    def optimising_match_divergence(self, sig_xpx, sig_ypy, q_strength):
        """

            Method to find the optimum quads

            :param sig_xpx: Transversal coupling term in x:

            :param sig_ypy: Transversal coupling term in y

            :param q_strength: Initial guess of quad strength:

            :return optimum quad strength: Optimised quad strength:

        """
        return scipy.optimize.fmin(func=self.merit_function(sig_xpx, sig_ypy), x0=q_strength)

    def transfer_matrix_from_simframe(self, directory):

        """

        Transfer matrix between reconstruction point and observation point, extracted from SIMFRAME

        :param directory: Directory where the quad scans input and output files are located

        :return: transfer_matrix: Transfer matrix between reconstruction point and observation point

        """
        transfer_matrix = np.zeros((4, 4))
        transfer_matrix_rec_point = np.zeros_like(transfer_matrix)
        transfer_matrix_obs_point = np.zeros_like(transfer_matrix)

        twiss_object = read_twiss_file.twiss()

        for file_mat in os.listdir(directory):
            if file_mat.endswith('.mat'):
                file_sdds = deepcopy(os.path.join(directory, file_mat))
            else:
                continue
        twiss_object.read_sdds_file(file_sdds, ascii=False)
        index_rec = np.where(twiss_object['elegant']['ElementName'] == 'CLA-S02-DIA-SCR-02')[0][0]
        index_obs = np.where(twiss_object['elegant']['ElementName'] == 'CLA-S02-DIA-SCR-03')[0][0]

        for key in twiss_object['elegant'].keys():
            if key.startswith('R'):
                number = deepcopy(int(key.replace('R', '')))
                i = int(number / 10)
                j = np.remainder(number, 10)
                if (i <= 4) and (j <= 4):
                    transfer_matrix[i - 1, j - 1] = float(twiss_object['elegant'][key][index_obs])
                    transfer_matrix_rec_point[i - 1, j - 1] = float(twiss_object['elegant'][key][index_rec])
                else:
                    continue
            else:
                continue
        return np.dot(transfer_matrix, np.linalg.inv(transfer_matrix_rec_point))

    def calculation_d_matrix_step(self, transfer_matrix):
        """

        Calculation of the D matrix for a single set of values of quad scans

        :param transfer_matrix: Transfer matrix at the reconstruction point:

        :return: self.d_matrix: (filling in the d_matrix array):

        """
        d_matrix_step = np.zeros((3, 10))
        d_matrix_step[0, 0] = np.square(transfer_matrix[0, 0])
        d_matrix_step[0, 1] = 2.0 * transfer_matrix[0, 0] * transfer_matrix[0, 1]
        d_matrix_step[0, 2] = 2.0 * transfer_matrix[0, 0] * transfer_matrix[0, 2]
        d_matrix_step[0, 3] = 2.0 * transfer_matrix[0, 0] * transfer_matrix[0, 3]
        d_matrix_step[0, 4] = np.square(transfer_matrix[0, 1])
        d_matrix_step[0, 5] = 2.0 * transfer_matrix[0, 1] * transfer_matrix[0, 2]
        d_matrix_step[0, 6] = 2.0 * transfer_matrix[0, 1] * transfer_matrix[0, 3]
        d_matrix_step[0, 7] = np.square(transfer_matrix[0, 2])
        d_matrix_step[0, 8] = 2.0 * transfer_matrix[0, 2] * transfer_matrix[0, 3]
        d_matrix_step[0, 9] = np.square(transfer_matrix[0, 3])

        d_matrix_step[1, 0] = transfer_matrix[0, 0] * transfer_matrix[2, 0]
        d_matrix_step[1, 1] = (transfer_matrix[0, 1] * transfer_matrix[2, 0]) + (
                transfer_matrix[0, 0] * transfer_matrix[2, 1])
        d_matrix_step[1, 2] = (transfer_matrix[0, 2] * transfer_matrix[2, 0]) + (
                transfer_matrix[0, 0] * transfer_matrix[2, 2])
        d_matrix_step[1, 3] = (transfer_matrix[0, 3] * transfer_matrix[2, 0]) + (
                transfer_matrix[0, 0] * transfer_matrix[2, 3])
        d_matrix_step[1, 4] = transfer_matrix[0, 1] * transfer_matrix[2, 1]
        d_matrix_step[1, 5] = (transfer_matrix[0, 2] * transfer_matrix[2, 1]) + (
                transfer_matrix[0, 1] * transfer_matrix[2, 2])
        d_matrix_step[1, 6] = (transfer_matrix[0, 3] * transfer_matrix[2, 1]) + (
                transfer_matrix[0, 1] * transfer_matrix[2, 3])
        d_matrix_step[1, 7] = transfer_matrix[0, 2] * transfer_matrix[2, 2]
        d_matrix_step[1, 8] = (transfer_matrix[0, 3] * transfer_matrix[2, 2]) + (
                transfer_matrix[0, 2] * transfer_matrix[2, 3])
        d_matrix_step[1, 9] = transfer_matrix[0, 3] * transfer_matrix[2, 3]

        d_matrix_step[2, 0] = np.square(transfer_matrix[2, 0])
        d_matrix_step[2, 1] = 2.0 * transfer_matrix[2, 0] * transfer_matrix[2, 1]
        d_matrix_step[2, 2] = 2.0 * transfer_matrix[2, 0] * transfer_matrix[2, 2]
        d_matrix_step[2, 3] = 2.0 * transfer_matrix[2, 0] * transfer_matrix[2, 3]
        d_matrix_step[2, 4] = np.square(transfer_matrix[2, 1])
        d_matrix_step[2, 5] = 2.0 * transfer_matrix[2, 1] * transfer_matrix[2, 2]
        d_matrix_step[2, 6] = 2.0 * transfer_matrix[2, 1] * transfer_matrix[2, 3]
        d_matrix_step[2, 7] = np.square(transfer_matrix[2, 2])
        d_matrix_step[2, 8] = 2.0 * transfer_matrix[2, 2] * transfer_matrix[2, 3]
        d_matrix_step[2, 9] = np.square(transfer_matrix[2, 3])

        setattr(self, 'd_matrix_step', d_matrix_step)

    def cov_matrix_from_simframe(self, screen, directory):

        """

        Covariance matrix at reconstruction point, extracted from SIMFRAME

        :param screen:
        :param directory: Directory where the quad scans input and output files are located

        :return: cov_matrix: Covariant matrix at reconstruction point

        """
        cov_matrix = np.zeros((4, 4))
        twiss_object = read_twiss_file.twiss()

        for file_sig in os.listdir(directory):
            if file_sig.endswith('.sig'):
                file_sdds = deepcopy(os.path.join(directory, file_sig))
            else:
                continue
        twiss_object.read_sdds_file(file_sdds,  ascii=False)
        index_obs = np.where(twiss_object['elegant']['ElementName'] == screen)[0][0]
        keys = [key for key in twiss_object['elegant'].keys() if key.startswith('s') and not key.endswith('s')]
        for key in keys:
            number = deepcopy(int(key.replace('s', '')))
            if 4 < number < 10:
                continue
            elif number <= 4:
                if number == 1:
                    i = 1
                    j = 1
                elif number == 2:
                    i = 2
                    j = 2
                elif number == 3:
                    i = 3
                    j = 3
                elif number == 4:
                    i = 4
                    j = 4
                value = deepcopy(np.square(twiss_object['elegant'][key][index_obs]))
            else:
                i = int(number / 10)
                j = np.remainder(number, 10)
                if (i <= 4) and (j <= 4):
                    value = deepcopy(float(twiss_object['elegant'][key][index_obs]))
                else:
                    continue
            cov_matrix[i - 1, j - 1] = value
        return cov_matrix

    def reconstruction_d_matrix(self):
        """

            Calculating the D matrix from the transfer matrix post Linac for all measurements

            :return  self.d_matrix: filling in the self.d_matrix (dimensions (3*self.nstep,10)):

        """

        d_matrix = np.zeros_like(self.d_matrix)

        # for n_step, q_str in zip(np.arange(self.nsteps), np.arange(len(self.qstrengths))):
        for n_step in np.arange(self.nsteps):
            # quad_strengths = deepcopy(self.qstrengths[q_str, :])
            # transfer_matrix = self.transfer_matrix_quad_scan(quad_strengths)
            transfer_matrix = self.transfer_matrix_from_simframe(os.path.abspath(os.path.join(os.getcwd(),
                                                                                              'quad_scan_setup_' +
                                                                                              str(n_step))))
            np.savetxt(os.path.abspath(os.path.join(os.getcwd(), 'quad_scan_setup_' + str(n_step),
                                                    "transfer_matrix_rec_obs_VM.txt")), transfer_matrix)
            self.calculation_d_matrix_step(transfer_matrix)
            # cov_matrix_rec_point=self.cov_matrix_from_simframe('CLA-S02-DIA-SCR-02',
            #    os.path.join('C:\\','Users','qfi29231','Documents','spawn_emittances', 'Emittance_GUI','quad_scan_setup_'+str(n_step)))
            # cov_matrix_obs_point = self.cov_matrix_from_simframe('CLA-S02-DIA-SCR-03',
            #                                                     os.path.join('C:\\', 'Users', 'qfi29231', 'Documents',
            #                                                                  'spawn_emittances', 'Emittance_GUI',
            #                                                                  'quad_scan_setup_' + str(n_step)))

            for k in np.arange(self.d_matrix_step.shape[1]):
                d_matrix[(3 * n_step), k] = deepcopy(self.d_matrix_step[0, k])
                d_matrix[(3 * n_step) + 1, k] = deepcopy(self.d_matrix_step[1, k])
                d_matrix[(3 * n_step) + 2, k] = deepcopy(self.d_matrix_step[2, k])
        setattr(self, 'd_matrix', d_matrix)

    def covariance_matrix_reconstruction(self):
        """

        Reconstruction of the covariance matrix at reconstruction point from D Matrix and set of beamsizes

        :return  self.cov_matrix: (covariance matrix at reconstruction point):

        """
        matrix_cov = np.zeros_like(self.cov_matrix)
        self.reconstruction_d_matrix()
        np.savetxt(os.path.join(os.getcwd(), 'd_matrix_test.dat'), self.d_matrix)
        np.savetxt(os.path.join(os.getcwd(), 'sigma_1_test.dat'), self.screen_data)
        # dxinv = np.linalg.pinv(self.d_matrix, rcond=1e-5, hermitian=False)
        dxinv = linalg.pinv2(self.d_matrix, rcond=1.e-8)
        np.savetxt(os.path.join(os.getcwd(), 'd_matrix_inv_test.dat'), dxinv)
        matrix_repr = np.dot(dxinv, self.screen_data)
        for ix in np.arange(self.cov_matrix.shape[0]):
            for iy in np.arange(self.cov_matrix.shape[1]):
                if ix == 0:
                    value = deepcopy(matrix_repr[iy])
                elif ix == 1:
                    if iy == 0:
                        value = deepcopy(matrix_repr[1])
                    elif iy == 1:
                        value = deepcopy(matrix_repr[4])
                    elif iy == 2:
                        value = deepcopy(matrix_repr[5])
                    else:
                        value = deepcopy(matrix_repr[6])
                elif ix == 2:
                    if iy == 0:
                        value = deepcopy(matrix_repr[2])
                    elif iy == 1:
                        value = deepcopy(matrix_repr[5])
                    elif iy == 2:
                        value = deepcopy(matrix_repr[7])
                    else:
                        value = deepcopy(matrix_repr[8])
                else:
                    if iy == 0:
                        value = deepcopy(matrix_repr[3])
                    elif iy == 1:
                        value = deepcopy(matrix_repr[6])
                    elif iy == 2:
                        value = deepcopy(matrix_repr[8])
                    else:
                        value = deepcopy(matrix_repr[9])
                matrix_cov[ix, iy] = deepcopy(value)
        setattr(self, 'cov_matrix', matrix_cov)
        directory = os.path.join('C:\\', 'Users', 'qfi29231', 'Documents', 'spawn_emittances', 'Emittance_GUI',
                                 'quad_scan_setup_0')
        np.savetxt(os.path.join(os.getcwd(), 'cov_matrix_test.dat'), self.cov_matrix)
        np.savetxt(os.path.join(os.getcwd(), 'cov_matrix_test_sdds.dat'),
                   self.cov_matrix_from_simframe('CLA-S02-DIA-SCR-02', directory))
        np.savetxt(os.path.join(os.getcwd(), 'Cov_times_Smatrix.txt'), np.dot(self.cov_matrix, self.Smatrix))

    def finding_eigenvalues(self):
        """

        Method to find eigenvalues (in order to calculate the emittances as the imaginary eigenvalues of cov_matrix\dot S

        :return self.emit:  Emittances for both normal modes:

        :return self.emit_matrix: Transformation between normal mode space and cartesian space:

        """
        setattr(self, 'rel_gamma', getattr(self, 'BeamMomentum') / self.m_e_MeV)
        self.covariance_matrix_reconstruction()
        time.sleep(2)
        d_eigen, a_f = scipy.linalg.eig(np.dot(self.cov_matrix, self.Smatrix))
        d_eigen = np.imag(d_eigen)
        ix = np.argsort(d_eigen, axis=0)
        ix2 = deepcopy(np.array([ix[i] for i in [0, 3, 1, 2]]))

        d_eigen_new = deepcopy(np.array([d_eigen[y] for y in [ix2[1], ix2[3]]]))
        m_transf = deepcopy(a_f[:, ix2])
        # Normalise the transformation matrix
        nrm = np.dot(np.transpose(m_transf), np.dot(self.Smatrix, np.dot(m_transf, self.Smatrix)))
        m_transf = np.linalg.solve(np.transpose(m_transf), np.transpose(np.sqrt(np.absolute(nrm))))
        # m_transf = np.dot(m_transf, np.linalg.inv(np.sqrt(np.absolute(nrm))))
        mx = m_transf[0:2, 0]
        my = m_transf[2:, 0]

        if np.dot(np.transpose(mx), np.conjugate(mx)) < np.dot(np.transpose(my), np.conjugate(my)):
            d_eigen_new = deepcopy(np.array([d_eigen_new[y] for y in [1, 0]]))
            m_transf = deepcopy(m_transf[:, [2, 3, 0, 1]])
        time.sleep(15)

        setattr(self, 'emits', np.multiply(1.0e6 * self.rel_gamma, d_eigen_new))
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
                                                     [r'x$_{rms}$[m]', r'y$_{rms}$[m]'], ['o', "^"]):
            axs.plot(np.arange(1, 1 + len(self.beam_sizes[key])), np.multiply(1.0, self.beam_sizes[key]), ls='--',
                     lw=2.2,
                     color=colour,
                     marker='o',
                     ms=5)
            axs.set_ylim([0.999 * np.amin(self.beam_sizes[key]), 1.005 * np.amax(self.beam_sizes[key])])
            axs.tick_params(axis='y', color=colour, labelcolor=colour)
            axs.set_ylabel(title_l, color=colour)
            axs.yaxis.get_offset_text().set_color(colour)
            plt.setp(axs.spines.values(), color=colour)
            plt.setp([axs.get_xticklines(), axs.get_yticklines()], color=colour)
            for ticks in axs.yaxis.get_major_ticks():
                ticks.label.set_color(colour)
                ticks.label.set_fontsize(11)
        ax[1].plot(np.arange(1, 1 + len(self.beam_sizes[key])), np.multiply(1.0, self.beam_sizes['x_y_mean']),
                   ls='--', lw=2.2, color='red',
                   marker=marker, ms=5)
        ax[1].tick_params(axis='y', color='tomato')
        ax[1].set_ylabel(r'<xy> [m$^2$]', color='tomato')
        ax[1].yaxis.get_offset_text().set_color('tomato')
        plt.setp(ax[1].spines.values(), color='tomato')
        plt.setp([ax[1].get_xticklines(), ax[1].get_yticklines()], color='tomato')
        ax[1].set_ylim([0.999 * np.amin(self.beam_sizes['x_y_mean']), 1.001 * np.amax(self.beam_sizes['x_y_mean'])])
        for ticks in ax[1].yaxis.get_major_ticks():
            ticks.label.set_color('tomato')
            ticks.label.set_fontsize(11)
        for axs in ax:
            axs.set_xticks(np.arange(1, 1 + self.nsteps))
            axs.set_xticklabels(np.arange(1, 1 + self.nsteps), fontsize=11)
            axs.grid(True, color='navy')
            axs.set_title(self.screen, color='navy')
        plt.subplots_adjust(hspace=0.5, wspace=0.5)
        plt.savefig(self.path_output, format='png', dpi=120, bbox_inches='tight')

    def plot_quad_scan_strengths(self):
        """

            Method to  plot the quad scans strengths

        """

        fig, ax = plt.subplots(1, 1)

        for i_x, colour, marker in zip(np.arange(2, 5), ['darkslateblue', 'maroon', 'forestgreen'],
                                       ['o', '^', 'v']):
            if i_x == 2:
                mag_leng = 0.127242
            elif i_x == 3:
                mag_leng = 0.127422
            else:
                mag_leng = 0.127163
            ax.plot(np.arange(1, 1 + self.nsteps),
                    np.array([np.multiply(mag_leng, self.qstrengths[t][int(i_x)]) for t in np.arange(self.nsteps)]),
                    ls='--', lw=2.2, color=colour, marker=marker, ms=5, label=r'Quad ' + str(int(i_x + 1)))
        leg = ax.legend()
        for line, text in zip(leg.get_lines(), leg.get_texts()):
            text.set_color(line.get_color())
        ax.set_ylabel('k$_1 $L$_{magnetic}$ [m$^{-1}$]', color='navy')
        ax.set_xlabel('Step', color='navy')
        ax.yaxis.get_offset_text().set_color('navy')
        ax.set_xticks(np.arange(1, 1 + self.nsteps))
        ax.set_xticklabels(np.arange(1, 1 + self.nsteps), fontsize=10)

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
